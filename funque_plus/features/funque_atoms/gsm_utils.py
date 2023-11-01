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


def gsm_model(y, M):
    tol = 1e-15
    y_size = (int(y.shape[0]/M)*M, int(y.shape[1]/M)*M)
    y = y[:y_size[0], :y_size[1]]

    y_vecs = im2col(y, M, 1)
    cov = np.cov(y_vecs)
    lamda, V = np.linalg.eigh(cov)
    lamda[lamda < tol] = tol
    cov = V@np.diag(lamda)@V.T

    y_vecs = im2col(y, M, M)

    s = np.linalg.inv(cov)@y_vecs
    s = np.sum(s * y_vecs, 0)/(M*M)
    s = np.clip(s.reshape((int(y_size[0]/M), int(y_size[1]/M))), tol, None)

    return s, lamda, cov


def complex_gsm_model(y, M):
    tol = 1e-15
    y_size = (int(y.shape[0]/M)*M, int(y.shape[1]/M)*M)
    y = y[:y_size[0], :y_size[1]]

    y_vecs = im2col(y, M, 1)
    _, num_samples = y_vecs.shape
    mu = np.expand_dims(np.mean(y_vecs, -1), -1)
    y_ms = y_vecs - mu

    cov = (y_ms @ y_ms.conj().T) / num_samples
    rel = (y_ms @ y_ms.T) / num_samples

    lamda, V = np.linalg.eigh(cov)
    lamda[lamda < tol] = tol
    # lamda_cov_all.append(lamda)
    cov = V@np.diag(lamda)@V.T
    cov_inv = np.linalg.inv(cov)

    U, lamda, V_h = np.linalg.svd(rel)
    lamda[lamda < tol] = tol
    # lamda_rel_all.append(lamda)
    rel = U@np.diag(lamda)@V_h

    y_vecs = im2col(y, M, M)

    scaled_vecs = y_vecs.T @ np.linalg.pinv(cov.conj() - rel.conj() @ cov_inv @ rel, hermitian=True)
    rsq = (np.real(np.sum(scaled_vecs * y_vecs.conj().T, 1)) - np.abs(np.sum(scaled_vecs * ((rel.conj() @ cov_inv) @ y_vecs).T, 1))) / (M*M)
    rsq = np.clip(rsq.reshape((int(y_size[0]/M), int(y_size[1]/M))), tol, None)

    return rsq, cov, rel