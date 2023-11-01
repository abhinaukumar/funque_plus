import numpy as np

# 2d Convolution
def conv_opp(in_c, out_c, k, stride=1):
    return k**2 * in_c * out_c / stride**2  # Filter kernel is k x k x in_c, there are out_c filters, strided in both directions by stride

# Max Pooling
def max_pool_opp(k, chans, stride=None):
    if stride is None:
        stride = k
    return k**2 * chans / stride**2

# L2 Pooling
def l2_pool_opp(chans):
    opp = 0
    opp += 1  # square input
    opp += conv_opp(1, 1, 5, 2)  # Filter by Hanning
    opp += 1/4  # sqrt output
    return opp * chans

# Pointwise Activations - eg ReLU
def act_opp(chans):
    return chans