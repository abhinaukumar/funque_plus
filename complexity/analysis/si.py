def sobel_1d_opp():
    return 4  # 00 - 02, 02 - 22, 2*(10 - 12)

def si_opp():
    opp = 0
    opp += 2*sobel_1d_opp() # x and y grads
    opp += 2 + 1 # square and add x and y grads
    opp += 1  # E of energy + E of sqrt energy to get std(sqrt(energy))
    return opp
