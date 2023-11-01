import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

font = {'family' : 'normal',
        'size'   : 11}

matplotlib.rc('font', **font)

mean_times = [
    29.384,
    6.462,
    1047.35,
    43.378,
    612.594,
    561.524,
    84.404,
    737.774,
    13.79,
    61.368,
    7.684,
    79.754,
    21.96
]
mean_times = np.array(mean_times)/150

sroccs = [
    0.6685,
    0.7024,
    0.7082,
    0.7849,
    0.7603,
    0.7956,
    0.8312,
    0.8377,
    0.8409,
    0.8484,
    0.8660,
    0.8707,
    0.8754
]

algs = [
    'SSIM',
    'PSNR',
    'FSIM',
    'MS-SSIM',
    'ST-VMAF',
    'Ens-VMAF',
    'VMAF',
    'Enh-VMAF',
    'FUNQUE',
    'FS-Y-FUNQUE+',
    'Y-FUNQUE+',
    'FS-3C-FUNQUE+',
    '3C-FUNQUE+'
]

plt.figure(figsize=(6.4, 4.8), dpi=1000)
fig, ax = plt.subplots()

ax.scatter(mean_times[:1], sroccs[:1], color='royalblue', label='Atomic Models')
ax.scatter(mean_times[1:4], sroccs[1:4], color='royalblue')
ax.scatter(mean_times[4:5], sroccs[4:5], color='orange', label='Fusion Models')
ax.scatter(mean_times[5:8], sroccs[5:8], color='orange')
ax.scatter(mean_times[8:9], sroccs[8:9], color='darkgreen', label='FUNQUE Models' )
ax.scatter(mean_times[9:], sroccs[9:], color='darkgreen')

ax.set_xscale('log')
ax.xaxis.set_major_formatter(ScalarFormatter())

for mean_time, srocc, alg in zip(mean_times, sroccs, algs):
    # if alg not in ['Enh-VMAF', 'FSIM']:
    ax.annotate(alg, (mean_time*1.1, srocc-0.002))
    # elif alg == 'Enh-VMAF':
    #     ax.annotate(alg, (mean_time*0.5, srocc*0.985))
    # elif alg == 'FSIM':
    #     ax.annotate(alg, (mean_time*0.6, srocc))

ax.set_xlabel('Avg. time per frame (s)')
ax.set_ylabel('Avg. Test SROCC')
ax.set_xlim([0.03, 14])
ax.set_xticks([0.1, 1, 10], [0.1, 1, 10])

ax.legend(bbox_to_anchor=(0.5, 0.3), loc='center')

plt.savefig('plots/srocc_v_time.png')


