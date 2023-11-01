from .cnn import conv_opp, l2_pool_opp, act_opp
import numpy as np

_vgg_cfg = [[64, 64, "L"], [128, 128, "L"], [256, 256, 256, "L"], [512, 512, 512, "L"], [512, 512, 512]]

def _wsd_opp(chans):
    wsd_win = 16
    opp = 0
    opp += 2 * 1 * chans  # Sum all coeffs
    opp += 2 * 1 * chans # Divide by sum
    opp += 2 * 1 * chans # x_1d * pdf_1d

    opp += 2 * 1.39*wsd_win**2*np.log2(wsd_win**2) * chans / wsd_win**2  # Estimated number of comparisons for quicksort

    opp += 2 * 1 * chans  # cumsum
    opp += 1.39*2*wsd_win**2*np.log2(2*wsd_win**2) * chans / wsd_win**2  # Estimated number of comparisons for quicksort
    opp += (2*wsd_win**2-1) * chans / wsd_win**2  # delta computation
    opp += 2 * chans  # diff quantiles computation
    opp += 3 * chans  # power, multiply, sum
    return opp


def deep_wsd_opp():
    sub_factor = 1
    chans = 3
    opp = 0
    ds_factor = int(max(1,np.round(max(1920, 1080)/256)))  # Assume 1080p original input
    opp += 2 * conv_opp(1, 1, ds_factor, stride=ds_factor) * chans
    sub_factor *= ds_factor
    for stage in _vgg_cfg:
        for c in stage:
            if c == "L":
                opp += _wsd_opp(chans=chans) / sub_factor**2  # Compute wasserstein distance before L2 pooling
                opp += 2 * l2_pool_opp(chans=chans) / sub_factor**2  # L2 pool each channel independently
                sub_factor *= 2
            else:
                opp += 2 * conv_opp(in_c=chans, out_c=c, k=3) / sub_factor**2  # Conv
                chans = c
                opp += 2 * act_opp(chans=chans) / sub_factor**2  # ReLU
    return 2 * opp  # Repeat operations for both inputs