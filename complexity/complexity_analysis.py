from analysis import \
    psnr_opp, \
    ssim_opp, \
    ms_ssim_opp, \
    fsim_opp, \
    vmaf_opp, \
    st_vmaf_opp, \
    ens_vmaf_opp, \
    enh_vmaf_opp, \
    funque_opp, \
    y_funque_plus_opp, \
    ah_y_funque_plus_opp, \
    three_channel_funque_plus_opp, \
    ah_three_channel_funque_plus_opp, \
    lpips_opp, \
    dists_opp, \
    deep_wsd_opp


def main():
    M, N = 1080, 1920
    ssim_filt_size = 11
    ms_ssim_levels = 5
    frames = 150
    scale_factor = 1e-9*M*N*frames  # 1e-9 for "Giga"
    print(f'SSIM: {(scale_factor*ssim_opp(ssim_filt_size)):.3f} GFLOPs')
    print(f'PSNR: {(scale_factor*psnr_opp()):.3f} GFLOPs')
    print(f'FSIM: {(scale_factor*fsim_opp(M, N)):.3f} GFLOPs')
    print(f'ST-VMAF: {(scale_factor*st_vmaf_opp()):.3f} GFLOPs')
    print(f'MS-SSIM: {(scale_factor*ms_ssim_opp(ms_ssim_levels, ssim_filt_size, scale_factor=1)):.3f} GFLOPs')
    print(f'Ens-VMAF: {(scale_factor*ens_vmaf_opp()):.3f} GFLOPs')
    print(f'VMAF: {(scale_factor*vmaf_opp()):.3f} GFLOPs')
    print(f'Enh-VMAF: {(scale_factor*enh_vmaf_opp()):.3f} GFLOPs')
    print(f'FUNQUE: {(scale_factor*funque_opp()):.3f} GFLOPs')
    print(f'AH-Y-FUNQUE+: {(scale_factor*ah_y_funque_plus_opp()):.3f} GFLOPs')
    print(f'Y-FUNQUE+: {(scale_factor*y_funque_plus_opp()):.3f} GFLOPs')
    print(f'AH-3C-FUNQUE+: {(scale_factor*ah_three_channel_funque_plus_opp()):.3f} GFLOPs')
    print(f'3C-FUNQUE+: {(scale_factor*three_channel_funque_plus_opp()):.3f} GFLOPs')
    print(f'LPIPS: {(scale_factor*lpips_opp()):.3f} GFLOPs')
    print(f'DISTS: {(scale_factor*dists_opp()):.3f} GFLOPs')
    print(f'DeepWSD: {(scale_factor*deep_wsd_opp()):.3f} GFLOPs')

if __name__ == '__main__':
    main()