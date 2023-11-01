from .filt import sep_filt_opp

# l level db2
def db2_opp(l):
    opp = 0

    level_opp = 4*0.25*sep_filt_opp(4)  # 4 subbands of 1/4 size each created using 4 separable 4-tap filters

    for i in range(l):
        opp += level_opp / 4**i  # After each level, image becomes 1/4 of size

    return opp

def haar_opp(l):
    opp = 0
    
    level_opp = 1 + 1 + 1  # div by sqrt 2 + Sum and difference in both vertical and horiz directions
    for i in range(l):
        opp += level_opp / 4**i

    return opp
