# Separable k-tap filter 
def sep_filt_opp(k):
    opp = 0
    # Two passes - horizontal and vertical
    for dir in range(2):
        opp += k + k # mult + add
    return opp

# Integral image sums
def int_opp():
    opp = 1 + 1 + 3  # Hor sum, ver sum, diff for sums
    return opp
