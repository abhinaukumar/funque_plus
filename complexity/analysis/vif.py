from .filt import sep_filt_opp, int_opp

# VIF scale l using k-tap separable filter for mean calculation
def vif_scale_opp(l, k, opt_filt=False):
    opp = 0
    if opt_filt:
        for img in ['ref', 'dis']:
            opp += 1 + int_opp()  # E[X] calculation (sum + norm)
            opp += 1 + 1 + int_opp()  # squaring + E[X^2] calculation (sum + norm)
        opp += 1 + 1 + int_opp()  # X1 X2 multiplication + E[X1X2] calculation
    else:
        for img in ['ref', 'dis']:
            opp += sep_filt_opp(k)  # E[X] calculation
            opp += 1 + sep_filt_opp(k)  # squaring + E[X^2] calculation
        opp += 1 + sep_filt_opp(k)  # X1 X2 multiplication + E[X1X2] calculation

    stats_opp = 0
    for img in ['ref', 'dis']:
        stats_opp += 2  # variance = E[X^2] - E[X]^2
    stats_opp += 2  # cov = E[XY] - E[X]E[Y]
    stats_opp += 1  # g = cov / var
    stats_opp += 2  # sig2_v = var - g * cov

    agg_opp = 0
    agg_opp += 5 + 1 + 1 + 1  # Num terms + log + aggregation + eps
    agg_opp += 2 + 1 + 1 + 1  # Den terms + log + aggregation + eps

    opp += stats_opp + agg_opp
    opp /= 4**l  # At scale l, input is 1/4^l size
    return opp


def t_vif_scale_opp(l, k, opt_filt=False):
    opp = 0
    opp += 1 / 4**l  # Compute frame diff
    opp += vif_scale_opp(l, k, opt_filt=opt_filt)
    return opp