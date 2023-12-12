from typing import Dict, Any, Optional

from videolib import Video
from qualitylib.feature_extractor import FeatureExtractor
from qualitylib.result import Result

import numpy as np
import scipy as sp
from skimage import metrics
from skvideo import measure
from image_similarity_measures import quality_metrics
from ..features.baseline_atoms import vmaf_features, ens_vmaf_features, evmaf_features, flow_utils
from ..features.funque_atoms import pyr_features


class SsimFeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements SSIM.
    '''
    NAME = 'SSIM_fex'
    VERSION = '1.0'
    feat_names = ['ssim_channel_y']

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
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
                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    if frame_ind % sample_interval:
                        continue
                    ssim = metrics.structural_similarity(frame_ref.yuv[..., 0], frame_dis.yuv[..., 0], win_size=11, gaussian_weights=True, data_range=1)
                    feats_dict['ssim_channel_y'].append(ssim)

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class PsnrFeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements PSNR.
    '''
    NAME = 'PSNR_fex'
    VERSION = '1.0'
    feat_names = ['psnr_channel_y']

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
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
                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    if frame_ind % sample_interval:
                        continue
                    psnr = -10*np.log10(np.mean((frame_ref.yuv[..., 0] - frame_dis.yuv[..., 0])**2))
                    if np.isinf(psnr) or np.isnan(psnr):
                        psnr = 100 
                    feats_dict['psnr_channel_y'].append(psnr)

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class FsimFeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements FSIM.
    '''
    NAME = 'FSIM_fex'
    VERSION = '1.0'
    feat_names = ['fsim_channel_y']

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
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
                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    if frame_ind % sample_interval:
                        continue
                    fsim = quality_metrics.fsim(frame_ref.yuv[..., :1], frame_dis[..., :1])
                    feats_dict['fsim_channel_y'].append(fsim)

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class StVmafFeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements ST-VMAF.
    '''
    NAME = 'STVMAF_fex'
    VERSION = '1.0'
    feat_names = \
        [f'vif_channel_y_scale_{scale}' for scale in range(4)] + \
        [f't_vif_channel_y_scale_{scale}' for scale in range(4)] + \
        [f't_speed_channel_y_scale_{scale}' for scale in range(1, 4)] + \
        ['dlm_channel_y']

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.scales = 4
        self.vif_filters = [
            np.array([0.00745626912, 0.0142655009, 0.0250313189, 0.0402820669, 0.0594526194, 0.0804751068, 0.0999041125, 0.113746084, 0.118773937, 0.113746084, 0.0999041125, 0.0804751068, 0.0594526194, 0.0402820669, 0.0250313189, 0.0142655009, 0.00745626912]),
            np.array([0.0189780835, 0.0558981746, 0.120920904, 0.192116052, 0.224173605, 0.192116052, 0.120920904, 0.0558981746, 0.0189780835]),
            np.array([0.054488685, 0.244201347, 0.402619958, 0.244201347, 0.054488685]),
            np.array([0.166378498, 0.667243004, 0.166378498])
        ]

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
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
                y_scales_ref_prev = [None, None, None, None]
                y_scales_dis_prev = [None, None, None, None]
                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    if frame_ind % sample_interval:
                        continue

                    # VIF-Y features
                    y_scale_ref = frame_ref.yuv[..., 0].copy()
                    y_scale_dis = frame_dis.yuv[..., 0].copy()

                    y_scales_ref_cur = []
                    y_scales_dis_cur = []
                    for scale in range(self.scales):
                        # Compute VIF at current scale
                        feats_dict[f'vif_channel_y_scale_{scale}'].append(vmaf_features.vif(y_scale_ref, y_scale_dis, self.vif_filters[scale]))

                        # Compute T-SpEED at scales above 1
                        if scale >= 1:
                            t_speed = ens_vmaf_features.t_speed(y_scale_ref, y_scale_dis, y_scales_ref_prev[scale], y_scales_dis_prev[scale])
                            feats_dict[f't_speed_channel_y_scale_{scale}'].append(t_speed)

                        # Compute T-VIF
                        t_vif_val = ens_vmaf_features.t_vif(y_scale_ref, y_scale_dis, y_scales_ref_prev[scale], y_scales_dis_prev[scale], self.vif_filters[scale])
                        feats_dict[f't_vif_channel_y_scale_{scale}'].append(t_vif_val)

                        y_scales_ref_cur.append(y_scale_ref)
                        y_scales_dis_cur.append(y_scale_dis)

                        # Filter and decimate
                        if scale != self.scales-1:
                            y_scale_ref = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_ref, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_dis = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_dis, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_ref = y_scale_ref[::2, ::2]
                            y_scale_dis = y_scale_dis[::2, ::2]

                    # DLM feature
                    [pyr_ref, pyr_dis] = [pyr_features.custom_wavedec2(channel, self.wavelet, 'periodization', self.scales) for channel in (frame_ref.yuv[..., 0], frame_dis.yuv[..., 0])]

                    dlm_val = pyr_features.dlm_pyr(pyr_ref, pyr_dis, csf='watson')
                    feats_dict[f'dlm_channel_y'].append(dlm_val)

                    y_scales_ref_prev = y_scales_ref_cur
                    y_scales_dis_prev = y_scales_dis_cur

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class MsSsimFeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements MS-SSIM.
    '''
    NAME = 'MS_SSIM_fex'
    VERSION = '1.0'
    feat_names = ['ms_ssim_channel_y']

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
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
                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    if frame_ind % sample_interval:
                        continue
                    ms_ssim = measure.msssim(frame_ref.yuv[..., :1], frame_dis[..., :1])
                    feats_dict['ms_ssim_channel_y'].append(ms_ssim)

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class EnsVmafM1FeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements model 1 of Ensemble VMAF.
    '''
    NAME = 'EnsVMAF_M1_fex'
    VERSION = '1.0'
    feat_names = \
        [f'vif_channel_y_scale_{scale}' for scale in range(4)] + \
        ['dlm_channel_y', 'ti_channel_y_scale_2']

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.scales = 4
        self.vif_filters = [
            np.array([0.00745626912, 0.0142655009, 0.0250313189, 0.0402820669, 0.0594526194, 0.0804751068, 0.0999041125, 0.113746084, 0.118773937, 0.113746084, 0.0999041125, 0.0804751068, 0.0594526194, 0.0402820669, 0.0250313189, 0.0142655009, 0.00745626912]),
            np.array([0.0189780835, 0.0558981746, 0.120920904, 0.192116052, 0.224173605, 0.192116052, 0.120920904, 0.0558981746, 0.0189780835]),
            np.array([0.054488685, 0.244201347, 0.402619958, 0.244201347, 0.054488685]),
            np.array([0.166378498, 0.667243004, 0.166378498])
        ]

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
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
                y_scales_ref_prev = [None, None, None, None]
                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    y_scale_ref = frame_ref.yuv[..., 0].copy()
                    y_scale_dis = frame_dis.yuv[..., 0].copy()

                    y_scales_ref_cur = []
                    y_scales_dis_cur = []
                    for scale in range(self.scales):
                        y_scales_ref_cur.append(y_scale_ref)
                        y_scales_dis_cur.append(y_scale_dis)
                        # Filter and decimate
                        if scale != self.scales-1:
                            y_scale_ref = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_ref, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_dis = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_dis, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_ref = y_scale_ref[::2, ::2]
                            y_scale_dis = y_scale_dis[::2, ::2]

                    if frame_ind % sample_interval:
                        y_scales_ref_prev = y_scales_ref_cur
                        continue

                    for scale, (y_scale_ref, y_scale_dis) in enumerate(zip(y_scales_ref_cur, y_scales_dis_cur)):
                        # Compute VIF at current scale
                        feats_dict[f'vif_channel_y_scale_{scale}'].append(vmaf_features.vif(y_scale_ref, y_scale_dis, self.vif_filters[scale]))

                        # Compute TI-Y feature at scale 2
                        if scale == 2:
                            if y_scales_ref_prev[2] is None:
                                motion_val = 0
                            else:
                                motion_val = np.mean(np.abs(y_scale_ref - y_scales_ref_prev[2]))
                            feats_dict['ti_channel_y_scale_2'].append(motion_val)

                    # Compute DLM
                    [pyr_ref, pyr_dis] = [pyr_features.custom_wavedec2(channel, self.wavelet, 'periodization', self.scales) for channel in (frame_ref.yuv[..., 0], frame_dis.yuv[..., 0])]

                    dlm_val = pyr_features.dlm_pyr(pyr_ref, pyr_dis, csf='watson')
                    feats_dict[f'dlm_channel_y'].append(dlm_val)

                    y_scales_ref_prev = y_scales_ref_cur

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class EnsVmafM2FeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements model 2 of Ensemble VMAF.
    '''
    NAME = 'EnsVMAF_fex'
    VERSION = '1.0'
    feat_names = \
        [f's_speed_channel_y_scale_{scale}' for scale in range(1, 4)] + \
        [f't_speed_channel_y_scale_{scale}' for scale in range(1, 4)]

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.scales = 4
        self.vif_filters = [
            np.array([0.00745626912, 0.0142655009, 0.0250313189, 0.0402820669, 0.0594526194, 0.0804751068, 0.0999041125, 0.113746084, 0.118773937, 0.113746084, 0.0999041125, 0.0804751068, 0.0594526194, 0.0402820669, 0.0250313189, 0.0142655009, 0.00745626912]),
            np.array([0.0189780835, 0.0558981746, 0.120920904, 0.192116052, 0.224173605, 0.192116052, 0.120920904, 0.0558981746, 0.0189780835]),
            np.array([0.054488685, 0.244201347, 0.402619958, 0.244201347, 0.054488685]),
            np.array([0.166378498, 0.667243004, 0.166378498])
        ]

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
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
                y_scales_ref_prev = [None, None, None, None]
                y_scales_dis_prev = [None, None, None, None]
                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    y_scale_ref = frame_ref.yuv[..., 0].copy()
                    y_scale_dis = frame_dis.yuv[..., 0].copy()

                    y_scales_ref_cur = []
                    y_scales_dis_cur = []
                    for scale in range(self.scales):
                        y_scales_ref_cur.append(y_scale_ref)
                        y_scales_dis_cur.append(y_scale_dis)
                        # Filter and decimate
                        if scale != self.scales-1:
                            y_scale_ref = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_ref, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_dis = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_dis, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_ref = y_scale_ref[::2, ::2]
                            y_scale_dis = y_scale_dis[::2, ::2]

                    if frame_ind % sample_interval:
                        y_scales_ref_prev = y_scales_ref_cur
                        y_scales_dis_prev = y_scales_dis_cur
                        continue

                    for scale, (y_scale_ref, y_scale_dis) in enumerate(zip(y_scales_ref_cur, y_scales_dis_cur)):
                        # Compute S-SpEED and T-SpEED at scales above 1
                        if scale >= 1:
                            s_speed, t_speed = ens_vmaf_features.speed(y_scale_ref, y_scale_dis, y_scales_ref_prev[scale], y_scales_dis_prev[scale])
                            feats_dict[f's_speed_channel_y_scale_{scale}'].append(s_speed)
                            feats_dict[f't_speed_channel_y_scale_{scale}'].append(t_speed)

                    y_scales_ref_prev = y_scales_ref_cur
                    y_scales_dis_prev = y_scales_dis_cur

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class EnsVmafFeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements Ensemble VMAF.
    '''
    NAME = 'EnsVMAF_fex'
    VERSION = '1.0'
    feat_names = \
        [f'vif_channel_y_scale_{scale}' for scale in range(4)] + \
        [f's_speed_channel_y_scale_{scale}' for scale in range(1, 4)] + \
        [f't_speed_channel_y_scale_{scale}' for scale in range(1, 4)] + \
        ['dlm_channel_y', 'ti_channel_y_scale_2']

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.scales = 4
        self.vif_filters = [
            np.array([0.00745626912, 0.0142655009, 0.0250313189, 0.0402820669, 0.0594526194, 0.0804751068, 0.0999041125, 0.113746084, 0.118773937, 0.113746084, 0.0999041125, 0.0804751068, 0.0594526194, 0.0402820669, 0.0250313189, 0.0142655009, 0.00745626912]),
            np.array([0.0189780835, 0.0558981746, 0.120920904, 0.192116052, 0.224173605, 0.192116052, 0.120920904, 0.0558981746, 0.0189780835]),
            np.array([0.054488685, 0.244201347, 0.402619958, 0.244201347, 0.054488685]),
            np.array([0.166378498, 0.667243004, 0.166378498])
        ]

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
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
                y_scales_ref_prev = [None, None, None, None]
                y_scales_dis_prev = [None, None, None, None]
                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    y_scale_ref = frame_ref.yuv[..., 0].copy()
                    y_scale_dis = frame_dis.yuv[..., 0].copy()

                    y_scales_ref_cur = []
                    y_scales_dis_cur = []
                    for scale in range(self.scales):
                        y_scales_ref_cur.append(y_scale_ref)
                        y_scales_dis_cur.append(y_scale_dis)
                        # Filter and decimate
                        if scale != self.scales-1:
                            y_scale_ref = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_ref, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_dis = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_dis, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_ref = y_scale_ref[::2, ::2]
                            y_scale_dis = y_scale_dis[::2, ::2]

                    if frame_ind % sample_interval:
                        y_scales_ref_prev = y_scales_ref_cur
                        y_scales_dis_prev = y_scales_dis_cur
                        continue

                    for scale, (y_scale_ref, y_scale_dis) in enumerate(zip(y_scales_ref_cur, y_scales_dis_cur)):
                        # Compute VIF at current scale
                        feats_dict[f'vif_channel_y_scale_{scale}'].append(vmaf_features.vif(y_scale_ref, y_scale_dis, self.vif_filters[scale]))

                        # Compute TI-Y feature at scale 2
                        if scale == 2:
                            if y_scales_ref_prev[2] is None:
                                motion_val = 0
                            else:
                                motion_val = np.mean(np.abs(y_scale_ref - y_scales_ref_prev[2]))
                            feats_dict['ti_channel_y_scale_2'].append(motion_val)

                        # Compute S-SpEED and T-SpEED at scales above 1
                        if scale >= 1:
                            s_speed, t_speed = ens_vmaf_features.speed(y_scale_ref, y_scale_dis, y_scales_ref_prev[scale], y_scales_dis_prev[scale])
                            feats_dict[f's_speed_channel_y_scale_{scale}'].append(s_speed)
                            feats_dict[f't_speed_channel_y_scale_{scale}'].append(t_speed)

                    # Compute DLM
                    [pyr_ref, pyr_dis] = [pyr_features.custom_wavedec2(channel, self.wavelet, 'periodization', self.scales) for channel in (frame_ref.yuv[..., 0], frame_dis.yuv[..., 0])]

                    dlm_val = pyr_features.dlm_pyr(pyr_ref, pyr_dis, csf='watson')
                    feats_dict[f'dlm_channel_y'].append(dlm_val)

                    y_scales_ref_prev = y_scales_ref_cur
                    y_scales_dis_prev = y_scales_dis_cur

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class VmafFeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements VMAF.
    '''
    NAME = 'VMAF_fex'
    VERSION = '1.0'
    feat_names = \
        [f'vif_channel_y_scale_{scale}' for scale in range(4)] + \
        ['dlm_channel_y', 'motion_channel_y']

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.scales = 4
        self.vif_filters = [
            np.array([0.00745626912, 0.0142655009, 0.0250313189, 0.0402820669, 0.0594526194, 0.0804751068, 0.0999041125, 0.113746084, 0.118773937, 0.113746084, 0.0999041125, 0.0804751068, 0.0594526194, 0.0402820669, 0.0250313189, 0.0142655009, 0.00745626912]),
            np.array([0.0189780835, 0.0558981746, 0.120920904, 0.192116052, 0.224173605, 0.192116052, 0.120920904, 0.0558981746, 0.0189780835]),
            np.array([0.054488685, 0.244201347, 0.402619958, 0.244201347, 0.054488685]),
            np.array([0.166378498, 0.667243004, 0.166378498])
        ]

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
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
                y_ref_prev = None
                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    if frame_ind % sample_interval:
                        y_ref_prev = frame_ref.yuv[..., 0]
                        continue

                    y_scale_ref = frame_ref.yuv[..., 0].copy()
                    y_scale_dis = frame_dis.yuv[..., 0].copy()

                    y_scales_ref_cur = []
                    y_scales_dis_cur = []
                    for scale in range(self.scales):
                        y_scales_ref_cur.append(y_scale_ref)
                        y_scales_dis_cur.append(y_scale_dis)
                        # Filter and decimate
                        if scale != self.scales-1:
                            y_scale_ref = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_ref, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_dis = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_dis, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_ref = y_scale_ref[::2, ::2]
                            y_scale_dis = y_scale_dis[::2, ::2]

                    for scale, (y_scale_ref, y_scale_dis) in enumerate(zip(y_scales_ref_cur, y_scales_dis_cur)):
                        # Compute VIF at current scale
                        feats_dict[f'vif_channel_y_scale_{scale}'].append(vmaf_features.vif(y_scale_ref, y_scale_dis, self.vif_filters[scale]))

                    # DLM feature
                    feats_dict[f'dlm_channel_y'].append(vmaf_features.dlm(frame_ref.yuv[..., 0], frame_dis.yuv[..., 0]))

                    # Motion feature
                    if y_ref_prev is not None:
                        feats_dict[f'motion_channel_y'].append(vmaf_features.motion(frame_ref.yuv[..., 0], y_ref_prev, self.vif_filters[2]))
                    else:
                        feats_dict[f'motion_channel_y'].append(0)

                    y_ref_prev = frame_ref.yuv[..., 0]

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class EnhVmafM1FeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements model 1 of Enhanced VMAF.
    '''
    NAME = 'EnhVMAF_M1_fex'
    VERSION = '1.0'
    feat_names = \
        [f'vif_channel_y_scale_{scale}' for scale in range(4)] + \
        ['e_dlm_channel_y_alpha_20', 'ti_channel_y_scale_2', 'blur_channel_y_scale_1', 'edge_channel_y_scale_3']

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.scales = 4
        self.vif_filters = [
            np.array([0.00745626912, 0.0142655009, 0.0250313189, 0.0402820669, 0.0594526194, 0.0804751068, 0.0999041125, 0.113746084, 0.118773937, 0.113746084, 0.0999041125, 0.0804751068, 0.0594526194, 0.0402820669, 0.0250313189, 0.0142655009, 0.00745626912]),
            np.array([0.0189780835, 0.0558981746, 0.120920904, 0.192116052, 0.224173605, 0.192116052, 0.120920904, 0.0558981746, 0.0189780835]),
            np.array([0.054488685, 0.244201347, 0.402619958, 0.244201347, 0.054488685]),
            np.array([0.166378498, 0.667243004, 0.166378498])
        ]

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
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
                y_scales_ref_prev = [None, None, None, None]

                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    y_scale_ref = frame_ref.yuv[..., 0].copy()
                    y_scale_dis = frame_dis.yuv[..., 0].copy()

                    y_scales_ref_cur = []
                    y_scales_dis_cur = []
                    for scale in range(self.scales):
                        y_scales_ref_cur.append(y_scale_ref)
                        y_scales_dis_cur.append(y_scale_dis)
                        # Filter and decimate
                        if scale != self.scales-1:
                            y_scale_ref = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_ref, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_dis = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_dis, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_ref = y_scale_ref[::2, ::2]
                            y_scale_dis = y_scale_dis[::2, ::2]

                    if frame_ind % sample_interval:
                        y_scales_ref_prev = y_scales_ref_cur
                        continue

                    for scale, (y_scale_ref, y_scale_dis) in enumerate(zip(y_scales_ref_cur, y_scales_dis_cur)):
                        # Compute VIF at current scale
                        feats_dict[f'vif_channel_y_scale_{scale}'].append(vmaf_features.vif(y_scale_ref, y_scale_dis, self.vif_filters[scale]))

                        # TI-Y feature
                        if scale == 2:
                            if y_scales_ref_prev[2] is None:
                                motion_val = 0
                            else:
                                motion_val = np.mean(np.abs(y_scale_ref - y_scales_ref_prev[2]))
                            feats_dict['ti_channel_y_scale_2'].append(motion_val)

                    # E-DLM feature
                    [pyr_ref, pyr_dis] = [pyr_features.custom_wavedec2(channel, self.wavelet, 'periodization', self.scales) for channel in (frame_ref.yuv[..., 0], frame_dis.yuv[..., 0])]
                    if y_scales_ref_prev[0] is None:
                        dtf = np.zeros_like(frame_ref.yuv[..., 0])
                    else:
                        dtf = flow_utils.compensated_diff(frame_ref.yuv[..., 0], y_scales_ref_prev[0])
                    pyr_dtf = pyr_features.custom_wavedec2(dtf, self.wavelet, 'periodization', self.scales)

                    exp = 20
                    dlm_val = evmaf_features.e_dlm_pyr(pyr_dtf, pyr_ref, pyr_dis, [exp])[0]
                    feats_dict[f'e_dlm_channel_y_alpha_{exp}'].append(dlm_val)

                    # Blur-Y feature
                    blur_scales = pyr_features.blur_edge_pyr(([None], [pyr_ref[1][1]]), ([None], [pyr_dis[1][1]]), mode='blur')
                    feats_dict['blur_channel_y_scale_1'].append(blur_scales[0])
                    # Edge-Y feature
                    edge_scales = pyr_features.blur_edge_pyr(([None], [pyr_ref[1][3]]), ([None], [pyr_dis[1][3]]), mode='edge')
                    feats_dict['edge_channel_y_scale_3'].append(edge_scales[0])

                    y_scales_ref_prev = y_scales_ref_cur

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class EnhVmafM2FeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements model 2 of Enhanced VMAF.
    '''
    NAME = 'EnhVMAF_M2_fex'
    VERSION = '1.0'
    feat_names = \
        ['e_dlm_channel_y_alpha_20', 'ti_channel_y_scale_2'] + \
        ['psnr_channel_y_scale_3', 'vif_channel_u_scale_0', 'delta_ti_channel_u_scale_3', 'delta_si_channel_v_scale_0']

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.scales = 4
        self.vif_filters = [
            np.array([0.00745626912, 0.0142655009, 0.0250313189, 0.0402820669, 0.0594526194, 0.0804751068, 0.0999041125, 0.113746084, 0.118773937, 0.113746084, 0.0999041125, 0.0804751068, 0.0594526194, 0.0402820669, 0.0250313189, 0.0142655009, 0.00745626912]),
            np.array([0.0189780835, 0.0558981746, 0.120920904, 0.192116052, 0.224173605, 0.192116052, 0.120920904, 0.0558981746, 0.0189780835]),
            np.array([0.054488685, 0.244201347, 0.402619958, 0.244201347, 0.054488685]),
            np.array([0.166378498, 0.667243004, 0.166378498])
        ]

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
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
                y_scales_ref_prev = [None, None, None, None]
                u_scale_ref_prev = None
                u_scale_dis_prev = None

                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    y_scale_ref = frame_ref.yuv[..., 0].copy()
                    y_scale_dis = frame_dis.yuv[..., 0].copy()

                    y_scales_ref_cur = []
                    y_scales_dis_cur = []
                    for scale in range(self.scales):
                        y_scales_ref_cur.append(y_scale_ref)
                        y_scales_dis_cur.append(y_scale_dis)
                        # Filter and decimate
                        if scale != self.scales-1:
                            y_scale_ref = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_ref, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_dis = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_dis, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_ref = y_scale_ref[::2, ::2]
                            y_scale_dis = y_scale_dis[::2, ::2]

                    u_scale_ref = frame_ref.yuv[..., 1].copy()
                    u_scale_dis = frame_dis.yuv[..., 1].copy()
                    for scale in range(self.scales-1):
                        # Filter and decimate
                        u_scale_ref = sp.ndimage.convolve1d(sp.ndimage.convolve1d(u_scale_ref, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                        u_scale_dis = sp.ndimage.convolve1d(sp.ndimage.convolve1d(u_scale_dis, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                        u_scale_ref = u_scale_ref[::2, ::2]
                        u_scale_dis = u_scale_dis[::2, ::2]

                    if frame_ind % sample_interval:
                        y_scales_ref_prev = y_scales_ref_cur
                        u_scale_ref_prev = u_scale_ref
                        u_scale_dis_prev = u_scale_dis
                        continue

                    for scale, (y_scale_ref, y_scale_dis) in enumerate(zip(y_scales_ref_cur, y_scales_dis_cur)):
                        # TI-Y feature
                        if scale == 2:
                            if y_scales_ref_prev[2] is None:
                                motion_val = 0
                            else:
                                motion_val = np.mean(np.abs(y_scale_ref - y_scales_ref_prev[2]))
                            feats_dict['ti_channel_y_scale_2'].append(motion_val)

                        # PSNR-Y feature
                        if scale == 3:
                            mse_val = np.mean((y_scale_ref - y_scale_dis)**2)
                            psnr_val = -10*np.log10(mse_val)
                            if np.isinf(psnr_val) or np.isnan(psnr_val):
                                psnr_val = 100
                            feats_dict['psnr_channel_y_scale_3'].append(psnr_val)

                    # E-DLM feature
                    [pyr_ref, pyr_dis] = [pyr_features.custom_wavedec2(channel, self.wavelet, 'periodization', self.scales) for channel in (frame_ref.yuv[..., 0], frame_dis.yuv[..., 0])]
                    if y_scales_ref_prev[0] is None:
                        dtf = np.zeros_like(frame_ref.yuv[..., 0])
                    else:
                        dtf = flow_utils.compensated_diff(frame_ref.yuv[..., 0], y_scales_ref_prev[0])
                    pyr_dtf = pyr_features.custom_wavedec2(dtf, self.wavelet, 'periodization', self.scales)

                    exp = 20
                    dlm_val = evmaf_features.e_dlm_pyr(pyr_dtf, pyr_ref, pyr_dis, [exp])[0]
                    feats_dict[f'e_dlm_channel_y_alpha_{exp}'].append(dlm_val)

                    # VIF-U feature
                    feats_dict['vif_channel_u_scale_0'].append(vmaf_features.vif(frame_ref.yuv[..., 1], frame_dis.yuv[..., 1], self.vif_filters[0]))

                    # deltaTI-U feature
                    if u_scale_ref_prev is None:
                        ref_motion_val = 0
                    else:
                        ref_motion_val = np.mean(np.abs(u_scale_ref - u_scale_ref_prev))

                    if u_scale_dis_prev is None:
                        dis_motion_val = 0
                    else:
                        dis_motion_val = np.mean(np.abs(u_scale_dis - u_scale_dis_prev))

                    feats_dict['delta_ti_channel_u_scale_3'].append(dis_motion_val - ref_motion_val)

                    # deltaSI-V feature
                    grad_ref = np.sqrt(sp.ndimage.sobel(v_ref, axis=0)**2 + sp.ndimage.sobel(v_ref, axis=1)**2)
                    si_ref_val = np.std(grad_ref[1:-1, 1:-1])
                    grad_dis = np.sqrt(sp.ndimage.sobel(v_dis, axis=0)**2 + sp.ndimage.sobel(v_dis, axis=1)**2)
                    si_dis_val = np.std(grad_dis[1:-1, 1:-1])
                    feats_dict['delta_si_channel_v_scale_0'].append(si_dis_val - si_ref_val)

                    y_scales_ref_prev = y_scales_ref_cur
                    u_scale_ref_prev = u_scale_ref
                    u_scale_dis_prev = u_scale_dis

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))


class EnhVmafFeatureExtractor(FeatureExtractor):
    '''
    A feature extractor that implements Enhanced VMAF.
    '''
    NAME = 'EnhVMAF_fex'
    VERSION = '1.0'
    feat_names = \
        [f'vif_channel_y_scale_{scale}' for scale in range(4)] + \
        ['e_dlm_channel_y_alpha_20', 'ti_channel_y_scale_2', 'blur_channel_y_scale_1', 'edge_channel_y_scale_3'] + \
        ['psnr_channel_y_scale_3', 'vif_channel_u_scale_0', 'delta_ti_channel_u_scale_3', 'delta_si_channel_v_scale_0']

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.scales = 4
        self.vif_filters = [
            np.array([0.00745626912, 0.0142655009, 0.0250313189, 0.0402820669, 0.0594526194, 0.0804751068, 0.0999041125, 0.113746084, 0.118773937, 0.113746084, 0.0999041125, 0.0804751068, 0.0594526194, 0.0402820669, 0.0250313189, 0.0142655009, 0.00745626912]),
            np.array([0.0189780835, 0.0558981746, 0.120920904, 0.192116052, 0.224173605, 0.192116052, 0.120920904, 0.0558981746, 0.0189780835]),
            np.array([0.054488685, 0.244201347, 0.402619958, 0.244201347, 0.054488685]),
            np.array([0.166378498, 0.667243004, 0.166378498])
        ]

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
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
                y_scales_ref_prev = [None, None, None, None]
                u_scale_ref_prev = None
                u_scale_dis_prev = None

                for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                    y_scale_ref = frame_ref.yuv[..., 0].copy()
                    y_scale_dis = frame_dis.yuv[..., 0].copy()

                    y_scales_ref_cur = []
                    y_scales_dis_cur = []
                    for scale in range(self.scales):
                        y_scales_ref_cur.append(y_scale_ref)
                        y_scales_dis_cur.append(y_scale_dis)
                        # Filter and decimate
                        if scale != self.scales-1:
                            y_scale_ref = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_ref, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_dis = sp.ndimage.convolve1d(sp.ndimage.convolve1d(y_scale_dis, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                            y_scale_ref = y_scale_ref[::2, ::2]
                            y_scale_dis = y_scale_dis[::2, ::2]

                    u_scale_ref = frame_ref.yuv[..., 1].copy()
                    u_scale_dis = frame_dis.yuv[..., 1].copy()
                    for scale in range(self.scales-1):
                        # Filter and decimate
                        u_scale_ref = sp.ndimage.convolve1d(sp.ndimage.convolve1d(u_scale_ref, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                        u_scale_dis = sp.ndimage.convolve1d(sp.ndimage.convolve1d(u_scale_dis, self.vif_filters[scale+1], 0), self.vif_filters[scale+1], 1)
                        u_scale_ref = u_scale_ref[::2, ::2]
                        u_scale_dis = u_scale_dis[::2, ::2]

                    if frame_ind % sample_interval:
                        y_scales_ref_prev = y_scales_ref_cur
                        u_scale_ref_prev = u_scale_ref
                        u_scale_dis_prev = u_scale_dis
                        continue

                    for scale, (y_scale_ref, y_scale_dis) in enumerate(zip(y_scales_ref_cur, y_scales_dis_cur)):
                        # Compute VIF at current scale
                        feats_dict[f'vif_channel_y_scale_{scale}'].append(vmaf_features.vif(y_scale_ref, y_scale_dis, self.vif_filters[scale]))

                        # TI-Y feature
                        if scale == 2:
                            if y_scales_ref_prev[2] is None:
                                motion_val = 0
                            else:
                                motion_val = np.mean(np.abs(y_scale_ref - y_scales_ref_prev[2]))
                            feats_dict['ti_channel_y_scale_2'].append(motion_val)

                        # PSNR-Y feature
                        if scale == 3:
                            mse_val = np.mean((y_scale_ref - y_scale_dis)**2)
                            psnr_val = -10*np.log10(mse_val)
                            if np.isinf(psnr_val) or np.isnan(psnr_val):
                                psnr_val = 100
                            feats_dict['psnr_channel_y_scale_3'].append(psnr_val)

                    # E-DLM feature
                    [pyr_ref, pyr_dis] = [pyr_features.custom_wavedec2(channel, self.wavelet, 'periodization', self.scales) for channel in (frame_ref.yuv[..., 0], frame_dis.yuv[..., 0])]
                    if y_scales_ref_prev[0] is None:
                        dtf = np.zeros_like(frame_ref.yuv[..., 0])
                    else:
                        dtf = flow_utils.compensated_diff(frame_ref.yuv[..., 0], y_scales_ref_prev[0])
                    pyr_dtf = pyr_features.custom_wavedec2(dtf, self.wavelet, 'periodization', self.scales)

                    exp = 20
                    dlm_val = evmaf_features.e_dlm_pyr(pyr_dtf, pyr_ref, pyr_dis, [exp])[0]
                    feats_dict[f'e_dlm_channel_y_alpha_{exp}'].append(dlm_val)

                    # Blur-Y feature
                    blur_scales = pyr_features.blur_edge_pyr(([None], [pyr_ref[1][1]]), ([None], [pyr_dis[1][1]]), mode='blur')
                    feats_dict['blur_channel_y_scale_1'].append(blur_scales[0])
                    # Edge-Y feature
                    edge_scales = pyr_features.blur_edge_pyr(([None], [pyr_ref[1][3]]), ([None], [pyr_dis[1][3]]), mode='edge')
                    feats_dict['edge_channel_y_scale_3'].append(edge_scales[0])

                    # VIF-U feature
                    feats_dict['vif_channel_u_scale_0'].append(vmaf_features.vif(frame_ref.yuv[..., 1], frame_dis.yuv[..., 1], self.vif_filters[0]))

                    # deltaTI-U feature
                    if u_scale_ref_prev is None:
                        ref_motion_val = 0
                    else:
                        ref_motion_val = np.mean(np.abs(u_scale_ref - u_scale_ref_prev))

                    if u_scale_dis_prev is None:
                        dis_motion_val = 0
                    else:
                        dis_motion_val = np.mean(np.abs(u_scale_dis - u_scale_dis_prev))

                    feats_dict['delta_ti_channel_u_scale_3'].append(dis_motion_val - ref_motion_val)

                    # deltaSI-V feature
                    grad_ref = np.sqrt(sp.ndimage.sobel(v_ref, axis=0)**2 + sp.ndimage.sobel(v_ref, axis=1)**2)
                    si_ref_val = np.std(grad_ref[1:-1, 1:-1])
                    grad_dis = np.sqrt(sp.ndimage.sobel(v_dis, axis=0)**2 + sp.ndimage.sobel(v_dis, axis=1)**2)
                    si_dis_val = np.std(grad_dis[1:-1, 1:-1])
                    feats_dict['delta_si_channel_v_scale_0'].append(si_dis_val - si_ref_val)

                    y_scales_ref_prev = y_scales_ref_cur
                    u_scale_ref_prev = u_scale_ref
                    u_scale_dis_prev = u_scale_dis

        feats = np.array(list(feats_dict.values())).T
        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats, list(feats_dict.keys()))
