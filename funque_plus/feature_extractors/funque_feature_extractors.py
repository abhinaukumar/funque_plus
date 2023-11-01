from typing import Dict, Any, Optional

from videolib import Video, standards
from qualitylib.feature_extractor import FeatureExtractor
from qualitylib.result import Result

import numpy as np
import cv2
from ..features.funque_atoms import pyr_features, vif_utils, filter_utils


class FunqueFeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements FUNQUE.
    '''
    NAME = 'FUNQUE_fex'
    VERSION = '1.0'

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.wavelet_levels = 1
        self.vif_extra_levels = 1
        self.wavelet = 'haar'
        self.feat_names = \
            [f'ssim_cov_channel_y_levels_{self.wavelet_levels}', f'dlm_channel_y_scale_{self.wavelet_levels}', f'motion_channel_y_scale_{self.wavelet_levels}'] + \
            [f'vif_approx_scalar_channel_y_scale_{scale+1}' for scale in range(self.wavelet_levels+self.vif_extra_levels)]

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}

        channel_names = ['y', 'u', 'v']
        channel_name = 'y'
        channel_ind = 0

        with Video(
            asset_dict['ref_path'], mode='r',
            standard=asset_dict['ref_standard'],
            width=asset_dict['width'], height=asset_dict['height']
        ) as v_ref:
            with Video(
                asset_dict['dis_path'], mode='r',
                standard=asset_dict['dis_standard'],
                width=asset_dict['width'], height=asset_dict['height']
            ) as v_dis:
                w_crop = (v_ref.width >> (self.wavelet_levels+self.vif_extra_levels+1)) << (self.wavelet_levels+self.vif_extra_levels)
                h_crop = (v_ref.height >> (self.wavelet_levels+self.vif_extra_levels+1)) << (self.wavelet_levels+self.vif_extra_levels)

                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    y_ref = cv2.resize(frame_ref.yuv[..., 0].astype(v_ref.standard.dtype), (frame_ref.width//2, frame_ref.height//2), interpolation=cv2.INTER_CUBIC).astype('float64')/asset_dict['ref_standard'].range
                    y_dis = cv2.resize(frame_dis.yuv[..., 0].astype(v_dis.standard.dtype), (frame_dis.width//2, frame_dis.height//2), interpolation=cv2.INTER_CUBIC).astype('float64')/asset_dict['dis_standard'].range

                    # Cropping to a power of 2 to avoid problems in WD-SSIM
                    y_ref = y_ref[:h_crop, :w_crop]
                    y_dis = y_dis[:h_crop, :w_crop]

                    channel_ref = y_ref
                    channel_dis = y_dis

                    [channel_ref, channel_dis] = [filter_utils.filter_img(channel, self.csf, self.wavelet, channel=channel_ind) for channel in (channel_ref, channel_dis)]

                    [vif_pyr_ref, vif_pyr_dis] = [pyr_features.custom_wavedec2(channel, self.wavelet, 'periodization', self.wavelet_levels+self.vif_extra_levels) for channel in (channel_ref, channel_dis)]
                    pyr_ref = tuple([p[:1] for p in vif_pyr_ref])
                    pyr_dis = tuple([p[:1] for p in vif_pyr_dis])

                    if frame_ind % sample_interval:
                        prev_pyr_ref = pyr_ref.copy()
                        continue

                    # SSIM features
                    ssim_cov = pyr_features.ssim_pyr(pyr_ref, pyr_dis, pool='cov')
                    feats_dict[f'ssim_cov_channel_{channel_name}_levels_1'].append(ssim_cov)

                    # Scalar VIF features
                    vif_approx_scales = [vif_utils.vif_spatial(approx_ref, approx_dis, sigma_nsq=5, k=9, full=False) for approx_ref, approx_dis in zip(vif_pyr_ref[0], vif_pyr_dis[0])]
                    for lev, vif_approx_scale in enumerate(vif_approx_scales):
                        feats_dict[f'vif_approx_scalar_channel_{channel_name}_scale_{lev+1}'].append(vif_approx_scale)

                    # DLM features
                    dlm_val = pyr_features.dlm_pyr(pyr_ref, pyr_dis, csf=None)
                    feats_dict[f'dlm_channel_{channel_name}_scale_1'].append(dlm_val)

                    # MAD features
                    if frame_ind != 0:
                        subband = pyr_ref[0][0]
                        prev_subband = prev_pyr_ref[0][0]
                        motion_val = np.mean(np.abs(subband - prev_subband))
                    else:
                        motion_val = 0

                    feats_dict[f'motion_channel_{channel_name}_scale_1'].append(motion_val)

                    prev_pyr_ref = pyr_ref

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class YFunquePlusFeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements Y-FUNQUE+.
    '''
    NAME = 'Y_FUNQUE_Plus_fex'
    VERSION = '1.0'

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.wavelet_levels = 2
        self.csf = 'nadenau_weight'
        self.wavelet = 'haar'
        self.feat_names = [f'ms_ssim_cov_channel_y_levels_{self.wavelet_levels}', f'dlm_channel_y_scale_{self.wavelet_levels}', f'mad_ref_channel_y_scale_{self.wavelet_levels}']

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}

        channel_names = ['y', 'u', 'v']
        channel_name = 'y'
        channel_ind = 0

        with Video(
            asset_dict['ref_path'], mode='r',
            standard=asset_dict['ref_standard'],
            width=asset_dict['width'], height=asset_dict['height']
        ) as v_ref:
            with Video(
                asset_dict['dis_path'], mode='r',
                standard=asset_dict['dis_standard'],
                width=asset_dict['width'], height=asset_dict['height']
            ) as v_dis:
                w_crop = (v_ref.width >> (self.wavelet_levels+1)) << self.wavelet_levels
                h_crop = (v_ref.height >> (self.wavelet_levels+1)) << self.wavelet_levels

                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    y_ref = cv2.resize(frame_ref.yuv[..., 0].astype(v_ref.standard.dtype), (frame_ref.width//2, frame_ref.height//2), interpolation=cv2.INTER_CUBIC).astype('float64') / asset_dict['ref_standard'].range
                    y_dis = cv2.resize(frame_dis.yuv[..., 0].astype(v_dis.standard.dtype), (frame_dis.width//2, frame_dis.height//2), interpolation=cv2.INTER_CUBIC).astype('float64') / asset_dict['dis_standard'].range

                    # Cropping to a power of 2 to avoid problems in SSIM
                    y_ref = y_ref[:h_crop, :w_crop]
                    y_dis = y_dis[:h_crop, :w_crop]

                    channel_ref = y_ref
                    channel_dis = y_dis

                    [pyr_ref, pyr_dis] = [pyr_features.custom_wavedec2(channel, self.wavelet, 'periodization', self.wavelet_levels) for channel in (channel_ref, channel_dis)]
                    [pyr_ref, pyr_dis] = [filter_utils.filter_pyr(pyr, self.csf, channel=channel_ind) for pyr in (pyr_ref, pyr_dis)]

                    if frame_ind % sample_interval:
                        prev_pyr_ref = pyr_ref.copy()
                        continue

                    # SSIM features
                    _, (ms_ssim_cov_scales, _) = pyr_features.ms_ssim_pyr(pyr_ref, pyr_dis, pool='all')
                    feats_dict[f'ms_ssim_cov_channel_{channel_name}_levels_{self.wavelet_levels}'].append(ms_ssim_cov_scales[-1])

                    # DLM features
                    dlm_val = pyr_features.dlm_pyr((None, [pyr_ref[1][-1]]), (None, [pyr_dis[1][-1]]), csf=None)
                    feats_dict[f'dlm_channel_{channel_name}_scale_{self.wavelet_levels}'].append(dlm_val)

                    # MAD features
                    if frame_ind != 0:
                        motion_val = np.mean(np.abs(pyr_ref[0][-1]- prev_pyr_ref[0][-1]))
                    else:
                        motion_val = 0 
                    feats_dict[f'mad_ref_channel_{channel_name}_scale_{self.wavelet_levels}'].append(motion_val)

                    prev_pyr_ref = pyr_ref

        feats = np.array(list(feats_dict.values())).T

        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class FullScaleYFunquePlusFeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements FS-Y-FUNQUE+.
    '''
    NAME = 'FS_Y_FUNQUE_Plus_fex'
    VERSION = '1.0'

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.wavelet_levels = 2
        self.csf = 'nadenau_spat'
        self.wavelet = 'haar'
        self.feat_names = [f'ms_ssim_cov_channel_y_levels_{self.wavelet_levels}', f'dlm_channel_y_scale_{self.wavelet_levels}', f'strred_scalar_channel_y_levels_{self.wavelet_levels}', f'mad_dis_channel_y_scale_{self.wavelet_levels}', f'sai_diff_channel_y_scale_{self.wavelet_levels}']

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}

        channel_names = ['y', 'u', 'v']
        channel_name = 'y'
        channel_ind = 0

        with Video(
            asset_dict['ref_path'], mode='r',
            standard=asset_dict['ref_standard'],
            width=asset_dict['width'], height=asset_dict['height']
        ) as v_ref:
            with Video(
                asset_dict['dis_path'], mode='r',
                standard=asset_dict['dis_standard'],
                width=asset_dict['width'], height=asset_dict['height']
            ) as v_dis:
                w_crop = (v_ref.width >> self.wavelet_levels) << self.wavelet_levels
                h_crop = (v_ref.height >> self.wavelet_levels) << self.wavelet_levels

                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    y_ref = frame_ref.yuv[..., 0] / asset_dict['ref_standard'].range
                    y_dis = frame_dis.yuv[..., 0] / asset_dict['dis_standard'].range

                    # Cropping to a power of 2 to avoid problems in SSIM
                    y_ref = y_ref[:h_crop, :w_crop]
                    y_dis = y_dis[:h_crop, :w_crop]

                    channel_ref = y_ref
                    channel_dis = y_dis

                    [channel_ref, channel_dis] = [filter_utils.filter_img(channel, self.csf, self.wavelet, channel=channel_ind) for channel in (channel_ref, channel_dis)]
                    [pyr_ref, pyr_dis] = [pyr_features.custom_wavedec2(channel, self.wavelet, 'periodization', self.wavelet_levels) for channel in (channel_ref, channel_dis)]

                    if frame_ind % sample_interval:
                        prev_pyr_ref = pyr_ref.copy()
                        prev_pyr_dis = pyr_dis.copy()
                        continue

                    # SSIM features
                    _, (ms_ssim_cov_scales, _) = pyr_features.ms_ssim_pyr(pyr_ref, pyr_dis, pool='all')
                    feats_dict[f'ms_ssim_cov_channel_{channel_name}_levels_{self.wavelet_levels}'].append(ms_ssim_cov_scales[-1])

                    # DLM features
                    dlm_val = pyr_features.dlm_pyr((None, [pyr_ref[1][-1]]), (None, [pyr_dis[1][-1]]), csf=None)
                    feats_dict[f'dlm_channel_{channel_name}_scale_{self.wavelet_levels}'].append(dlm_val)

                    if frame_ind != 0:
                        # MAD features
                        motion_val = np.mean(np.abs(pyr_dis[0][-1]- prev_pyr_dis[0][-1]))

                        # STRRED features
                        (_, _, strred_scales) = pyr_features.strred_hv_pyr(pyr_ref, pyr_dis, prev_pyr_ref, prev_pyr_dis, block_size=1)
                    else:
                        motion_val = 0 
                        strred_scales = [0]*self.wavelet_levels

                    feats_dict[f'mad_dis_channel_{channel_name}_scale_{self.wavelet_levels}'].append(motion_val)
                    feats_dict[f'strred_scalar_channel_{channel_name}_levels_{self.wavelet_levels}'].append(strred_scales[-1])

                    # TLVQM-like features 
                    # Spatial activity - swap Haar H, V for Sobel H, V
                    energy_ref = pyr_ref[1][-1][0]**2 + pyr_ref[1][-1][1]**2
                    energy_dis = pyr_dis[1][-1][0]**2 + pyr_dis[1][-1][1]**2

                    sai_ref = np.std(np.sqrt(energy_ref))**0.25
                    sai_dis = np.std(np.sqrt(energy_dis))**0.25

                    feats_dict[f'sai_diff_channel_{channel_name}_scale_{self.wavelet_levels}'].append(sai_ref - sai_dis)

                    prev_pyr_ref = pyr_ref
                    prev_pyr_dis = pyr_dis

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class ThreeChannelFunquePlusFeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements FS-Y-FUNQUE+.
    '''
    NAME = '3C_FUNQUE_Plus_fex'
    VERSION = '1.0'

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.wavelet_levels = 2
        self.csf = 'li'
        self.wavelet = 'haar'
        self.feat_names = \
            [f'ms_ssim_cov_channel_y_levels_{self.wavelet_levels}', f'srred_scalar_channel_y_levels_{self.wavelet_levels}', f'trred_scalar_channel_y_levels_{self.wavelet_levels}'] + \
            [f'dlm_channel_y_scale_{self.wavelet_levels}', f'mad_dis_channel_y_scale_{self.wavelet_levels}'] + \
            [f'edge_channel_u_scale_{self.wavelet_levels}', f'mad_channel_v_scale_{self.wavelet_levels}']

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}

        channel_names = ['y', 'u', 'v']

        with Video(
            asset_dict['ref_path'], mode='r',
            standard=asset_dict['ref_standard'],
            width=asset_dict['width'], height=asset_dict['height']
        ) as v_ref:
            with Video(
                asset_dict['dis_path'], mode='r',
                standard=asset_dict['dis_standard'],
                width=asset_dict['width'], height=asset_dict['height']
            ) as v_dis:
                w_crop = (v_ref.width >> (self.wavelet_levels+1)) << self.wavelet_levels
                h_crop = (v_ref.height >> (self.wavelet_levels+1)) << self.wavelet_levels

                pyrs_ref = {}
                pyrs_dis = {}
                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    for channel_ind, channel_name in enumerate(channel_names):
                        channel_ref = cv2.resize(frame_ref.yuv[..., channel_ind].astype(v_ref.standard.dtype), (frame_ref.width//2, frame_ref.height//2), interpolation=cv2.INTER_CUBIC) / asset_dict['ref_standard'].range
                        channel_dis = cv2.resize(frame_dis.yuv[..., channel_ind].astype(v_dis.standard.dtype), (frame_dis.width//2, frame_dis.height//2), interpolation=cv2.INTER_CUBIC) / asset_dict['dis_standard'].range

                        channel_ref = channel_ref[:h_crop, :w_crop]
                        channel_dis = channel_dis[:h_crop, :w_crop]

                        [pyr_ref, pyr_dis] = [pyr_features.custom_wavedec2(channel, self.wavelet, 'periodization', self.wavelet_levels) for channel in (channel_ref, channel_dis)]
                        [pyr_ref, pyr_dis] = [filter_utils.filter_pyr(pyr, self.csf, channel=channel_ind) for pyr in (pyr_ref, pyr_dis)]

                        pyrs_ref[channel_name] = pyr_ref
                        pyrs_dis[channel_name] = pyr_dis

                    if frame_ind % sample_interval:
                        prev_pyrs_ref = pyrs_ref.copy()
                        prev_pyrs_dis = pyrs_dis.copy()
                        continue

                    # Y channel
                    channel_name = 'y'
                    channel_ind = 0
                    pyr_ref = pyrs_ref[channel_name]
                    pyr_dis = pyrs_dis[channel_name]

                    # SSIM features
                    _, (ms_ssim_cov_scales, _) = pyr_features.ms_ssim_pyr(pyr_ref, pyr_dis, pool='all')
                    feats_dict[f'ms_ssim_cov_channel_{channel_name}_levels_{self.wavelet_levels}'].append(ms_ssim_cov_scales[-1])

                    # DLM features
                    dlm_val = pyr_features.dlm_pyr((None, [pyr_ref[1][-1]]), (None, [pyr_dis[1][-1]]), csf=None)
                    feats_dict[f'dlm_channel_{channel_name}_scale_{self.wavelet_levels}'].append(dlm_val)

                    if frame_ind != 0:
                        # MAD features
                        mad_dis_val = np.mean(np.abs(pyr_dis[0][-1] - prev_pyrs_dis[channel_name][0][-1]))

                        # Scalar ST-RRED features
                        srred_scales, trred_scales, _ = pyr_features.strred_hv_pyr(pyr_ref, pyr_dis, prev_pyrs_ref[channel_name], prev_pyrs_dis[channel_name], block_size=1)
                    else:
                        mad_dis_val = 0
                        srred_scales = [0]*self.wavelet_levels
                        trred_scales = [0]*self.wavelet_levels

                    feats_dict[f'mad_dis_channel_{channel_name}_scale_{self.wavelet_levels}'].append(mad_dis_val)

                    feats_dict[f'srred_scalar_channel_{channel_name}_levels_{self.wavelet_levels}'].append(srred_scales[-1])
                    feats_dict[f'trred_scalar_channel_{channel_name}_levels_{self.wavelet_levels}'].append(trred_scales[-1])

                    # U channel
                    channel_name = 'u'
                    channel_ind = 1

                    pyr_ref = pyrs_ref[channel_name]
                    pyr_dis = pyrs_dis[channel_name]

                    [edge_val] = pyr_features.blur_edge_pyr((None, [pyr_ref[1][-1]]), (None, [pyr_dis[1][-1]]), mode='edge')
                    feats_dict[f'edge_channel_{channel_name}_scale_{self.wavelet_levels}'].append(edge_val)

                    # V channel
                    channel_name = 'v'
                    channel_ind = 2
                    pyr_ref = pyrs_ref[channel_name]
                    pyr_dis = pyrs_dis[channel_name]

                    feats_dict[f'mad_channel_{channel_name}_scale_{self.wavelet_levels}'].append(np.mean(np.abs(pyr_ref[0][-1] - pyr_dis[0][-1])))

                    prev_pyrs_ref = pyrs_ref.copy()
                    prev_pyrs_dis = pyrs_dis.copy()

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class FullScaleThreeChannelFunquePlusFeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements FS-Y-FUNQUE+.
    '''
    NAME = 'FS_3C_FUNQUE_Plus_fex'
    VERSION = '1.0'

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.wavelet_levels = 3
        self.csf = 'watson'
        self.wavelet = 'haar'
        self.feat_names = \
            [f'ms_ssim_cov_channel_y_levels_{self.wavelet_levels}', f'dlm_channel_y_scale_{self.wavelet_levels}', f'sai_diff_channel_y_scale_{self.wavelet_levels}'] + \
            [f'mad_dis_channel_u_scale_{self.wavelet_levels}', f'srred_scalar_channel_u_levels_{self.wavelet_levels}', f'trred_scalar_channel_u_levels_{self.wavelet_levels}', f'edge_channel_u_scale_{self.wavelet_levels}'] + \
            [f'mad_channel_v_scale_{self.wavelet_levels}', f'blur_channel_v_scale_{self.wavelet_levels}']

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}

        channel_names = ['y', 'u', 'v']

        with Video(
            asset_dict['ref_path'], mode='r',
            standard=asset_dict['ref_standard'],
            width=asset_dict['width'], height=asset_dict['height']
        ) as v_ref:
            with Video(
                asset_dict['dis_path'], mode='r',
                standard=asset_dict['dis_standard'],
                width=asset_dict['width'], height=asset_dict['height']
            ) as v_dis:
                w_crop = (v_ref.width >> self.wavelet_levels) << self.wavelet_levels
                h_crop = (v_ref.height >> self.wavelet_levels) << self.wavelet_levels

                pyrs_ref = {}
                pyrs_dis = {}
                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    for channel_ind, channel_name in enumerate(channel_names):
                        channel_ref = frame_ref.yuv[..., channel_ind] / asset_dict['ref_standard'].range
                        channel_dis = frame_dis.yuv[..., channel_ind] / asset_dict['dis_standard'].range

                        channel_ref = channel_ref[:h_crop, :w_crop]
                        channel_dis = channel_dis[:h_crop, :w_crop]

                        [pyr_ref, pyr_dis] = [pyr_features.custom_wavedec2(channel, self.wavelet, 'periodization', self.wavelet_levels) for channel in (channel_ref, channel_dis)]
                        [pyr_ref, pyr_dis] = [filter_utils.filter_pyr(pyr, self.csf, channel=channel_ind) for pyr in (pyr_ref, pyr_dis)]

                        pyrs_ref[channel_name] = pyr_ref
                        pyrs_dis[channel_name] = pyr_dis

                    if frame_ind % sample_interval:
                        prev_pyrs_ref = pyrs_ref.copy()
                        prev_pyrs_dis = pyrs_dis.copy()
                        continue

                    # Y channel
                    channel_name = 'y'
                    channel_ind = 0
                    pyr_ref = pyrs_ref[channel_name]
                    pyr_dis = pyrs_dis[channel_name]

                    # SSIM features
                    ms_ssim_cov_scales, _ = pyr_features.ms_ssim_pyr(pyr_ref, pyr_dis, pool='cov')
                    feats_dict[f'ms_ssim_cov_channel_{channel_name}_levels_{self.wavelet_levels}'].append(ms_ssim_cov_scales[-1])

                    # TLVQM-like features 
                    # Spatial activity - swap Haar H, V for Sobel H, V
                    energy_ref = pyr_ref[1][-1][0]**2 + pyr_ref[1][-1][1]**2
                    energy_dis = pyr_dis[1][-1][0]**2 + pyr_dis[1][-1][1]**2

                    sai_ref = np.std(np.sqrt(energy_ref))**0.25
                    sai_dis = np.std(np.sqrt(energy_dis))**0.25

                    feats_dict[f'sai_diff_channel_{channel_name}_scale_{self.wavelet_levels}'].append(sai_ref - sai_dis)

                    # DLM features
                    dlm_val = pyr_features.dlm_pyr((None, [pyr_ref[1][-1]]), (None, [pyr_dis[1][-1]]), csf=None)
                    feats_dict[f'dlm_channel_{channel_name}_scale_{self.wavelet_levels}'].append(dlm_val)

                    # U channel
                    channel_name = 'u'
                    channel_ind = 1
                    pyr_ref = pyrs_ref[channel_name]
                    pyr_dis = pyrs_dis[channel_name]

                    if frame_ind != 0:
                        # MAD-Dis features
                        mad_dis_val = np.mean(np.abs(pyr_dis[0][-1] - prev_pyrs_dis[channel_name][0][-1]))
                        # Scalar ST-RRED features
                        srred_scales, trred_scales, _ = pyr_features.strred_hv_pyr(pyr_ref, pyr_dis, prev_pyrs_ref[channel_name], prev_pyrs_dis[channel_name], block_size=1)
                    else:
                        mad_dis_val = 0
                        srred_scales = [0]*self.wavelet_levels
                        trred_scales = [0]*self.wavelet_levels

                    feats_dict[f'mad_dis_channel_{channel_name}_scale_{self.wavelet_levels}'].append(mad_dis_val)

                    feats_dict[f'srred_scalar_channel_{channel_name}_levels_{self.wavelet_levels}'].append(srred_scales[-1])
                    feats_dict[f'trred_scalar_channel_{channel_name}_levels_{self.wavelet_levels}'].append(trred_scales[-1])

                    # Edge features
                    [edge_val] = pyr_features.blur_edge_pyr((None, [pyr_ref[1][-1]]), (None, [pyr_dis[1][-1]]), mode='edge')
                    feats_dict[f'edge_channel_{channel_name}_scale_{self.wavelet_levels}'].append(edge_val)

                    # V channel
                    channel_name = 'v'
                    channel_ind = 2
                    pyr_ref = pyrs_ref[channel_name]
                    pyr_dis = pyrs_dis[channel_name]

                    feats_dict[f'mad_channel_{channel_name}_scale_{self.wavelet_levels}'].append(np.mean(np.abs(pyr_ref[0][-1] - pyr_dis[0][-1])))

                    # Blur features
                    [blur_val] = pyr_features.blur_edge_pyr((None, [pyr_ref[1][-1]]), (None, [pyr_dis[1][-1]]), mode='blur')
                    feats_dict[f'blur_channel_{channel_name}_scale_{self.wavelet_levels}'].append(blur_val)

                    prev_pyrs_ref = pyrs_ref.copy()
                    prev_pyrs_dis = pyrs_dis.copy()

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))
