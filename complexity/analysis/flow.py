from .filt import sep_filt_opp

# l-level Gaussian pyramid
def pyramid_opp(l):
    k = 5  # Gaussian filter size
    opp = 0
    for i in range(l-1):  # Finest level is free
        opp += sep_filt_opp(k) / 4**i
    return opp


def warp_opp():
    opp = 0
    opp += 2  # Add i,j to flow(i,j) at each point to get warp points
    # Approximate "map_coordinates" as lookup + linear interpolation (4-tap filter in 2x2 neighborhood)
    opp += 4 + 4
    opp += 1  # Clipping
    return opp


# ILK solver on pyramid level l, with radius r and warps w
def ilk_solver_opp(l, r, w):
    opp = 0
    
    for i in range(w):
        opp += warp_opp()
        opp += 2  # Gradient along coordinates dir
        opp += 2 + 1  # grad*flow + sum along axis=0
        opp += 2  # error image calc
        opp += 3*(1 + sep_filt_opp(2*r+1))  # (0,0), (1,1) (1,2) grad[i]*grad[j] + filtering
        opp += 2*(1 + sep_filt_opp(2*r+1))  # 0, 1 grad[i] * error img + filtering
        opp += 4 + 1  # Check conditioning
        opp += 1 + 2 + 1 + 2  # scale factor computation + dubtraction twice to solve 2x2 system using Gauss elimination

    return opp / (4**l)  # At level l, input image is 1/4**l size


def ilk_opp():
    r = 4
    w = 4
    opp = 0
    pyr_levels = 7 # corresp to 16 pix coarsest level for 1080p, which is the min size.
    opp += 2*pyramid_opp(pyr_levels)  # 7-level ref, dis pyramids
    for i in range(pyr_levels-1, -1, -1):
        opp += ilk_solver_opp(i, r, w)
        if i:
            opp += 2/4**i  # multiplying by 2 when resizing flow for next level
    return opp

