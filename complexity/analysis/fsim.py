import numpy as np

def sim_opp():
    opp = 0
    opp += 3  # Num
    opp += 4  # den
    opp += 1  # ratio
    return opp

def scharr_1d_opp():
    return 7  # (00 - 02 + 20 - 22) * 3 + (10 - 12)*10

def grad_mag_opp():
    opp = 0
    opp += scharr_1d_opp()  # scharr x
    opp += scharr_1d_opp()  # scharr y
    opp += 3  # square both and add
    opp += 1  # sqrt
    return opp

def pc_opp(M, N, s, o):
    opp = 0
    opp += 2.5*N*M*np.log2(M)/(M*N)  # real to complex FFT along each row
    opp += 5*M*N*np.log2(N)/(M*N)  # complext to complex FFT along each col of prev output
    opp += 1 + 4 + 2  # meshgrid setup + radius + angle using atan
    opp += 2  # sin and cos theta

    opp += 4  # lpf computation using precomputed radius
    for i in range(s):
        opp += 2  # log rad
        opp += 4  # gaussian on log rad
        opp += 1  # mult for filtering

    for i in range(o):
        opp += 3 + 3  # ang dist in cos and sin
        opp += 3  # ang dist
        opp += 2  # scale dtheta and clip
        opp += 3  # spread calc
        for j in range(s):
            opp += 1  # filter calc
            opp += 2  # filter mult
            opp += 5*N*M*np.log2(M)/(M*N)  # complex to complex IFFT along each row
            opp += 5*M*N*np.log2(N)/(M*N)  # complext to complex IFFT along each col of prev output
            opp += 4  # complex abs calc
            opp += 1  # abs sum
            opp += 1  # real sum
            opp += 1  # imag sum
            if i == 0:
                opp += 1  # Median used, but hard to analyze flops. Underestimating using mean
            else:
                opp += 1  # Max of An
        opp += 1 + 2 + 2  # energy v sum with sumE and odd * sin/cos
        opp += 5  # xenergy
        opp += 2  # meanE and meanO

        for j in range(s):
            opp += 1 + 3 + 4 + 1  # energy computation

        opp += 2  # thresh - sub + clip
        opp += 4  # width
        opp += 5  # weight
        opp += 2  # thisPC
        opp += 1  # pcSum

        # extra computation performed in phasepack but not encessary
        # pcSum already computed here so let's assume it's reused
        return opp

def fsim_opp(M, N):
    s = 4
    o = 6
    opp = 0
    opp += 2*pc_opp(M, N, s, o)  # phasecong for ref and dis
    opp += 2*grad_mag_opp()  # ref and dis grad mags
    opp += 2*sim_opp()  # phasecong and gradmag sims
    opp += 3  # combined sim
    opp += 3  # num
    opp += 2  # den
    return opp
