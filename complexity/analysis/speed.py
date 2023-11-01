from .filt import sep_filt_opp

# S-SpEED scale l with Block size b
def s_speed_opp(l, b):
    opp = 0
    opp += (1 + sep_filt_opp(8))  # 8-tap Gaussian Mean Sub - ref
    opp += (1 + sep_filt_opp(8))  # 8-tap Gaussian Mean Sub - dis

    gsm_opp = 0
    gsm_opp += b**2  # vector mean
    gsm_opp += b**2*(b**2+1)/2  # x_i x_i.T calculation
    gsm_opp += b**2*(b**2+1)/2  # adding to get E[x_i x_i.T]
    gsm_opp += (2*b**2*b**2 + b**2 + 1)/b**2  # x.TM (=y.T) calc + y.Tx calc + norm , on 1/b**2 blocks pp
    gsm_opp += 1/b**2 # clip to tol to avoid negative values, on 1/b**2 blocks pp
    gsm_opp += b**2 * (1 + 3 + 1) / b**2 # entropy calc - sum over eigvals, on 1/b**2 blocks pp
    gsm_opp += 2/b**2  # log(1 + s_sq) to calculate scales, on 1/b**2 blocks pp

    opp += 2*gsm_opp  # Model both ref and dis as GSM

    opp += 5/b**2  # mean of abs diff of scale * entr, on 1/b**2 blocks pp

    return opp / 4**l


# T-SpEED scale l with Block size b
def t_speed_opp(l, b):
    opp = 0
    opp += (1 + 1) / 4**l  # diff calc - ref and dis

    opp += s_speed_opp(l, b)
    opp += (2/b**2)/4**l  # extra mult of spatial scale, on 1/b**2 blocks pp
    return opp


# SpEED with Block size b
def speed_opp(l, b):
    opp = 0
    opp += s_speed_opp(l, b)
    opp += t_speed_opp(l, b)
    return opp