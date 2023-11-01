from .vmaf import vmaf_filter_widths
from .filt import sep_filt_opp
from .vif import vif_scale_opp, t_vif_scale_opp
from .speed import t_speed_opp
from .dwt import db2_opp
from .csf import sw_csf_opp
from .dlm import dlm_opp

def st_vmaf_opp():
    opp = 0
    for i, k in enumerate(vmaf_filter_widths):
        if i != 0:
            opp += sep_filt_opp(k)*2  # Filter and decimate both
        opp += vif_scale_opp(i, k, opt_filt=False)  # Compute VIF
        opp += t_vif_scale_opp(i, k, opt_filt=False)  # Compute T-VIF
        if i > 0:
            opp += t_speed_opp(i, 5)

    opp += db2_opp(4)  # Ref Db2
    opp += db2_opp(4)  # Dis Db2

    opp += sw_csf_opp(4)  # Ref CSF
    opp += sw_csf_opp(4)  # Dis CSF

    opp += dlm_opp(4, opt_cm=False)
    return opp

