def sai_opp(l):
    opp = 0
    opp += (1 + 1 + 1)/4**l  # Square hor and ver subbands and add
    opp += 1/4**l  # sqrt
    opp += (1 + 1)/4**l  # accum val and sqrt to get std of sqrt
    return opp
