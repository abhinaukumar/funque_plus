import numpy as np


def im2col(img, k, stride=1):
    # Parameters
    m, n = img.shape
    s0, s1 = img.strides
    nrows = m - k + 1
    ncols = n - k + 1
    shape = (k, k, nrows, ncols)
    arr_stride = (s0, s1, s0, s1)

    ret = np.lib.stride_tricks.as_strided(img, shape=shape, strides=arr_stride)
    return ret[:, :, ::stride, ::stride].reshape(k*k, -1)


def integral_image(x):
    M, N = x.shape
    int_x = np.zeros((M+1, N+1))
    # int_x[1:, 1:] = np.cumsum(np.cumsum(x, 0), 1)
    # Slower, but more precise than cumsum
    for i in range(x.shape[0]):
        int_x[i+1, 1:] = int_x[i, 1:] + x[i, :]
    for j in range(x.shape[1]):
        int_x[:, j+1] = int_x[:, j+1] + int_x[:, j]
    return int_x


def moments(x, y, k, stride):
    kh = kw = k

    k_norm = k**2

    x_pad = np.pad(x, int((kh - stride)/2), mode='reflect')
    y_pad = np.pad(y, int((kw - stride)/2), mode='reflect')

    int_1_x = integral_image(x_pad)
    int_1_y = integral_image(y_pad)

    int_2_x = integral_image(x_pad*x_pad)
    int_2_y = integral_image(y_pad*y_pad)

    int_xy = integral_image(x_pad*y_pad)

    mu_x = (int_1_x[:-kh:stride, :-kw:stride] - int_1_x[:-kh:stride, kw::stride] - int_1_x[kh::stride, :-kw:stride] + int_1_x[kh::stride, kw::stride])/k_norm
    mu_y = (int_1_y[:-kh:stride, :-kw:stride] - int_1_y[:-kh:stride, kw::stride] - int_1_y[kh::stride, :-kw:stride] + int_1_y[kh::stride, kw::stride])/k_norm

    var_x = (int_2_x[:-kh:stride, :-kw:stride] - int_2_x[:-kh:stride, kw::stride] - int_2_x[kh::stride, :-kw:stride] + int_2_x[kh::stride, kw::stride])/k_norm - mu_x**2
    var_y = (int_2_y[:-kh:stride, :-kw:stride] - int_2_y[:-kh:stride, kw::stride] - int_2_y[kh::stride, :-kw:stride] + int_2_y[kh::stride, kw::stride])/k_norm - mu_y**2

    cov_xy = (int_xy[:-kh:stride, :-kw:stride] - int_xy[:-kh:stride, kw::stride] - int_xy[kh::stride, :-kw:stride] + int_xy[kh::stride, kw::stride])/k_norm - mu_x*mu_y

    mask_x = (var_x < 0)
    mask_y = (var_y < 0)

    var_x[mask_x] = 0
    var_y[mask_y] = 0

    cov_xy[mask_x + mask_y] = 0

    return (mu_x, mu_y, var_x, var_y, cov_xy)


def vif_channel_est(y_ref, y_dist, winsize, M=3):
    tol = 1e-15

    y_size = (int(y_ref.shape[0]/M)*M, int(y_ref.shape[1]/M)*M)
    y_ref = y_ref[:y_size[0], :y_size[1]]
    y_dist = y_dist[:y_size[0], :y_size[1]]

    _, _, var_x, var_y, cov_xy = moments(y_ref, y_dist, winsize, M)

    g = cov_xy / (var_x + tol)
    sigma_vsq = var_y - g*cov_xy

    g[var_x < tol] = 0
    sigma_vsq[var_x < tol] = var_y[var_x < tol]
    var_x[var_x < tol] = 0
    g[var_y < tol] = 0
    sigma_vsq[var_y < tol] = 0
    sigma_vsq[g < 0] = var_y[g < 0]
    g[g < 0] = 0
    sigma_vsq[sigma_vsq < tol] = tol

    return g, sigma_vsq


def vif_spatial(img_ref, img_dist, k=11, sigma_nsq=0.1, stride=1, full=False):
    x = img_ref.astype('float64')
    y = img_dist.astype('float64')

    _, _, var_x, var_y, cov_xy = moments(x, y, k, stride)

    g = cov_xy / (var_x + 1e-10)
    sv_sq = var_y - g * cov_xy

    g[var_x < 1e-10] = 0
    sv_sq[var_x < 1e-10] = var_y[var_x < 1e-10]
    var_x[var_x < 1e-10] = 0

    g[var_y < 1e-10] = 0
    sv_sq[var_y < 1e-10] = 0

    sv_sq[g < 0] = var_x[g < 0]
    g[g < 0] = 0
    sv_sq[sv_sq < 1e-10] = 1e-10

    vif_val = np.sum(np.log(1 + g**2 * var_x / (sv_sq + sigma_nsq)) + 1e-4)/np.sum(np.log(1 + var_x / sigma_nsq) + 1e-4)
    if (full):
        return (np.sum(np.log(1 + g**2 * var_x / (sv_sq + sigma_nsq)) + 1e-4), np.sum(np.log(1 + var_x / sigma_nsq) + 1e-4), vif_val)
    else:
        return vif_val


def msvif_spatial(img_ref, img_dist, k=11, sigma_nsq=0.1, stride=1, full=False):
    x = img_ref.astype('float64')
    y = img_dist.astype('float64')

    n_levels = 5
    nums = np.ones((n_levels,))
    dens = np.ones((n_levels,))
    for i in range(n_levels-1):
        if np.min(x.shape) <= k:
            break
        nums[i], dens[i], _ = vif_spatial(x, y, k, sigma_nsq, stride, full=True)
        x = x[:(x.shape[0]//2)*2, :(x.shape[1]//2)*2]
        y = y[:(y.shape[0]//2)*2, :(y.shape[1]//2)*2]
        x = (x[::2, ::2] + x[1::2, ::2] + x[1::2, 1::2] + x[::2, 1::2])/4
        y = (y[::2, ::2] + y[1::2, ::2] + y[1::2, 1::2] + y[::2, 1::2])/4

    if np.min(x.shape) > k:
        nums[-1], dens[-1], _ = vif_spatial(x, y, k, sigma_nsq, stride, full=True)
    msvifval = np.sum(nums) / np.sum(dens)

    if full:
        return msvifval, nums, dens
    else:
        return msvifval
