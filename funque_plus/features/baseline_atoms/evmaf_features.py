import numpy as np
from ..funque_atoms.pyr_features import custom_wavedec2
from ..funque_atoms.dlm_utils import dlm_decouple, integral_image_sums
from ..funque_atoms.filter_utils import filter_pyr
from .flow_utils import optical_flow


# Masks level_2 using level_1
def new_dlm_contrast_mask_one_way(dtf, exps, level_1, level_2):
    ret_single = False
    if not isinstance(exps, (list, tuple)):
        ret_single = True
        exps = [exps]
    masking_threshold_base = 0
    for subband in level_1:
        masking_signal = np.abs(subband)
        masking_threshold_base += (np.clip(integral_image_sums(masking_signal, 3), 0, None) + masking_signal) / 30
    masking_thresholds = [masking_threshold_base / (1 + dtf)**exp for exp in exps]
    masked_levels = [tuple([np.clip(np.abs(subband) - masking_threshold, 0, None) for subband in level_2]) for masking_threshold in masking_thresholds]
    if ret_single:
        return masked_levels[0]
    else:
        return masked_levels


# Pyr ref and pyr dis were obtained using Db2 DWT
def e_dlm_pyr(pyr_dtf, pyr_ref, pyr_dist, exps, border_size=0.2, csf='watson'):
    if not isinstance(exps, (list, tuple)):
        raise TypeError('exps must be of type list or tuple')
    # Pyramids are assumed to have the structure
    # ([A1, ..., An], [(H1, V1, D1), ..., (Hn, Vn, Dn)])
    _, details_ref = pyr_ref
    _, details_dist = pyr_dist
    assert len(details_ref) == len(details_dist), 'Pyramids must be of equal height.'
    n_levels = len(details_ref)

    pyrs_decouple = [dlm_decouple(level_ref, level_dist) for level_ref, level_dist in zip(details_ref, details_dist)]
    pyr_rest = [level[0] for level in pyrs_decouple]
    pyr_add = [level[1] for level in pyrs_decouple]

    # Below this point, pyramids have the structure
    # [(H1, V1, D1), ..., (Hn, Vn, Dn)])]
    _, details_ref = filter_pyr((None, details_ref), csf)
    _, pyr_rest = filter_pyr((None, pyr_rest), csf)
    _, pyr_add = filter_pyr((None, pyr_add), csf)

    dtfs = [np.sum(np.abs(np.stack(level_dtf, axis=-1)), -1) for level_dtf in pyr_dtf[1]]
    pyr_rest_masked_all = [new_dlm_contrast_mask_one_way(dtf, exps, level_add, level_rest) for level_rest, level_add, dtf in zip(pyr_rest, pyr_add, dtfs)]

    # pool results
    dlm_numses = [np.ones((n_levels,))*1e-4 for _ in exps]

    for i, level in enumerate(pyr_rest_masked_all):
        for level_exp, dlm_nums in zip(level, dlm_numses):
            h, w = level_exp[0].shape
            border_h = int(border_size*h)
            border_w = int(border_size*w)
            for subband in level_exp:
                dlm_nums[i] += np.power(np.sum(np.power(subband[border_h:-border_h, border_w:-border_w], 3.0)), 1.0/3)

    dlm_dens = np.ones((n_levels,))*1e-4
    for i, level in enumerate(details_ref):
        h, w = level[0].shape
        border_h = int(border_size*h)
        border_w = int(border_size*w)
        for subband in level:
            dlm_dens[i] += np.power(np.sum(np.power(np.abs(subband[border_h:-border_h, border_w:-border_w]), 3.0)), 1.0/3)

    return [np.sum(dlm_nums) / np.sum(dlm_dens) for dlm_nums in dlm_numses]


# Pyr ref and pyr dis were obtained using Db2 DWT
def approx_e_dlm_pyr(pyr_dtf, pyr_ref, pyr_dist, exps, border_size=0.2, csf='watson'):
    if not isinstance(exps, (list, tuple)):
        raise TypeError('exps must be of type list or tuple')
    # Pyramids are assumed to have the structure
    # ([A1, ..., An], [(H1, V1, D1), ..., (Hn, Vn, Dn)])
    _, details_ref = pyr_ref
    _, details_dist = pyr_dist
    assert len(details_ref) == len(details_dist), 'Pyramids must be of equal height.'
    n_levels = len(details_ref)

    pyrs_decouple = [dlm_decouple(level_ref, level_dist) for level_ref, level_dist in zip(details_ref, details_dist)]
    pyr_rest = [level[0] for level in pyrs_decouple]
    pyr_add = [level[1] for level in pyrs_decouple]

    # Below this point, pyramids have the structure
    # [(H1, V1, D1), ..., (Hn, Vn, Dn)])]
    _, details_ref = filter_pyr((None, details_ref), csf)
    _, pyr_rest = filter_pyr((None, pyr_rest), csf)
    _, pyr_add = filter_pyr((None, pyr_add), csf)

    dtfs = [np.abs(dtf) for dtf in pyr_dtf[0]]
    pyr_rest_masked_all = [new_dlm_contrast_mask_one_way(dtf, exps, level_add, level_rest) for level_rest, level_add, dtf in zip(pyr_rest, pyr_add, dtfs)]

    # pool results
    dlm_numses = [np.ones((n_levels,))*1e-4 for _ in exps]

    for i, level in enumerate(pyr_rest_masked_all):
        for level_exp, dlm_nums in zip(level, dlm_numses):
            h, w = level_exp[0].shape
            border_h = int(border_size*h)
            border_w = int(border_size*w)
            for subband in level_exp:
                dlm_nums[i] += np.power(np.sum(np.power(subband[border_h:-border_h, border_w:-border_w], 3.0)), 1.0/3)

    dlm_dens = np.ones((n_levels,))*1e-4
    for i, level in enumerate(details_ref):
        h, w = level[0].shape
        border_h = int(border_size*h)
        border_w = int(border_size*w)
        for subband in level:
            dlm_dens[i] += np.power(np.sum(np.power(np.abs(subband[border_h:-border_h, border_w:-border_w]), 3.0)), 1.0/3)

    return [np.sum(dlm_nums) / np.sum(dlm_dens) for dlm_nums in dlm_numses]

