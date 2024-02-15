import numpy as np
from .vif_utils import integral_image
from .gsm_utils import complex_gsm_model, gsm_model


def rred_entropies_and_scales(subband, block_size=3):
    sigma_nsq = 0.1
    tol = 1e-10

    if block_size == 1:
        entr_const = np.log(2*np.pi*np.exp(1))
        sigma_nsq = 0.1
        k = 9
        k_norm = k**2
        x_pad = np.pad(subband, int((k - 1)/2), mode='reflect')
        int_1_x = integral_image(x_pad)
        int_2_x = integral_image(x_pad*x_pad)
        mu_x = (int_1_x[:-k, :-k] - int_1_x[:-k, k:] - int_1_x[k:, :-k] + int_1_x[k:, k:])/k_norm
        var_x = (int_2_x[:-k, :-k] - int_2_x[:-k, k:] - int_2_x[k:, :-k] + int_2_x[k:, k:])/k_norm - mu_x**2
        var_x = np.clip(var_x, 0, None)
        entropies = np.log(var_x + sigma_nsq) + entr_const
        scales = np.log(1 + var_x)
    else:
        if np.iscomplexobj(subband):
            s, cov, rel = complex_gsm_model(subband, block_size)
            cov_x = 0.5*(np.real(cov) + np.real(rel))
            cov_y = 0.5*(np.real(cov) - np.real(rel))
            cov_xy = 0.5*(np.imag(rel) - np.imag(cov))
            cov_real = np.block([[cov_x, cov_xy], [cov_xy.T, cov_y]])
            lamda, _ = np.linalg.eigh(cov_real)
            lamda[lamda < tol] = tol
        else:
            s, lamda, cov = gsm_model(subband, block_size)

        n_eigs = (2 if np.iscomplexobj(subband) else 1)*block_size*block_size

        entropies = np.zeros_like(s)
        for j in range(n_eigs):
            entropies = entropies + np.log(s*lamda[j]+sigma_nsq) + np.log(2*np.pi*np.exp(1))
        scales = np.log(1 + s)

    return entropies, scales

def rred_entropies_and_scales_low_dynamic_range(subband, block_size=3):
    sigma_nsq = 0.01
    tol = 1e-10

    if block_size == 1:
        entr_const = np.log(2*np.pi*np.exp(1))
        sigma_nsq = 0.01
        k = 9
        k_norm = k**2
        x_pad = np.pad(subband, int((k - 1)/2), mode='reflect')
        int_1_x = integral_image(x_pad)
        int_2_x = integral_image(x_pad*x_pad)
        mu_x = (int_1_x[:-k, :-k] - int_1_x[:-k, k:] - int_1_x[k:, :-k] + int_1_x[k:, k:])/k_norm
        var_x = (int_2_x[:-k, :-k] - int_2_x[:-k, k:] - int_2_x[k:, :-k] + int_2_x[k:, k:])/k_norm - mu_x**2
        var_x = np.clip(var_x, 0, None)
        entropies = np.log(var_x + sigma_nsq) + entr_const
        scales = np.log(0.1 + var_x)
    else:
        if np.iscomplexobj(subband):
            s, cov, rel = complex_gsm_model(subband, block_size)
            cov_x = 0.5*(np.real(cov) + np.real(rel))
            cov_y = 0.5*(np.real(cov) - np.real(rel))
            cov_xy = 0.5*(np.imag(rel) - np.imag(cov))
            cov_real = np.block([[cov_x, cov_xy], [cov_xy.T, cov_y]])
            lamda, _ = np.linalg.eigh(cov_real)
            lamda[lamda < tol] = tol
        else:
            s, lamda, cov = gsm_model(subband, block_size)

        n_eigs = (2 if np.iscomplexobj(subband) else 1)*block_size*block_size

        entropies = np.zeros_like(s)
        for j in range(n_eigs):
            entropies = entropies + np.log(s*lamda[j]+sigma_nsq) + np.log(2*np.pi*np.exp(1))
        scales = np.log(1 + s)

    return entropies, scales