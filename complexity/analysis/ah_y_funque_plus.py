from .filt import sep_filt_opp
from .dwt import haar_opp
from .ssim import wd_ms_essim_opp
from .sai import sai_opp
from .motion import motion_opp
from .dlm import dlm_opp
from .strred import strred_opp

def ah_y_funque_plus_opp():
    opp = 0
    opp += sep_filt_opp(5)  # Ref CSF
    opp += sep_filt_opp(5)  # Dis CSF

    opp += haar_opp(2)  # Ref Haar
    opp += haar_opp(2)  # Dis Haar

    opp += wd_ms_essim_opp(2)

    opp += 2*sai_opp(2)  # sai diff uses both sai's

    opp += motion_opp(0)/4**2  # MAD-Dis ~ Motion without smoothing on a subband of 1/16 size

    opp += dlm_opp(1, opt_cm=True) / 4  # Only coarsest scale

    opp += strred_opp(2)

    return opp

