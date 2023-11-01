from .filt import sep_filt_opp
from .dwt import haar_opp
from .ssim import wd_essim_opp
from .vif import vif_scale_opp
from .dlm import dlm_opp
from .motion import motion_opp

def funque_opp():
    opp = 0
    opp += sep_filt_opp(21)  # Ref CSF
    opp += sep_filt_opp(21)  # Dis CSF

    opp += haar_opp(1)  # Ref Haar
    opp += haar_opp(1)  # Dis Haar

    opp += 0.5 + 0.25 # Ref extra approx subband
    opp += 0.5 + 0.25 # Dis extra approx subband

    opp += wd_essim_opp(1)

    for i in range(1, 3):  # Scale 0 means orig size
        opp += vif_scale_opp(i, 5, opt_filt=True)

    opp += dlm_opp(1, opt_cm=True)

    opp += motion_opp(0)/4  # Motion without smoothing on a subband of 1/4 size

    opp = opp / 4  # SAST

    return opp

