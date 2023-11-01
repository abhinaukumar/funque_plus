from .filt import sep_filt_opp

# Motion using a k-tap smoothing filter
def motion_opp(k):
    opp = 0 
    opp += sep_filt_opp(k)
    opp += 2  # diff + abs
    opp += 1  # agg
    return opp

