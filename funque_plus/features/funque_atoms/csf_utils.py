import numpy as np


def ngan(f, channel=0):
    return (0.31 + 0.69*f) * np.exp(-0.29*f)


def ngan_spat(d2h=3.0, k=21, channel=0):
    if d2h == 3.0 and k == 21:
        return np.array([-0.01373464, -0.01608515, -0.01890698, -0.02215702, -0.02546262,
                         -0.02742965, -0.02361034, -0.00100996,  0.07137023,  0.22121922,
                          0.3279824, 0.22121922, 0.07137023, -0.00100996, -0.02361034,
                         -0.02742965, -0.02546262, -0.02215702, -0.01890698, -0.01608515,
                         -0.01373464])
    else:
        assert isinstance(k, int) and k > 0 and (k & 1), 'The length of the filter must be an odd positive integer'
        del_theta = 180 / (d2h * 1080 * np.pi)
        t = np.arange(-(k >> 1), (k >> 1) + 1) * del_theta
        assert len(t) == k, 'Filter is of the wrong size'

        a = 0.31
        b = 0.69
        c = 0.29
        f = 2*((a*c + b)*c**2 + (a*c - b)*4*np.pi**2 * t**2) / (c**2 + 4*np.pi**2 * t**2)**2   # Inverse Fourier Transform of CSF.

        return f*del_theta


# Ref "Most apparent distortion: full-reference image quality assessment and the role of strategy", E. C. Larson and D. M. Chandler
def mannos(f, theta, channel=0):
    f_theta = f / (0.15*np.cos(4*theta) + 0.85)
    lamda = 0.228
    f_max = 4  # TODO: Find out how f_max is obtained from lamda
    if isinstance(f, np.ndarray):
        return np.where(f >= f_max, 2.6*(0.0192 + lamda*f_theta)*np.exp(-np.power(lamda*f_theta, 1.1)), 0.981)
    else:
        return 2.6*(0.0192 + lamda*f_theta)*np.exp(-np.power(lamda*f_theta, 1.1)) if f >= f_max else 0.981


def mannos_weight(level, subband, channel=0):
    '''
    level: 0 indexed level of the discrete wavelet transform
    subband: 0 indexed in the list [approximation, horizontal, vertical, diagonal]
    '''
    if level <= 4:
        lookup = np.array([[1.83006647e-03, 7.11828321e-03, 7.11828321e-03, 2.43358422e-04],
                           [1.30120204e-01, 2.25003123e-01, 2.25003123e-01, 5.62679733e-02],
                           [6.59710109e-01, 7.82068784e-01, 7.82068784e-01, 4.94193706e-01],
                           [9.81000000e-01, 9.81000000e-01, 9.81000000e-01, 9.81000000e-01],
                           [9.81000000e-01, 9.81000000e-01, 9.81000000e-01, 9.81000000e-01]])
        return lookup[level, subband]
    else:
        # Distance to height ratio of the display
        d2h = 3.0
        pic_height = 1080
        factor = np.pi*pic_height*d2h/180
        level_frequency = factor / (1 << (level+1))
        orientation_angles = [np.pi/8, 0, np.pi/2, np.pi/4]  # Using pi/8 for approx only to match default value used for Li.
        return mannos(level_frequency, orientation_angles[subband])


# Ref "Compression of color images with wavelets under consideration of the HVS"
def nadenau(f, channel=0):
    a = 1/256
    b_vals = [-5.4715e-3, -1.9584e-2, -7.6400e-3]
    c_vals = [1.91, 1.74, 2.06]
    b = b_vals[channel]
    c = c_vals[channel]
    return (1 - a) * np.exp(b*f**c) + a


def nadenau_spat(d2h=3.0, k=5, channel=0):
    lookup_lens = [5, 7, 5]
    if d2h == 3.0 and k == lookup_lens[channel]:
        lookups = [np.array([0.02531332, 0.23100677, 0.47597679, 0.23100677, 0.02531332]),
                   np.array([0.02572540, 0.08738394, 0.21680633, 0.30467982, 0.21680633, 0.08738394, 0.0257254]),
                   np.array([0.08337400, 0.23642262, 0.33644310, 0.23642262, 0.08337400])]
        return lookups[channel]
    else:
        assert isinstance(k, int) and k > 0 and (k & 1), 'The length of the filter must be an odd positive integer'
        f_max = np.pi * d2h * 1080 / 180
        fs = np.linspace(-0.5, 0.5, 10000) * f_max
        filt = np.real(np.fft.ifft(np.fft.fftshift(nadenau(np.abs(fs), channel))))
        return np.concatenate([filt[-(k//2):], filt[:k//2+1]], axis=0)


def nadenau_weight(level, subband, channel=0):
    '''
    level: 0 indexed level of the discrete wavelet transform
    subband: 0 indexed in the list [approximation, horizontal, vertical, diagonal]
    '''
    if level <= 4:
        lookup = np.array([[[0.01593581, 0.01593581, 0.01593581],
                            [0.04299846, 0.04299846, 0.04299846],
                            [0.04299846, 0.04299846, 0.04299846],
                            [0.00556257, 0.00556257, 0.00556257]],
                           [[0.31146019, 0.31146019, 0.31146019],
                            [0.42474743, 0.42474743, 0.42474743],
                            [0.42474743, 0.42474743, 0.42474743],
                            [0.18536903, 0.18536903, 0.18536903]],
                           [[0.73251132, 0.73251132, 0.73251132],
                            [0.79592083, 0.79592083, 0.79592083],
                            [0.79592083, 0.79592083, 0.79592083],
                            [0.63707782, 0.63707782, 0.63707782]],
                           [[0.92047007, 0.92047007, 0.92047007],
                            [0.94104990, 0.94104990, 0.94104990],
                            [0.94104990, 0.94104990, 0.94104990],
                            [0.88686180, 0.88686180, 0.88686180]],
                           [[0.97818739, 0.97818739, 0.97818739],
                            [0.98396102, 0.98396102, 0.98396102],
                            [0.98396102, 0.98396102, 0.98396102],
                            [0.96855064, 0.96855064, 0.96855064]]])
        return lookup[level, subband, channel]
    else:
        # Distance to height ratio of the display
        d2h = 3.0
        pic_height = 1080
        factor = np.pi*pic_height*d2h/180
        level_frequency = factor / (1 << (level+1))
        orientation_factors = [1.0/0.85, 1.0, 1.0, 1/(0.85-0.15)]
        return nadenau(level_frequency * orientation_factors[subband], channel=0)


def detection_threshold(a, k, f0, g, level_frequency):
    return a * np.power(10, k*np.log10(f0 * g / level_frequency)**2)


def li(level, subband, channel=0):
    '''
    level: 0 indexed level of the discrete wavelet transform
    subband: 0 indexed in the list [approximation, horizontal, vertical, diagonal]
    '''
    if level <= 4:
        lookup = np.array([[0.00150387263, 0.00544585178, 0.00544585178, 0.00023055401], 
                           [0.09476531388, 0.16683506215, 0.16683506215, 0.04074566701],
                           [0.54231822084, 0.66786346496, 0.66786346496, 0.38921962529],
                           [0.95194661972, 0.98626459244, 0.98626459244, 0.87735995465],
                           [0.95462489181, 0.91608864363, 0.91608864363, 0.98675189575]])
        return lookup[level, subband]
    else:
        # Distance to height ratio of the display
        d2h = 3.0
        pic_height = 1080
        factor = np.pi*pic_height*d2h/180
        level_frequency = factor / (1 << (level+1))
        orientation_factors = [1.0/0.85, 1.0, 1.0, 1/(0.85-0.15)]
        return ngan(level_frequency * orientation_factors[subband])


def watson(level, subband, channel=0, pic_height=1080):
    '''
    level: 0 indexed level of the discrete wavelet transform
    subband: 0 indexed in the list [approximation, horizontal, vertical, diagonal]
    Ref: A. Watson, G. Yang, et al. "Visibility of Wavelet Quantization Noise"
    '''
    if level <= 4 and pic_height == 1080:
        lookup = np.array([[[0.03129084, 0.00867185, 0.01688188],
                            [0.01738153, 0.00513065, 0.00599886],
                            [0.01738153, 0.00513065, 0.00599886],
                            [0.00589069, 0.00182899, 0.00164671]],
                           [[0.0464456 , 0.01161772, 0.02621272],
                            [0.03198481, 0.00831135, 0.01253507],
                            [0.03198481, 0.00831135, 0.01253507],
                            [0.01429907, 0.00379459, 0.00468441]],
                           [[0.05326017, 0.01260494, 0.03073023],
                            [0.04337266, 0.01040081, 0.01886397],
                            [0.04337266, 0.01040081, 0.01886397],
                            [0.02439691, 0.00580073, 0.00915396]],
                           [[0.04896673, 0.01149426, 0.02822877],
                            [0.04567341, 0.01059541, 0.02154499],
                            [0.04567341, 0.01059541, 0.02154499],
                            [0.03131274, 0.00699261, 0.01315086]],
                           [[0.03669688, 0.00895634, 0.02065759],
                            [0.03867382, 0.00909817, 0.01933739],
                            [0.03867382, 0.00909817, 0.01933739],
                            [0.03187392, 0.00700816, 0.014644  ]]])
        return lookup[level, subband, channel]
    else:
        # Distance to height ratio of the display
        d2h = 3.0
        factor = np.pi*pic_height*d2h/180
        level_frequency = factor / (1 << (level+1))

        # Detection threshold model parameters
        a_vals = [0.495, 1.633, 0.944]
        k_vals = [0.466, 0.353, 0.521]
        f0_vals = [0.401, 0.209, 0.404]
        g_vals = [[1.501, 1, 1, 0.534],
                  [1.520, 1, 1, 0.502],
                  [1.868, 1, 1, 0.516]]

        a, k, f0, gs = a_vals[channel], k_vals[channel], f0_vals[channel], g_vals[channel]

        # Basis function amplitudes
        amplitudes = np.array([[0.621710, 0.672340, 0.672340, 0.727090],
                               [0.345370, 0.413170, 0.413170, 0.494280],
                               [0.180040, 0.227270, 0.227270, 0.286880],
                               [0.091401, 0.117920, 0.117920, 0.152140],
                               [0.045943, 0.059758, 0.059758, 0.077727],
                               [0.023013, 0.030018, 0.030018, 0.039156]])

        return 0.5 * amplitudes[level, subband] / detection_threshold(a, k, f0, gs[subband], level_frequency)


def hill(level, subband, channel=0, pic_height=1080):
    '''
    level: 0 indexed level of the discrete wavelet transform
    subband: 0 indexed in the list [approximation, horizontal, vertical, diagonal]
    Ref: P. Hill, A. Achim, et al. "Contrast Sensitivity of the Wavelet, Dual Tree Complex Wavelet, Curvelet, and Steerable Pyramid Transforms"
    '''
    if level <= 4 and pic_height == 1080:
        lookup = np.array([[ 0.36755274,  0.08655904,  0.08655904,  0.03830355],
                           [-0.09872951, -0.33820268, -0.33820268,  0.10885236],
                           [-0.04965274, -0.06836095, -0.06836095, -0.20426743],
                           [-0.03661276, -0.04262307, -0.04262307, -0.0619592 ],
                           [-0.03159788, -0.03394834, -0.03394834, -0.04074054]])
        return lookup[level, subband]
    else:
        # Detection threshold model parameters
        a = 2.818
        k = 0.783
        f0 = 0.578
        gs = [1.5, 1, 1, 0.555]  # g0, i.e. for approximation subband, is not provided. Using value from Watson (ref: watson). Use with caution.

        # Distance to height ratio of the display
        d2h = 3.0
        factor = np.pi*pic_height*d2h/180
        level_frequency = factor / (1 << (level+1))

        return 1.0 / (20 * np.log10(detection_threshold(a, k, f0, gs[subband], level_frequency) / 128))


def ahc_weight(level, subband, n_levels, binarized=True, channel=0):
    '''
    Weighting function used in Adaptive High Frequency Clipping
    If binarized is True, weight is compared to a threshold and 0-1 outputs are returned.
    Ref: K. Gu, G. Zhai, et al. "Adaptive High Frequency Clipping for Improved Image Quality Assessment"
    '''
    # Weighting function parameters
    a = 10
    k = 10
    t = 2
    d0 = 512
    gs = [1, 2, 2, 1]  # g0, i.e. for approximation subband, is not provided. Guessing. Do not use recommend using.
    thresh = 1.0

    # Distance to height ratio of the display
    d2h = 3.0

    weight = gs[subband] * np.power(k, t*(n_levels - (level+1))) / np.power(a,  d2h/d0)  # Paper says "d/d0" but I think they meant to use d2h
    if binarized:
        weight = float(weight >= thresh)

    return weight


csf_dict = {'ngan': ngan,
            'ngan_spat': ngan_spat,
            'li': li,
            'mannos': mannos,
            'mannos_weight': mannos_weight,
            'nadenau': nadenau,
            'nadenau_spat': nadenau_spat,
            'nadenau_weight': nadenau_weight,
            'watson': watson,
            'hill': hill,
            'ahc': ahc_weight}

frequency_csfs = ['ngan', ngan,
                  'mannos', mannos,
                  'nadenau', nadenau]

spatial_csfs = ['ngan_spat', ngan_spat,
                'nadenau_spat', nadenau_spat]

wavelet_csfs = ['li', li,
                'mannos_weight', mannos_weight,
                'nadenau_weight', nadenau_weight,
                'watson', watson,
                'hill', hill,
                'ahc', ahc_weight]