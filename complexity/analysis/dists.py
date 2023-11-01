from .cnn import conv_opp, l2_pool_opp, act_opp

_vgg_cfg = [[64, 64, "L"], [128, 128, "L"], [256, 256, 256, "L"], [512, 512, 512, "L"], [512, 512, 512]]

def dists_opp():
    sub_factor = 1
    chans = 3
    opp = 0
    for stage in _vgg_cfg:
        for c in stage:
            if c == "L":
                opp += 1 * chans / sub_factor**2  # Avg pool before L2 pooling
                opp += 3 * chans / sub_factor**2  # Std pool before L2 pooling - subtract mean, square, add
                opp += l2_pool_opp(chans=chans) / sub_factor**2  # L2 pool each channel independently
                sub_factor *= 2
            else:
                opp += conv_opp(in_c=chans, out_c=c, k=3) / sub_factor**2  # Conv
                chans = c
                opp += act_opp(chans=chans) / sub_factor**2  # ReLU
    return 2 * opp  # Repeat operations for both inputs