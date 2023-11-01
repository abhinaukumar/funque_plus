import numpy as np
import scipy as sp

from pywt import wavedec2

from ..funque_atoms import dlm_utils
from ..funque_atoms import pyr_features
from ..funque_atoms.filter_utils import filter_pyr


def vif(img_ref, img_dist, kernel):
    sigma_nsq = 0.1

    mu_x = sp.ndimage.convolve1d(sp.ndimage.convolve1d(img_ref, kernel, 0), kernel, 1)
    mu_y = sp.ndimage.convolve1d(sp.ndimage.convolve1d(img_dist, kernel, 0), kernel, 1)
    mu2_x = sp.ndimage.convolve1d(sp.ndimage.convolve1d(img_ref*img_ref, kernel, 0), kernel, 1)
    mu2_y = sp.ndimage.convolve1d(sp.ndimage.convolve1d(img_dist*img_dist, kernel, 0), kernel, 1)
    mu_xy = sp.ndimage.convolve1d(sp.ndimage.convolve1d(img_ref*img_dist, kernel, 0), kernel, 1)

    var_x = mu2_x - mu_x*mu_x
    var_y = mu2_y - mu_y*mu_y
    cov_xy = mu_xy - mu_x*mu_y

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

    vif_val = np.sum(np.log(1 + g*g * var_x / (sv_sq + sigma_nsq)) + 1e-4)/np.sum(np.log(1 + var_x / sigma_nsq) + 1e-4)
    return vif_val


# Masks pyr_1 using pyr_2
def vmaf_dlm_contrast_mask_one_way(pyr_1, pyr_2):
    kernel = np.array([[1, 1, 1], [1, 2, 1], [1, 1, 1]])

    n_levels = len(pyr_1)
    masked_pyr = []
    for level in range(n_levels):
        masking_threshold = 0
        for i in range(3):
            masking_signal = np.abs(pyr_2[level][i]) / 30
            masking_threshold += sp.signal.convolve2d(masking_signal, kernel, mode='same')
        masked_level = []
        for i in range(3):
            masked_level.append(np.clip(np.abs(pyr_1[level][i]) - masking_threshold, 0, None))
        masked_pyr.append(tuple(masked_level))
    return masked_pyr


def dlm(img_ref, img_dist, wavelet='db2', border_size=0.2, csf='watson'):
    n_levels = 4

    pyr_ref = pyr_features.custom_wavedec2(img_ref, wavelet, 'periodization', n_levels)
    pyr_dist = pyr_features.custom_wavedec2(img_dist, wavelet, 'periodization', n_levels)

    # Ignore approximation coefficients
    approxs_ref, details_ref = pyr_ref
    approcs_dist, details_dist = pyr_dist

    details_rest = []
    details_add = []
    for level_ref, level_dist in zip(details_ref, details_dist):
        level_rest, level_add = dlm_utils.dlm_decouple(level_ref, level_dist)
        details_rest.append(level_rest)
        details_add.append(level_add)

    pyr_rest = (None, details_rest)
    pyr_add = (None, details_add)

    pyr_ref = filter_pyr(pyr_ref, csf)[1]
    pyr_rest = filter_pyr(pyr_rest, csf)[1]
    pyr_add = filter_pyr(pyr_add, csf)[1]

    pyr_rest = vmaf_dlm_contrast_mask_one_way(pyr_rest, pyr_add)

    # Flatten into a list of subbands for convenience
    pyr_ref = [item for sublist in pyr_ref for item in sublist]
    pyr_rest = [item for sublist in pyr_rest for item in sublist]
    pyr_add = [item for sublist in pyr_add for item in sublist]

    # Pool results
    dlm_num = 0
    dlm_den = 0
    for subband in pyr_rest:
        h, w = subband.shape
        border_h = int(border_size*h)
        border_w = int(border_size*w)
        dlm_num += np.power(np.sum(np.power(subband[border_h:-border_h, border_w:-border_w], 3.0)), 1.0/3)
    for subband in pyr_ref:
        h, w = subband.shape
        border_h = int(border_size*h)
        border_w = int(border_size*w)
        dlm_den += np.power(np.sum(np.power(np.abs(subband[border_h:-border_h, border_w:-border_w]), 3.0)), 1.0/3)

    dlm_ret = (dlm_num + 1e-4) / (dlm_den + 1e-4)

    return dlm_ret


def motion(img_ref, img_dist, kernel):
    if img_ref is None or img_dist is None:
        return 0
    mu_x = sp.ndimage.convolve1d(sp.ndimage.convolve1d(img_ref, kernel, 0), kernel, 1)
    mu_y = sp.ndimage.convolve1d(sp.ndimage.convolve1d(img_dist, kernel, 0), kernel, 1)
    return np.mean(np.abs(mu_x - mu_y))
