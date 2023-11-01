from .cnn import conv_opp, max_pool_opp, act_opp

def _norm_avg_opp(chans):
    opp = 0
    opp += (1*chans + 1*chans + 1 + 1 + 1*chans)  # L2 normalization - square, sum, sqrt, add eps, divide
    opp += 1 * chans  # Global average pooling
    return opp


def lpips_opp():
    opp = 0
    sub_factor = 1  # Subsampling factor due to strides

    # Deep blocks follow AlexNet architecture from torchvision

    opp += conv_opp(in_c=3, out_c=64, k=11, stride=4) / sub_factor**2 # Conv - first alone has a stride of 4
    chans = 64
    sub_factor *= 4
    opp += act_opp(chans=chans) / sub_factor**2  # ReLU
    opp += max_pool_opp(k=3, stride=2, chans=chans) / sub_factor**2  # MaxPool
    sub_factor *= 2

    opp += _norm_avg_opp(chans=chans) / sub_factor**2  # L2 normalize and avg pool

    opp += conv_opp(in_c=64, out_c=192, k=5) / sub_factor**2  # Conv
    chans = 192
    opp += act_opp(chans=chans) / sub_factor**2  # ReLU
    opp += max_pool_opp(k=3, stride=2, chans=chans) / sub_factor**2 # MaxPool
    sub_factor *= 2

    opp += _norm_avg_opp(chans=chans) / sub_factor**2  # L2 normalize and avg pool

    opp += conv_opp(in_c=192, out_c=384, k=3) / sub_factor**2  # Conv
    chans = 384
    opp += act_opp(chans=chans) / sub_factor**2  # ReLU

    opp += _norm_avg_opp(chans=chans) / sub_factor**2  # L2 normalize and avg pool

    opp += conv_opp(in_c=384, out_c=256, k=3) / sub_factor**2  # Conv
    chans = 256
    opp += act_opp(chans=chans) / sub_factor**2  # ReLU

    opp += _norm_avg_opp(chans=chans) / sub_factor**2  # L2 normalize and avg pool

    opp += conv_opp(in_c=256, out_c=256, k=3) / sub_factor**2  # Conv
    chans = 256
    opp += act_opp(chans=chans) / sub_factor**2  # ReLU
    opp += max_pool_opp(k=3, stride=2, chans=chans) / sub_factor**2 # MaxPool
    sub_factor *= 2

    opp += _norm_avg_opp(chans=chans) / sub_factor**2  # L2 normalize and avg pool

    return 2 * opp  # Repeat operations for both input images
