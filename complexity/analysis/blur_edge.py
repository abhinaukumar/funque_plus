def blur_opp(l):
    opp = 0
    opp += 3/4**l  # Absolute value of all high pass coeffs - ref
    opp += 3/4**l  # Absolute value of all high pass coeffs - dis

    opp += 3/4**l  # Sum over subbands - ref
    opp += 3/4**l  # Sum over subbands - dis

    opp += 1/4**l  # Difference
    opp += 1/4**l  # Clip to 0

    opp += 1/4**l  # Agg
    return opp

def edge_opp(l):
    return blur_opp(l)  # Same as blur, just clip in the opposite direction