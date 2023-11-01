import numpy as np
from scipy.ndimage import convolve1d
from .csf_utils import csf_dict, ngan, nadenau, mannos
from pywt import wavedec2, waverec2


def filter_pyr(pyr, csf_funct, channel=0):
    if csf_funct is None:
        return pyr
    elif isinstance(csf_funct, str):
        csf_funct = csf_dict[csf_funct]

    approxs, details = pyr  # Do not filter approx subbands.
    n_levels = len(details)
    filt_details = []
    for lev, detail_level in enumerate(details):
        filt_level = []
        for sub, subband in enumerate(detail_level):
            if csf_funct.__name__ != 'ahc_weight':
                filt_level.append(subband * csf_funct(lev, sub+1, channel=channel))
            else:
                filt_level.append(subband * csf_funct(lev, sub+1, n_levels, channel=channel))  # No approximation coefficient. Only H, V, D.
        filt_details.append(tuple(filt_level))
    return approxs, filt_details


def filter_img(img, filter_key, wavelet=None, channel=0, **kwargs):
    if filter_key is None:
        return img

    elif filter_key in ['ngan', 'ngan_rad', 'mannos', 'nadenau']:
        d2h = 3.0
        pic_height = 1080
        f_max = np.pi*pic_height*d2h/180
        h, w = img.shape
        u_min = -(h >> 1)
        u_max = (h >> 1) + 1 if h & 1 else (h >> 1)
        v_min = -(w >> 1)
        v_max = (w >> 1) + 1 if w & 1 else (w >> 1)

        u, v = np.meshgrid(np.arange(u_min, u_max), np.arange(v_min, v_max), indexing='ij')
        fx, fy = u*f_max/h, v*f_max/w

        if filter_key == 'ngan':
            csf_mat = ngan(np.abs(fx)) * ngan(np.abs(fy))  # Separable filtering
        elif filter_key == 'ngan_rad':
            f_mat = np.sqrt(fx**2 + fy**2)
            csf_mat = ngan(f_mat)
        elif filter_key == 'mannos':
            f_mat = np.sqrt(fx**2 + fy**2)
            theta_mat = np.arctan2(v, u)
            csf_mat = mannos(f_mat, theta_mat)
        elif filter_key == 'nadenau':
            csf_mat = nadenau(np.abs(fx), channel=channel) * nadenau(np.abs(fy), channel=channel)  # Separable filtering

        img_filtered = np.fft.ifft2(np.fft.ifftshift(np.fft.fftshift(np.fft.fft2(img)) * csf_mat))

    elif filter_key in ['li', 'watson', 'ahc', 'hill', 'mannos_weight']:
        n_levels = 4
        pyr = wavedec2(img, wavelet, 'reflect', n_levels)
        csf_funct = csf_dict[filter_key]

        pyr_filtered = filter_pyr(pyr, csf_funct, channel=channel)
        img_filtered = waverec2(pyr_filtered, wavelet, 'reflect')

    elif filter_key in ['ngan_spat', 'ngan_spat_clipped', 'nadenau_spat', 'nadenau_spat_clipped']:
        d2h = 3.0
        filt_funct = csf_dict[filter_key.split('_clipped')[0]]
        if 'k' in kwargs:
            filt = filt_funct(d2h, k=kwargs['k'])
        else:
            filt = filt_funct(d2h)

        img_filtered = convolve1d(img, filt, axis=0)
        if 'clipped' in filter_key:
            img_filtered = np.clip(img_filtered, 0, None)

        img_filtered = convolve1d(img_filtered, filt, axis=1)
        if 'clipped' in filter_key:
            img_filtered = np.clip(img_filtered, 0, None)

    return np.real(img_filtered)
