import numpy as np
from scipy import ndimage
import cv2
from skimage.registration import optical_flow_ilk
from skimage.transform import warp

from ..funque_atoms.vif_utils import im2col

def block_sums(img, k, stride=1):
    # Parameters
    m, n = img.shape
    s0, s1 = img.strides
    nrows = m - k + 1
    ncols = n - k + 1
    shape = (k, k, nrows, ncols)
    arr_stride = (s0, s1, s0, s1)

    block_img = np.lib.stride_tricks.as_strided(img, shape=shape, strides=arr_stride)
    return block_img[..., ::stride, ::stride].sum(0).sum(0)


def optical_flow(img, img_prev, window_size, tau=1e-2):
    # Low and high-pass filters for gradient computation
    k_lo = np.array([1.0, 1.0])
    k_hi = np.array([-1.0, 1.0])

    w = window_size//2
    fx = ndimage.convolve1d(ndimage.convolve1d(img, k_lo, axis=0), k_hi, axis=1)
    fy = ndimage.convolve1d(ndimage.convolve1d(img, k_hi, axis=0), k_lo, axis=1)
    ft = ndimage.convolve1d(ndimage.convolve1d(img - img_prev, k_lo, axis=0), k_lo, axis=1)

    sum_fx_2 = block_sums(fx*fx, window_size, stride=1)
    sum_fy_2 = block_sums(fy*fy, window_size, stride=1)
    sum_fxy = block_sums(fx*fy, window_size, stride=1)
    sum_fxt = block_sums(fx*ft, window_size, stride=1)
    sum_fyt = block_sums(fy*ft, window_size, stride=1)

    # x direction velocity
    u = (sum_fxy*sum_fyt - sum_fy_2*sum_fxt) / (sum_fx_2*sum_fy_2 - sum_fxy**2)
    # y direction velocity
    v = (sum_fxy*sum_fxt - sum_fx_2*sum_fyt) / (sum_fx_2*sum_fy_2 - sum_fxy**2)

    # Apply stability constraint on smaller eigenvalue
    min_eig = 0.5*(sum_fx_2 + sum_fy_2 - np.sqrt((sum_fx_2 + sum_fy_2)**2 + 4*sum_fxy**2))
    u[min_eig < tau] = 0
    v[min_eig < tau] = 0

    return np.stack([u,v], axis=-1)

def compensated_diff(img, img_prev):
    # Based on skimage registration example
    # --- Compute the optical flow
    v, u = optical_flow_ilk(img_prev, img, radius=4, num_warp=4)

    # --- Use the estimated optical flow for registration
    nr, nc = img.shape
    row_coords, col_coords = np.meshgrid(np.arange(nr), np.arange(nc),
                                        indexing='ij')

    img_warp = warp(img, np.array([row_coords + v, col_coords + u]),
                    mode='edge')

    return np.abs(img_prev - img_warp)