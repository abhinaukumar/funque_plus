import numpy as np

from .dlm_utils import dlm_decouple, dlm_contrast_mask
from .vif_utils import vif_spatial, vif_channel_est
from .gsm_utils import gsm_model, im2col
from .filter_utils import filter_pyr
from .rred_utils import rred_entropies_and_scales


from pywt import dwt2


def custom_wavedec2(data, wavelet, mode='symmetric', level=None, axes=(-2, -1)):
    approxs = []
    details = []
    if level is None:
        level = 1
    for _ in range(level):
        wavelet_level = dwt2(data, wavelet, mode, axes)
        approxs.append(wavelet_level[0])
        details.append(wavelet_level[1])
        data = wavelet_level[0]
    return (approxs, details)


def dlm_pyr(pyr_ref, pyr_dist, border_size=0.2, csf='li'):
    # Pyramids are assumed to have the structure
    # ([A1, ..., An], [(H1, V1, D1), ..., (Hn, Vn, Dn)])
    _, details_ref = pyr_ref
    _, details_dist = pyr_dist
    assert len(details_ref) == len(details_dist), 'Pyramids must be of equal height.'
    pyrs_decouple = [dlm_decouple(level_ref, level_dist) for level_ref, level_dist in zip(details_ref, details_dist)]
    pyr_rest = [level[0] for level in pyrs_decouple]
    pyr_add = [level[1] for level in pyrs_decouple]

    # Below this point, pyramids have the structure
    # [(H1, V1, D1), ..., (Hn, Vn, Dn)])]
    _, details_ref = filter_pyr((None, details_ref), csf)
    _, pyr_rest = filter_pyr((None, pyr_rest), csf)
    _, pyr_add = filter_pyr((None, pyr_add), csf)

    pyrs_masked = [dlm_contrast_mask(level_rest, level_add) for level_rest, level_add in zip(pyr_rest, pyr_add)]
    pyr_rest = [level[0] for level in pyrs_masked]
    # pyr_add = [level[1] for level in pyrs_masked]

    # pool results
    dlm_num = 0
    dlm_den = 0
    for level in pyr_rest:
        h, w = level[0].shape
        border_h = int(border_size*h)
        border_w = int(border_size*w)
        for subband in level:
            dlm_num += np.power(np.sum(np.power(subband[border_h:-border_h, border_w:-border_w], 3.0)), 1.0/3)

    for level in details_ref:
        h, w = level[0].shape
        border_h = int(border_size*h)
        border_w = int(border_size*w)
        for subband in level:
            dlm_den += np.power(np.sum(np.abs(np.power(subband[border_h:-border_h, border_w:-border_w], 3.0))), 1.0/3)

    dlm = (dlm_num + 1e-4) / (dlm_den + 1e-4)

    return dlm


def ms_dlm_pyr(pyr_ref, pyr_dist, border_size=0.2, full=False, csf='li'):
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
    details_ref = filter_pyr(details_ref, csf)
    pyr_rest = filter_pyr(pyr_rest, csf)
    pyr_add = filter_pyr(pyr_add, csf)

    pyrs_masked = [dlm_contrast_mask(level_rest, level_add) for level_rest, level_add in zip(pyr_rest, pyr_add)]
    pyr_rest = [level[0] for level in pyrs_masked]
    # pyr_add = [level[1] for level in pyrs_masked]

    # pool results
    dlm_nums = np.ones((n_levels,))*1e-4
    for i, level in enumerate(pyr_rest):
        h, w = level[0].shape
        border_h = int(border_size*h)
        border_w = int(border_size*w)
        for subband in level:
            dlm_nums[i] += np.power(np.sum(np.power(subband[border_h:-border_h, border_w:-border_w], 3.0)), 1.0/3)

    dlm_dens = np.ones((n_levels,))*1e-4
    for i, level in enumerate(details_ref):
        h, w = level[0].shape
        border_h = int(border_size*h)
        border_w = int(border_size*w)
        for subband in level:
            dlm_dens[i] += np.power(np.sum(np.power(np.abs(subband[border_h:-border_h, border_w:-border_w]), 3.0)), 1.0/3)

    if full:
        return np.cumsum(dlm_nums) / np.cumsum(dlm_dens), dlm_nums / dlm_dens
    else:
        return np.cumsum(dlm_nums) / np.cumsum(dlm_dens)


def vif_pyr(pyr_ref, pyr_dist, full=False, block_size=3, sigma_nsq=None):
    # Pyramids are assumed to have the structure
    # ([A1, ..., An], [(H1, V1, D1), ..., (Hn, Vn, Dn)])
    approxs_ref, details_ref = pyr_ref
    approxs_dist, details_dist = pyr_dist
    n_levels = len(approxs_ref)

    nums = np.ones((n_levels,))*1e-4
    dens = np.ones((n_levels,))*1e-4
    approx_nums = np.ones((n_levels,))*1e-4
    approx_dens = np.ones((n_levels,))*1e-4

    if block_size == 1:
        if sigma_nsq is None:
            sigma_nsq = 5.0
        for lev, (approx_ref, approx_dist, detail_ref, detail_dist) in enumerate(zip(approxs_ref, approxs_dist, details_ref, details_dist)):
            for subband_ref, subband_dist in zip(detail_ref[:-1], detail_dist[:-1]):
                num, den, _ = vif_spatial(subband_ref, subband_dist, k=9, sigma_nsq=sigma_nsq, full=True)
                nums[lev] += num
                dens[lev] += den

            num, den, _ = vif_spatial(approx_ref, approx_dist, k=9, sigma_nsq=sigma_nsq, full=True)
            approx_nums[lev] = num
            approx_dens[lev] = den
    else:
        if sigma_nsq is None:
            sigma_nsq = 0.1
        channel_details = []
        channel_approxs = []
        for lev, (approx_ref, approx_dist, detail_level_ref, detail_level_dist) in enumerate(zip(approxs_ref, approxs_dist, details_ref, details_dist)):
            # winsize = 2**(n_levels-lev) + 1
            winsize = 2**(lev+1) + 1
            channel_details.append(tuple([vif_channel_est(subband_ref, subband_dist, winsize, block_size) for subband_ref, subband_dist in zip(detail_level_ref[:-1], detail_level_dist[:-1])]))
            channel_approxs.append(vif_channel_est(approx_ref, approx_dist, winsize, block_size))

        gsm_details = []
        gsm_approxs = []
        for approx_ref, detail_level_ref in zip(approxs_ref, details_ref):
            gsm_details.append([gsm_model(subband_ref, block_size) for subband_ref in detail_level_ref[:-1]])
            gsm_approxs.append(gsm_model(approx_ref, block_size))

        for lev, (level_channel, level_gsm) in enumerate(zip(channel_details, gsm_details)):
            offset = int(np.ceil(2**lev/block_size))
            for (g, sigma_vsq), (s, lamda, _) in zip(level_channel, level_gsm):
                g = g[offset:-offset, offset:-offset]
                sigma_vsq = sigma_vsq[offset:-offset, offset:-offset]
                s = s[offset:-offset, offset:-offset]
                for j in range(block_size**2):
                    nums[lev] += np.mean(np.log(1 + g*g*s*lamda[j]/(sigma_vsq+sigma_nsq)))
                    dens[lev] += np.mean(np.log(1 + s*lamda[j]/sigma_nsq))

        for lev, ((g_approx, sigma_vsq_approx), (s_approx, lamda, _)) in enumerate(zip(channel_approxs, gsm_approxs)):
            offset = int(np.ceil(2**lev/block_size))
            g = g_approx[offset:-offset, offset:-offset]
            sigma_vsq = sigma_vsq_approx[offset:-offset, offset:-offset]
            s = s_approx[offset:-offset, offset:-offset]
            for j in range(block_size**2):
                approx_nums[lev] += np.mean(np.log(1 + g*g*s*lamda[j]/(sigma_vsq+sigma_nsq)))
                approx_dens[lev] += np.mean(np.log(1 + s*lamda[j]/sigma_nsq))

    vif_vals = np.cumsum(nums) / np.cumsum(dens)
    vif_approx_vals = approx_nums / approx_dens
    if not full:
        return vif_vals, vif_approx_vals
    else:
        return (vif_vals, vif_approx_vals), ((nums, dens), (approx_nums, approx_dens))


def ssim_pyr(pyr_ref, pyr_dist, max_val=1, K1=0.01, K2=0.03, pool='cov'):
    # Pyramids are assumed to have the structure
    # ([A1, ..., An], [(H1, V1, D1), ..., (Hn, Vn, Dn)])
    approxs_ref, details_ref = pyr_ref
    approxs_dist, details_dist = pyr_dist
    assert len(approxs_ref) == len(approxs_dist), 'Both wavelet pyramids must be of the same height'
    n_levels = len(approxs_ref)

    C1 = (K1*max_val)**2
    C2 = (K2*max_val)**2

    var_x = np.zeros((details_ref[0][0].shape[0] << 1, details_ref[0][0].shape[1] << 1))
    var_y = np.zeros((details_ref[0][0].shape[0] << 1, details_ref[0][0].shape[1] << 1))
    cov_xy = np.zeros((details_ref[0][0].shape[0] << 1, details_ref[0][0].shape[1] << 1))

    for detail_level_ref, detail_level_dist in zip(details_ref, details_dist):
        var_x_add = np.stack([subband**2 for subband in detail_level_ref], axis=-1).sum(-1)
        var_y_add = np.stack([subband**2 for subband in detail_level_dist], axis=-1).sum(-1)
        cov_xy_add = np.stack([subband_ref * subband_dist for subband_ref, subband_dist in zip(detail_level_ref, detail_level_dist)], axis=-1).sum(-1)
        var_x = im2col(var_x, 2, 2).sum(0).reshape(var_x_add.shape) + var_x_add
        var_y = im2col(var_y, 2, 2).sum(0).reshape(var_y_add.shape) + var_y_add
        cov_xy = im2col(cov_xy, 2, 2).sum(0).reshape(cov_xy_add.shape) + cov_xy_add

    win_dim = (1 << n_levels)  # 2^L
    win_size = (1 << (n_levels << 1))  # 2^(2L), i.e., a win_dim X win_dim square

    mu_x = approxs_ref[-1] / win_dim
    mu_y = approxs_dist[-1] / win_dim
    var_x /= win_size
    var_y /= win_size
    cov_xy /= win_size

    l = (2*mu_x*mu_y + C1) / (mu_x**2 + mu_y**2 + C1)
    cs = (2 * cov_xy + C2) / (var_x + var_y + C2)

    ssim_map = l * cs
    mean_ssim = np.mean(ssim_map)

    if pool == 'mean':
        return mean_ssim
    elif pool == 'cov':
        return np.std(ssim_map) / mean_ssim
    elif pool == 'all':
        return mean_ssim, np.std(ssim_map) / mean_ssim
    else:
        raise ValueError('Invalid pool option.')


def ms_ssim_pyr(pyr_ref, pyr_dist, max_val=1, K1=0.01, K2=0.03, pool='cov', full=False):
    # Pyramids are assumed to have the structure
    # ([A1, ..., An], [(H1, V1, D1), ..., (Hn, Vn, Dn)])
    approxs_ref, details_ref = pyr_ref
    approxs_dist, details_dist = pyr_dist

    assert len(details_ref) == len(details_dist), 'Both wavelet pyramids must be of the same height'
    n_levels = len(details_ref)
    assert n_levels <= 5, 'Exponents are defined only for 5 scales'
    assert pool in ['mean', 'cov', 'all'], 'pool must be one of \'mean\', \'cov\', or \'all\''
    exps = np.array([0.0448, 0.2856, 0.3001, 0.2363, 0.1333])

    l_mean_scales = np.zeros((n_levels,))
    cs_mean_scales = np.zeros((n_levels,))
    ssim_mean_scales = np.zeros((n_levels,))
    l_cov_scales = np.zeros((n_levels,))
    cs_cov_scales = np.zeros((n_levels,))
    ssim_cov_scales = np.zeros((n_levels,))
    l_mink_scales = np.zeros((n_levels,))
    cs_mink_scales = np.zeros((n_levels,))
    ssim_mink_scales = np.zeros((n_levels,))

    C1 = (K1*max_val)**2
    C2 = (K2*max_val)**2

    var_x = np.zeros((details_ref[0][0].shape[0] << 1, details_ref[0][0].shape[1] << 1))
    var_y = np.zeros((details_ref[0][0].shape[0] << 1, details_ref[0][0].shape[1] << 1))
    cov_xy = np.zeros((details_ref[0][0].shape[0] << 1, details_ref[0][0].shape[1] << 1))

    win_dim = 1
    win_size = 1
    for lev, (approx_ref, approx_dist, detail_level_ref, detail_level_dist) in enumerate(zip(approxs_ref, approxs_dist, details_ref, details_dist)):
        win_dim <<= 1
        win_size <<= 2

        var_x_add = np.stack([subband**2 for subband in detail_level_ref], axis=-1).sum(-1)
        var_y_add = np.stack([subband**2 for subband in detail_level_dist], axis=-1).sum(-1)
        cov_xy_add = np.stack([subband_ref * subband_dist for subband_ref, subband_dist in zip(detail_level_ref, detail_level_dist)], axis=-1).sum(-1)

        var_x = im2col(var_x, 2, 2).mean(0).reshape(var_x_add.shape) + var_x_add / win_size
        var_y = im2col(var_y, 2, 2).mean(0).reshape(var_y_add.shape) + var_y_add / win_size
        cov_xy = im2col(cov_xy, 2, 2).mean(0).reshape(cov_xy_add.shape) + cov_xy_add / win_size

        mu_x = approx_ref / win_dim
        mu_y = approx_dist / win_dim

        l = (2*mu_x*mu_y + C1) / (mu_x**2 + mu_y**2 + C1)
        cs = (2 * cov_xy + C2) / (var_x + var_y + C2)
        ssim_map = l * cs

        l_mean_scales[lev] = np.mean(l)
        cs_mean_scales[lev] = np.mean(cs)
        l_cov_scales[lev] = np.std(l) / l_mean_scales[lev]
        cs_cov_scales[lev] = np.std(cs) / cs_mean_scales[lev]
        l_mink_scales[lev] = 1 - np.mean((1 - l)**3)**(1.0/3)
        cs_mink_scales[lev] = 1 - np.mean((1 - cs)**3)**(1.0/3)
        ssim_mean_scales[lev] = np.mean(ssim_map)
        ssim_cov_scales[lev] = np.std(ssim_map) / ssim_mean_scales[lev]
        ssim_mink_scales[lev] = 1 - np.mean((1 - ssim_map)**3)**(1.0/3)
    
    if pool in ['mean', 'all']:
        ms_ssim_mean_scales = np.concatenate([np.array([1]), np.cumprod(np.sign(cs_mean_scales[:-1]) * np.abs(cs_mean_scales[:-1]) ** exps[:n_levels-1])]) * (np.sign(ssim_mean_scales) * np.abs(ssim_mean_scales) ** exps[:n_levels])
    if pool in ['cov', 'all']:
        ms_ssim_cov_scales = np.concatenate([np.array([1]), np.cumprod(np.sign(cs_cov_scales[:-1]) * np.abs(cs_cov_scales[:-1]) ** exps[:n_levels-1])]) * (np.sign(ssim_cov_scales) * np.abs(ssim_cov_scales) ** exps[:n_levels])
    if pool in ['mink', 'all']:
        ms_ssim_mink_scales = np.concatenate([np.array([1]), np.cumprod(np.sign(cs_mink_scales[:-1]) * np.abs(cs_mink_scales[:-1]) ** exps[:n_levels-1])]) * (np.sign(ssim_mink_scales) * np.abs(ssim_mink_scales) ** exps[:n_levels])

    ret_mean = tuple()
    ret_cov = tuple()
    ret_mink = tuple()
    if pool in ['mean', 'all']:
        ret_mean = ret_mean + (ms_ssim_mean_scales, ssim_mean_scales)
        if full:
            ret_mean = ret_mean + (l_mean_scales, cs_mean_scales)
    if pool in ['cov', 'all']:
        ret_cov = ret_cov + (ms_ssim_cov_scales, ssim_cov_scales)
        if full:
            ret_cov = ret_cov + (l_cov_scales, cs_cov_scales)
    if pool in ['mink', 'all']:
        ret_mink = ret_mink + (ms_ssim_mink_scales, ssim_mink_scales)
        if full:
            ret_mink = ret_mink + (l_mink_scales, cs_mink_scales)

    if pool == 'mean':
        return ret_mean
    elif pool == 'cov':
        return ret_cov
    elif pool == 'mink':
        return ret_mink
    elif pool == 'all':
        return (ret_mean, ret_cov, ret_mink)


def strred_pyr(pyr_ref, pyr_dist, prev_pyr_ref, prev_pyr_dist, block_size=3, single=False, full=False):
    # Pyramids are assumed to have the structure
    # ([A1, ..., An], [(H1, V1, D1), ..., (Hn, Vn, Dn)])
    approxs_ref, details_ref = pyr_ref
    approxs_dist, details_dist = pyr_dist
    assert len(details_ref) == len(details_dist), 'Both wavelet pyramids must be of the same height'
    n_levels = len(details_ref)
    spat_gsm_ref_details = [tuple([rred_entropies_and_scales(subband, block_size) for subband in level]) for level in details_ref]
    spat_gsm_dist_details = [tuple([rred_entropies_and_scales(subband, block_size) for subband in level]) for level in details_dist]
    spat_gsm_ref_approxs = [rred_entropies_and_scales(subband, block_size) for subband in approxs_ref]
    spat_gsm_dist_approxs = [rred_entropies_and_scales(subband, block_size) for subband in approxs_dist]
    compute_temporal = (prev_pyr_ref is not None and prev_pyr_dist is not None)
    if compute_temporal:
        prev_approxs_ref, prev_details_ref = prev_pyr_ref
        prev_approxs_dist, prev_details_dist = prev_pyr_dist
        temp_gsm_ref_details = [tuple([rred_entropies_and_scales(subband - prev_subband, block_size) for subband, prev_subband in zip(level, prev_level)])
                                for level, prev_level in zip(details_ref, prev_details_ref)]
        temp_gsm_dist_details = [tuple([rred_entropies_and_scales(subband - prev_subband, block_size) for subband, prev_subband in zip(level, prev_level)])
                                 for level, prev_level in zip(details_dist, prev_details_dist)]
        temp_gsm_ref_approxs = [rred_entropies_and_scales(subband - prev_subband, block_size) for subband, prev_subband in zip(approxs_ref, prev_approxs_ref)]
        temp_gsm_dist_approxs = [rred_entropies_and_scales(subband - prev_subband, block_size) for subband, prev_subband in zip(approxs_dist, prev_approxs_dist)]

    agg = lambda x: np.abs(np.mean(x)) if single else np.mean(np.abs(x))

    spat_vals = np.array([
        np.mean([agg(scale_ref * entropy_ref - scale_dist * entropy_dist) for (entropy_ref, scale_ref), (entropy_dist, scale_dist) in zip(level_ref, level_dist)])
        for level_ref, level_dist in zip(spat_gsm_ref_details, spat_gsm_dist_details)
    ])
    spat_approx_vals = np.array([
        agg(scale_ref * entropy_ref - scale_dist * entropy_dist) for (entropy_ref, scale_ref), (entropy_dist, scale_dist) in zip(spat_gsm_ref_approxs, spat_gsm_dist_approxs)
    ])

    if compute_temporal:
        temp_vals = np.array([
            np.mean([
                agg(spat_scale_ref * temp_scale_ref * entropy_ref - spat_scale_dist * temp_scale_dist * entropy_dist)
                for (_, spat_scale_ref), (_, spat_scale_dist), (entropy_ref, temp_scale_ref), (entropy_dist, temp_scale_dist)
                in zip(spat_level_ref, spat_level_dist, temp_level_ref, temp_level_dist)
            ])
            for spat_level_ref, spat_level_dist, temp_level_ref, temp_level_dist in zip(spat_gsm_ref_details, spat_gsm_dist_details, temp_gsm_ref_details, temp_gsm_dist_details)
        ])
        temp_approx_vals = np.array([
            agg(spat_scale_ref * temp_scale_ref * entropy_ref - spat_scale_dist * temp_scale_dist * entropy_dist)
            for (_, spat_scale_ref), (_, spat_scale_dist), (entropy_ref, temp_scale_ref), (entropy_dist, temp_scale_dist)
            in zip(spat_gsm_ref_approxs, spat_gsm_dist_approxs, temp_gsm_ref_approxs, temp_gsm_dist_approxs)
        ])
        spat_temp_vals = spat_vals * temp_vals
        spat_temp_approx_vals = spat_approx_vals * temp_approx_vals
    else:
        temp_vals = np.zeros_like(spat_vals)
        temp_approx_vals = np.zeros_like(spat_approx_vals)
        spat_temp_vals = np.zeros_like(spat_vals)
        spat_temp_approx_vals = np.zeros_like(spat_approx_vals)

    norm_factors = np.arange(1, n_levels+1)
    srred_vals = np.cumsum(spat_vals) / norm_factors
    trred_vals = np.cumsum(temp_vals) / norm_factors
    strred_vals = np.cumsum(spat_temp_vals) / norm_factors
    srred_approx_vals = spat_approx_vals
    trred_approx_vals = temp_approx_vals
    strred_approx_vals = spat_temp_approx_vals

    if not full:
        return (srred_vals, trred_vals, strred_vals), (srred_approx_vals, trred_approx_vals, strred_approx_vals)
    else:
        return ((srred_vals, trred_vals, strred_vals), (srred_approx_vals, trred_approx_vals, strred_approx_vals)), (spat_vals, temp_vals, spat_temp_vals)

def strred_hv_pyr(pyr_ref, pyr_dist, prev_pyr_ref, prev_pyr_dist, block_size=3, single=False, full=False):
    # Pyramids are assumed to have the structure
    # ([A1, ..., An], [(H1, V1, D1), ..., (Hn, Vn, Dn)])
    approxs_ref, details_ref = pyr_ref
    approxs_dist, details_dist = pyr_dist
    assert len(details_ref) == len(details_dist), 'Both wavelet pyramids must be of the same height'
    n_levels = len(details_ref)
    spat_gsm_ref_details = [tuple([rred_entropies_and_scales(subband, block_size) for subband in level]) for level in details_ref]
    spat_gsm_dist_details = [tuple([rred_entropies_and_scales(subband, block_size) for subband in level]) for level in details_dist]
    compute_temporal = (prev_pyr_ref is not None and prev_pyr_dist is not None)
    if compute_temporal:
        prev_approxs_ref, prev_details_ref = prev_pyr_ref
        prev_approxs_dist, prev_details_dist = prev_pyr_dist
        temp_gsm_ref_details = [tuple([rred_entropies_and_scales(subband - prev_subband, block_size) for subband, prev_subband in zip(level, prev_level)])
                                for level, prev_level in zip(details_ref, prev_details_ref)]
        temp_gsm_dist_details = [tuple([rred_entropies_and_scales(subband - prev_subband, block_size) for subband, prev_subband in zip(level, prev_level)])
                                 for level, prev_level in zip(details_dist, prev_details_dist)]

    agg = lambda x: np.abs(np.mean(x)) if single else np.mean(np.abs(x))

    spat_vals = np.array([
        np.mean([agg(scale_ref * entropy_ref - scale_dist * entropy_dist) for (entropy_ref, scale_ref), (entropy_dist, scale_dist) in zip(level_ref, level_dist)])
        for level_ref, level_dist in zip(spat_gsm_ref_details, spat_gsm_dist_details)
    ])

    if compute_temporal:
        temp_vals = np.array([
            np.mean([
                agg(spat_scale_ref * temp_scale_ref * entropy_ref - spat_scale_dist * temp_scale_dist * entropy_dist)
                for (_, spat_scale_ref), (_, spat_scale_dist), (entropy_ref, temp_scale_ref), (entropy_dist, temp_scale_dist)
                in zip(spat_level_ref, spat_level_dist, temp_level_ref, temp_level_dist)
            ])
            for spat_level_ref, spat_level_dist, temp_level_ref, temp_level_dist in zip(spat_gsm_ref_details, spat_gsm_dist_details, temp_gsm_ref_details, temp_gsm_dist_details)
        ])
        spat_temp_vals = spat_vals * temp_vals
    else:
        temp_vals = np.zeros_like(spat_vals)
        spat_temp_vals = np.zeros_like(spat_vals)

    norm_factors = np.arange(1, n_levels+1)
    srred_vals = np.cumsum(spat_vals) / norm_factors
    trred_vals = np.cumsum(temp_vals) / norm_factors
    strred_vals = np.cumsum(spat_temp_vals) / norm_factors

    if not full:
        return (srred_vals, trred_vals, strred_vals)
    else:
        return (srred_vals, trred_vals, strred_vals), (spat_vals, temp_vals, spat_temp_vals)

def blur_edge_pyr(pyr_ref, pyr_dis, mode='both'):
    if mode not in ['blur', 'edge', 'both']:
        raise ValueError

    _, details_ref = pyr_ref
    _, details_dis = pyr_dis

    diffs = [np.sum(np.stack([np.abs(sub_ref) - np.abs(sub_dis) for sub_ref, sub_dis in zip(lev_ref, lev_dis)], -1), -1) for lev_ref, lev_dis in zip(details_ref, details_dis)]

    if mode != 'edge':
        blur_scales = [np.mean(np.clip(diff, 0, None)) for diff in diffs]

    if mode != 'blur':
        edge_scales = [-np.mean(np.clip(diff, None, 0)) for diff in diffs]

    if mode == 'blur':
        return blur_scales
    elif mode == 'edge':
        return edge_scales
    else:
        return blur_scales, edge_scales
