from .csf import sw_csf_opp
from .dwt import haar_opp
from .ssim import wd_ms_essim_opp
from .motion import motion_opp
from .dlm import dlm_opp
from .strred import srred_opp, trred_opp
from .blur_edge import edge_opp

def three_channel_funque_plus_opp():
    opp = 0
    opp += sw_csf_opp(2)  # Ref CSF
    opp += sw_csf_opp(2)  # Dis CSF

    opp += haar_opp(2)  # Ref Haar
    opp += haar_opp(2)  # Dis Haar

    opp += wd_ms_essim_opp(2)

    opp += motion_opp(0)/4**2  # MAD-Dis ~ Motion without smoothing on a subband of 1/16 size

    opp += dlm_opp(1, opt_cm=True) / 4  # Only coarsest scale

    opp += srred_opp(2) + trred_opp(2)

    opp += edge_opp(2)

    opp += motion_opp(0)/4**2  # MAD ~ Motion without smoothing on a subband of 1/16 size

    opp /= 4  # SAST

    return opp

