from .filt import int_opp


# SRRED on subband at l'th level (0-based)
def srred_sub_opp(l):
    opp = 0

    # Ref entr and scale computation
    opp += (int_opp() + 1)/4**(l+1)  # mean ref - int sum + norm
    opp += (1 + int_opp() + 1 + 1 + 1)/4**(l+1)  # var ref - square, int sum, norm, square mean, sub
    opp += (1 + 1 + 1)  # entr ref - add sigma_nsq + log + entr const
    opp += (1 + 1)  # scales ref - add 1 + log

    # Dis entr and scale computation
    opp += (int_opp() + 1)/4**(l+1)  # mean dis - int sum + norm
    opp += (1 + int_opp() + 1 + 1 + 1)/4**(l+1)  # var dis - square, int sum, norm, square mean, sub
    opp += (1 + 1 + 1)  # entr dis - add sigma_nsq + log + entr const
    opp += (1 + 1)  # scales dis - add 1 + log

    opp += (1 + 1 + 1 + 1)/4**(l+1)  # diff of scale * entr + agg

    return opp


# TRRED on subband at l'th level (0-based)
def trred_sub_opp(l):
    opp = 0

    opp += (1 + 1)/4**(l+1)  # Diff wrt prev for ref and dis

    # same as srred
    opp += srred_sub_opp(l)
    # add uncounted extra spatial scale factor multiplication
    opp += (1 + 1)/4**(l+1)  # diff of scale * scale * entr

    return opp


# STRRED on subband at l'th level (0-based)
def strred_sub_opp(l):
    opp = 0
    opp += srred_sub_opp(l)
    opp += trred_sub_opp(l)

    return opp


# SRRED-HVD using l levels
def srred_opp(l):
    opp = 0
    for i in range(l):
        opp += 3*srred_sub_opp(i)
    return opp

# TRRED-HVD using l levels
def trred_opp(l):
    opp = 0
    for i in range(l):
        opp += 3*trred_sub_opp(i)
    return opp

# STRRED-HVD using l levels
def strred_opp(l):
    opp = 0
    for i in range(l):
        opp += 3*strred_sub_opp(i)
    return opp