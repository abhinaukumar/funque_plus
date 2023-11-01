import numpy as np
from .vif_utils import integral_image


def integral_image_sums(x, k, stride=1):
    x_pad = np.pad(x, int((k - stride)/2), mode='reflect')
    int_x = integral_image(x_pad)
    ret = (int_x[:-k:stride, :-k:stride] - int_x[:-k:stride, k::stride] - int_x[k::stride, :-k:stride] + int_x[k::stride, k::stride])
    return ret


def dlm_decouple(level_ref, level_dist):
    eps = 1e-30
    psi_ref = np.arctan(level_ref[1] / (level_ref[0] + eps)) + np.pi*(level_ref[0] <= 0)
    psi_dist = np.arctan(level_dist[1] / (level_dist[0] + eps)) + np.pi*(level_dist[0] <= 0)
    psi_diff = 180*np.abs(psi_ref - psi_dist)/np.pi
    mask = (psi_diff < 1)

    level_rest = []
    level_add = []
    for subband_ref, subband_dist in zip(level_ref, level_dist):
        k = np.clip(subband_dist / (subband_ref + eps), 0.0, 1.0)
        level_rest.append(k * subband_ref)
        level_rest[-1][mask] = subband_dist[mask]
        level_add.append(subband_dist - level_rest[-1])
    level_rest = tuple(level_rest)
    level_add = tuple(level_add)

    return level_rest, level_add


# Masks level_2 using level_1
def dlm_contrast_mask_one_way(level_1, level_2):
    masking_threshold = 0
    for subband in level_1:
        masking_signal = np.abs(subband)
        masking_threshold += (np.clip(integral_image_sums(masking_signal, 3), 0, None) + masking_signal) / 30
    masked_level = tuple([np.clip(np.abs(subband) - masking_threshold, 0, None) for subband in level_2])
    return masked_level


# Masks each pyramid using the other
def dlm_contrast_mask(level_1, level_2):
    masked_level_2 = dlm_contrast_mask_one_way(level_1, level_2)
    masked_level_1 = dlm_contrast_mask_one_way(level_2, level_1)
    return masked_level_1, masked_level_2
