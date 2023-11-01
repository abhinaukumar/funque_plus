# DLM excluding wavelet transform and CSF
from .flow import ilk_opp, warp_opp
from .dwt import db2_opp


# DLM excluding wavelet transform and CSF
def dlm_opp(l, opt_cm=False):
    opp = 0
    level_opp = 0

    # Decoupling
    sub_opp = 0
    sub_opp += 1  # t/o
    sub_opp += 1  # clip to 0, 1

    level_opp += 3*sub_opp/4

    angle_opp = 0
    angle_opp += 5  # eps addition, o/o, arctan, unit step, pi multi
    angle_opp += 5  # eps addition, t/t, arctan, unit step, pi multi
    angle_opp += 3  # Difference calc
    
    level_opp += angle_opp / 4
    
    rest_opp = 0
    rest_opp += 1  # Mult
    rest_opp += 1  # sub for add calc

    level_opp += 3*rest_opp/4

    # Masking
    mask_opp = 0
    mask_opp += ((1 + 1)*3 + 1)/4  # Abs value of detail subs + sum over subs + mult by 1/30

    # Filter to compute MT
    filt_opp = 0
    if opt_cm:
        filt_opp += 2  # integral image
        filt_opp += 3  # sum calculation
        filt_opp += 1  # add self
    else:
        filt_opp += 1  # mult each center by 1/15
        filt_opp += 9  # 3x3 conv

    mask_opp += filt_opp / 4  # summed sub is 1/4 of size

    mask_opp += 2*3/4  # subtraction + clipping

    level_opp += mask_opp

    # Aggregation
    sub_opp = 2 + 2  # Cubing and adding both rest and orig
    level_opp += 3*sub_opp/4

    for i in range(l):
        opp += level_opp / 4**i

    return opp


# E-DLM excluding wavelet transform and CSF
def edlm_opp(l, opt_cm=False):
    opp = 0
    level_opp = 0

    # Decoupling
    sub_opp = 0
    sub_opp += 1  # t/o
    sub_opp += 1  # clip to 0, 1

    level_opp += 3*sub_opp/4

    angle_opp = 0
    angle_opp += 5  # eps addition, o/o, arctan, unit step, pi multi
    angle_opp += 5  # eps addition, t/t, arctan, unit step, pi multi
    angle_opp += 3  # Difference calc
    
    level_opp += angle_opp / 4
    
    rest_opp = 0
    rest_opp += 1  # Mult
    rest_opp += 1  # sub for add calc

    level_opp += 3*rest_opp/4

    # Masking
    mask_opp = 0
    mask_opp += ilk_opp()  # optical flow for DTF
    mask_opp += warp_opp()  # motion compensation
    mask_opp += 1 + 1  # absolute diff for DTF
    mask_opp += db2_opp(4)  # decompose DTF

    mask_opp = 0
    mask_opp += ((1 + 1)*3 + 1)/4  # Abs value of detail subs + sum over subs + mult by 1/30

    # Filter to compute MT
    filt_opp = 0
    if opt_cm:
        filt_opp += 2  # integral image
        filt_opp += 3  # sum calculation
        filt_opp += 1  # add self
    else:
        filt_opp += 1  # mult each center by 1/15
        filt_opp += 9  # 3x3 conv

    mask_opp += filt_opp / 4  # summed sub is 1/4 of size

    mask_opp += 3/4  # Add 3 subbands to compute DTF at this level

    mask_opp += (1 + 1 + 1)/4  # add 1 to dtf, raise to alpha, divide MT

    mask_opp += 2*3/4  # subtraction + clipping

    level_opp += mask_opp

    # Aggregation
    sub_opp = 2 + 2  # Cubing and adding both rest and orig
    level_opp += 3*sub_opp/4

    for i in range(l):
        opp += level_opp / 4**i

    return opp
