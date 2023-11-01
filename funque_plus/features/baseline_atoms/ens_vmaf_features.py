import numpy as np
from scipy import ndimage
from ..funque_atoms.gsm_utils import gsm_model
from ..funque_atoms.rred_utils import rred_entropies_and_scales
from . import vmaf_features


def speed(img_ref, img_dis, img_ref_prev, img_dis_prev, block_size=5):
    img_ref_ms = img_ref - ndimage.gaussian_filter(img_ref, 7/6, truncate=3) 
    img_dis_ms = img_dis - ndimage.gaussian_filter(img_dis, 7/6, truncate=3) 

    entropies_ref, scales_ref = rred_entropies_and_scales(img_ref_ms, block_size=block_size)
    entropies_dis, scales_dis = rred_entropies_and_scales(img_dis_ms, block_size=block_size)

    s_speed = np.mean(np.abs(scales_ref*entropies_ref - scales_dis*entropies_dis))

    if img_ref_prev is None or img_dis_prev is None:
        t_speed = 0
    else:
        img_ref_diff_ms = img_ref_ms - (img_ref_prev - ndimage.gaussian_filter(img_ref_prev, 7/6, truncate=3))
        img_dis_diff_ms = img_dis_ms - (img_dis_prev - ndimage.gaussian_filter(img_dis_prev, 7/6, truncate=3))

        entropies_ref_diff, scales_ref_diff = rred_entropies_and_scales(img_ref_diff_ms, block_size=block_size)
        entropies_dis_diff, scales_dis_diff = rred_entropies_and_scales(img_dis_diff_ms, block_size=block_size)

        t_speed = np.mean(np.abs(scales_ref*scales_ref_diff*entropies_ref_diff - scales_dis*scales_dis_diff*entropies_dis_diff))

    return s_speed, t_speed


def t_speed(img_ref, img_dis, img_ref_prev, img_dis_prev, block_size=5):
    img_ref_ms = img_ref - ndimage.gaussian_filter(img_ref, 7/6, truncate=3) 
    img_dis_ms = img_dis - ndimage.gaussian_filter(img_dis, 7/6, truncate=3) 

    _, scales_ref = rred_entropies_and_scales(img_ref_ms, block_size=block_size)
    _, scales_dis = rred_entropies_and_scales(img_dis_ms, block_size=block_size)

    if img_ref_prev is None or img_dis_prev is None:
        t_speed = 0
    else:
        img_ref_diff_ms = img_ref_ms - (img_ref_prev - ndimage.gaussian_filter(img_ref_prev, 7/6, truncate=3))
        img_dis_diff_ms = img_dis_ms - (img_dis_prev - ndimage.gaussian_filter(img_dis_prev, 7/6, truncate=3))

        entropies_ref_diff, scales_ref_diff = rred_entropies_and_scales(img_ref_diff_ms, block_size=block_size)
        entropies_dis_diff, scales_dis_diff = rred_entropies_and_scales(img_dis_diff_ms, block_size=block_size)

        t_speed = np.mean(np.abs(scales_ref*scales_ref_diff*entropies_ref_diff - scales_dis*scales_dis_diff*entropies_dis_diff))

    return t_speed


def s_speed(img_ref, img_dis, block_size=5):
    img_ref_ms = img_ref - ndimage.gaussian_filter(img_ref, 7/6, truncate=3) 
    img_dis_ms = img_dis - ndimage.gaussian_filter(img_dis, 7/6, truncate=3) 

    entropies_ref, scales_ref = rred_entropies_and_scales(img_ref_ms, block_size=block_size)
    entropies_dis, scales_dis = rred_entropies_and_scales(img_dis_ms, block_size=block_size)

    s_speed = np.mean(np.abs(scales_ref*entropies_ref - scales_dis*entropies_dis))

    return s_speed


def t_vif(img_ref, img_dis, img_ref_prev, img_dis_prev, kernel):
    if img_ref_prev is None or img_dis_prev is None:
        return 0
    return vmaf_features.vif(img_ref - img_ref_prev, img_dis - img_dis_prev, kernel)