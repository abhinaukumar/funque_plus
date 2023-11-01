from .csf import sw_csf_opp
from .dwt import haar_opp
from .ssim import wd_ms_essim_opp
from .dlm import dlm_opp
from .motion import motion_opp

def y_funque_plus_opp():
    opp = 0
    opp += sw_csf_opp(2)  # Ref CSF
    opp += sw_csf_opp(2)  # Dis CSF

    opp += haar_opp(2)  # Ref Haar
    opp += haar_opp(2)  # Dis Haar

    opp += wd_ms_essim_opp(2)

    opp += dlm_opp(1, opt_cm=True) / 4  # Only coarsest scale

    opp += motion_opp(0)/4**2  # Motion without smoothing on a subband of 1/16 size

    opp /= 4  # SAST

    return opp

