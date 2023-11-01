from .csf import sw_csf_opp
from .dwt import haar_opp
from .ssim import wd_ms_essim_opp
from .sai import sai_opp
from .dlm import dlm_opp
from .motion import motion_opp
from .strred import srred_opp, trred_opp
from .blur_edge import blur_opp, edge_opp

def ah_three_channel_funque_plus_opp():
    opp = 0
    opp += sw_csf_opp(3)  # Ref CSF
    opp += sw_csf_opp(3)  # Dis CSF

    opp += haar_opp(3)  # Ref Haar
    opp += haar_opp(3)  # Dis Haar

    opp += wd_ms_essim_opp(3)

    opp += 2*sai_opp(3)  # sai diff uses both sai's

    opp += dlm_opp(1, opt_cm=True) / 4**2  # Only coarsest scale

    opp += motion_opp(0)/4**3  # MAD-Dis ~ Motion without smoothing on a subband of 1/16 size

    opp += srred_opp(3) + trred_opp(3)

    opp += edge_opp(3)

    opp += motion_opp(0)/4**3  # MAD ~ Motion without smoothing on a subband of 1/16 size

    opp += blur_opp(3)

    return opp

