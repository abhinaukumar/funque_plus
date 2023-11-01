from .filt import sep_filt_opp

def wd_essim_opp(l):
    opp = 0
    opp += 1/4**l  # mu1
    opp += 1/4**l  # mu2
    opp += (1 - 1/4**l) * (1 + 1)  # var1 - Square and add all except approx
    opp += (1 - 1/4**l) * (1 + 1)  # var2 - Square and add all except approx
    opp += (1 - 1/4**l) * (1 + 1)  # cov - mult corresp and add all except approx
    opp += 1/4**l  # var1 norm 
    opp += 1/4**l  # var2 norm
    opp += 1/4**l  # cov norm 
    opp += (3 + 4 + 1) / 4**l  # l num, den, ratio
    opp += (2 + 2 + 1) / 4**l  # cs num, den, ratio
    opp += 1 / 4**l  # l cs mult
    opp += (1 + 2) / 4**l  # cov pooling - mu and E[X^2] computation. conversion to std and div are negligible per pixel
    return opp


def wd_ms_essim_opp(l):
    opp = 0

    sub_opp = 0
    sub_opp += 1  # mu1 norm
    sub_opp += 1  # mu2 norm
    sub_opp += 1 + 3 + 4 + 1 + 1  # var1 - square, sum over subbands, sum over 2x2 of prev, add cur sum, norm
    sub_opp += 1 + 3 + 4 + 1 + 1  # var2 - square, sum over subbands, sum over 2x2 of prev, add cur sum, norm
    sub_opp += 1 + 3 + 4 + 1 + 1  # cov - mult corresp, sum over subbands, sum over 2x2 of prev, add cur sum, norm
    sub_opp += 3 + 4 + 1  # l num, den, ratio
    sub_opp += 2 + 2 + 1  # cs num, den, ratio

    accum_opp = 1 + 2

    for i in range(l):
        opp += sub_opp / 4**(i+1)
        if i != l-1:
            opp += 2 * accum_opp / 4**(i+1)  # Accumulate l and cs
        else:
            opp += (1 + accum_opp) / 4**(i+1)  # Multiply l and cs and accumulate product

    return opp


# SSIM using a k-tap filter for smoothing
def ssim_opp(k):
    opp = 0
    for img in ['ref', 'dis']:
        opp += sep_filt_opp(k)  # E[X] calculation
        opp += 1 + sep_filt_opp(k)  # squaring + E[X^2] calculation
    opp += 1 + sep_filt_opp(k)  # X1 X2 multiplication + E[X1X2] calculation

    for img in ['ref', 'dis']:
        opp += 2  # variance = E[X^2] - E[X]^2
    opp += 2  # cov = E[XY] - E[X]E[Y]

    opp += (3 + 4 + 1) # l num, den, ratio
    opp += (2 + 2 + 1) # cs num, den, ratio
    opp += 1 # l cs mult
    opp += 1 # mean pooling

    return opp


# l-level MS-SSIM using a k-tap filter for smoothing, including pre-scaling
def ms_ssim_opp(l, k, scale_factor=1):
    opp = 0
    lev_opp = 0
    for img in ['ref', 'dis']:
        lev_opp += sep_filt_opp(k)  # E[X] calculation
        lev_opp += 1 + sep_filt_opp(k)  # squaring + E[X^2] calculation
    lev_opp += 1 + sep_filt_opp(k)  # X1 X2 multiplication + E[X1X2] calculation

    for img in ['ref', 'dis']:
        lev_opp += 2  # variance = E[X^2] - E[X]^2
    lev_opp += 2  # cov = E[XY] - E[X]E[Y]

    lev_opp += (3 + 4 + 1) # l num, den, ratio
    lev_opp += (2 + 2 + 1) # cs num, den, ratio
    lev_opp += (1 + 1)  # l and cs means, or l cs mult + mean

    for i in range(l):
        if scale_factor != 1 and (2**i < scale_factor):
            opp += lev_opp / scale_factor**2
            opp += 2*scale_factor**2 / 4**i  # Scaling
        else:
            opp += lev_opp / 4**i
        if i != l-1:
            opp += 2*4 / 4**i  # Downsampling to next scale

    return opp