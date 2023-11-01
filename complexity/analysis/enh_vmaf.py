from .vmaf import vmaf_filter_widths
from .motion import motion_opp
from .filt import sep_filt_opp
from .vif import vif_scale_opp
from .blur_edge import blur_opp, edge_opp
from .dwt import db2_opp
from .csf import sw_csf_opp
from .dlm import edlm_opp
from .psnr import psnr_opp
from .si import si_opp


def enh_vmaf_opp():
    opp = 0

    opp += motion_opp(5)

    for i, k in enumerate(vmaf_filter_widths):
        if i != 0:
            opp += sep_filt_opp(k)*2  # Filter and decimate both
        opp += vif_scale_opp(i, k, opt_filt=False)  # Compute VIF

    opp += edge_opp(3)
    opp += blur_opp(1)

    opp += db2_opp(4)  # Ref Db2
    opp += db2_opp(4)  # Dis Db2

    opp += sw_csf_opp(4)  # Ref CSF
    opp += sw_csf_opp(4)  # Dis CSF

    opp += edlm_opp(4)

    opp += psnr_opp() / 4**3

    opp += vif_scale_opp(0, vmaf_filter_widths[0], opt_filt=False)
    opp += 2*motion_opp(5) / 4**3  # delta TI ~ two motion features
    opp += 2*si_opp()  # delta SI ~ two SI features

    return opp