from typing import Any, Dict, Optional
import os
import numpy as np
from PIL import Image
import torch

from videolib import Video, standards
from qualitylib.feature_extractor import FeatureExtractor
from qualitylib.result import Result

import lpips
import DISTS_pytorch
from ..features.baseline_atoms import DeepWSD


class LpipsFeatureExtractor(FeatureExtractor):
    NAME = 'LPIPS_fex'
    VERSION = '1.0'
    feat_names = ['lpips']

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.metric = lpips.LPIPS(net='alex').cuda().eval()
        self.batch_size = 32

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
        with torch.no_grad():
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
                    batch_ref_list = []
                    batch_dis_list = []
                    lpips_vals = np.empty((0,), dtype='float64')
                    for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                        if frame_ind % sample_interval == 0:
                            batch_ref_list.append(np.transpose(2*frame_ref.rgb/v_ref.standard.range - 1, (2, 0, 1)))
                            batch_dis_list.append(np.transpose(2*frame_dis.rgb/v_dis.standard.range - 1, (2, 0, 1)))

                        if len(batch_ref_list) == self.batch_size or (frame_ind == v_ref.num_frames-1 and len(batch_ref_list) != 0):
                            batch_ref = torch.from_numpy(np.stack(batch_ref_list, axis=0)).cuda()
                            batch_dis = torch.from_numpy(np.stack(batch_dis_list, axis=0)).cuda()
                            batch_ref_list = []
                            batch_dis_list = []
                            dist = self.metric(batch_ref.float(), batch_dis.float())
                            lpips_vals = np.concatenate([lpips_vals, dist.squeeze().cpu()])

        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats=np.expand_dims(lpips_vals, -1), feat_names=self.feat_names)


class DistsFeatureExtractor(FeatureExtractor):
    NAME = 'DISTS_fex'
    VERSION = '1.0'
    feat_names = ['dists']

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.metric = DISTS_pytorch.DISTS().cuda().eval()
        self.batch_size = 96

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
        with torch.no_grad():
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
                    batch_ref_list = []
                    batch_dis_list = []
                    dists_vals = np.empty((0,), dtype='float64')
                    for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                        if frame_ind % sample_interval == 0:
                            # batch_ref_list.append(DISTS_pytorch.DISTS_pt.prepare_image(Image.fromarray(np.dtype(v_ref.standard.dtype).type(frame_ref.rgb))))
                            # batch_dis_list.append(DISTS_pytorch.DISTS_pt.prepare_image(Image.fromarray(np.dtype(v_dis.standard.dtype).type(frame_dis.rgb))))
                            batch_ref_list.append(DISTS_pytorch.DISTS_pt.prepare_image(Image.fromarray(np.uint8(255*frame_ref.rgb/v_ref.standard.range))))
                            batch_dis_list.append(DISTS_pytorch.DISTS_pt.prepare_image(Image.fromarray(np.uint8(255*frame_dis.rgb/v_dis.standard.range))))

                        if len(batch_ref_list) == self.batch_size or (frame_ind == v_ref.num_frames-1 and len(batch_ref_list) != 0):
                            batch_ref = torch.cat(batch_ref_list, axis=0).cuda()
                            batch_dis = torch.cat(batch_dis_list, axis=0).cuda()
                            batch_ref_list = []
                            batch_dis_list = []
                            dist = self.metric(batch_ref.float(), batch_dis.float())
                            dists_vals = np.concatenate([dists_vals, dist.squeeze().cpu().numpy()])

        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats=np.expand_dims(dists_vals, -1), feat_names=self.feat_names)


class DeepWsdFeatureExtractor(FeatureExtractor):
    NAME = 'DeepWSD_fex'
    # VERSION = '1.0'
    VERSION = '1.1'  # Set batch size to 1
    feat_names = ['deep_wsd']

    def __init__(self, use_cache: bool = True, sample_rate: Optional[int] = None) -> None:
        super().__init__(use_cache, sample_rate)
        self.metric = DeepWSD.DeepWSD().cuda().eval()
        self.batch_size = 1

    def _run_on_asset(self, asset_dict: Dict[str, Any]) -> Result:
        sample_interval = self._get_sample_interval(asset_dict)
        feats_dict = {key: [] for key in self.feat_names}
        with torch.no_grad():
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
                    batch_ref_list = []
                    batch_dis_list = []
                    # wsds_vals = np.empty((0,), dtype='float64')
                    wsds_vals = []
                    for frame_ind, (frame_ref, frame_dis) in enumerate(zip(v_ref, v_dis)):
                        if frame_ind % sample_interval == 0:
                            # batch_ref_list.append(DeepWSD.prepare_image(Image.fromarray(np.dtype(v_ref.standard.dtype).type(frame_ref.rgb))))
                            # batch_dis_list.append(DeepWSD.prepare_image(Image.fromarray(np.dtype(v_dis.standard.dtype).type(frame_dis.rgb))))
                            batch_ref_list.append(DeepWSD.prepare_image(Image.fromarray(np.uint8(255*frame_ref.rgb/v_ref.standard.range))))
                            batch_dis_list.append(DeepWSD.prepare_image(Image.fromarray(np.uint8(255*frame_dis.rgb/v_dis.standard.range))))

                        if len(batch_ref_list) == self.batch_size or (frame_ind == v_ref.num_frames-1 and len(batch_ref_list) != 0):
                            batch_ref = torch.cat(batch_ref_list, axis=0).cuda()
                            batch_dis = torch.cat(batch_dis_list, axis=0).cuda()
                            batch_ref_list = []
                            batch_dis_list = []
                            wsd = self.metric(batch_ref.float(), batch_dis.float(), as_loss=False)
                            # wsds_vals = np.concatenate([wsds_vals, wsd.squeeze().cpu()])
                            wsds_vals.append(wsd.cpu().item())
                            # wsds_vals = np.concatenate([wsds_vals, [wsd.squeeze().cpu().item()]])

        print(f'Processed {asset_dict["dis_path"]}')
        return self._to_result(asset_dict, feats=np.expand_dims(wsds_vals, -1), feat_names=self.feat_names)
