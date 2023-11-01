from videolib import standards

dataset_name = 'MCL_V'

path_to_dataset = '[path to dataset]'
ref_dir = path_to_dataset + '/reference_sequences'
dis_dir = path_to_dataset + '/distorted_sequences'

width = 1920
height = 1080

ref_standard = standards.sRGB
dis_standard = standards.sRGB

ref_videos = {0: {
               'content_name': 'BQTerrace',
               'path': ref_dir + '/BQTerrace_30fps.yuv'},
              1: {
               'content_name': 'BigBuckBunny',
               'path': ref_dir + '/BigBuckBunny_25fps.yuv'},
              2: {
               'content_name': 'BirdsInCage',
               'path': ref_dir + '/BirdsInCage_30fps.yuv'},
              3: {
               'content_name': 'CrowdRun',
               'path': ref_dir + '/CrowdRun_25fps.yuv'},
              4: {
               'content_name': 'DanceKiss',
               'path': ref_dir + '/DanceKiss_25fps.yuv'},
              5: {
               'content_name': 'ElFuente1',
               'path': ref_dir + '/ElFuente1_30fps.yuv'},
              6: {
               'content_name': 'ElFuente2',
               'path': ref_dir + '/ElFuente2_30fps.yuv'},
              7: {
               'content_name': 'FoxBird',
               'path': ref_dir + '/FoxBird_25fps.yuv'},
              8: {
               'content_name': 'Kimono1',
               'path': ref_dir + '/Kimono1_24fps.yuv'},
              9: {
               'content_name': 'OldTownCross',
               'path': ref_dir + '/OldTownCross_25fps.yuv'},
              10: {
               'content_name': 'Seeking',
               'path': ref_dir + '/Seeking_25fps.yuv'},
              11: {
               'content_name': 'Tennis',
               'path': ref_dir + '/Tennis_24fps.yuv'}}

dis_videos = {0: {
               'content_id': 1,
               'score': 66.72413793103448,
               'path': dis_dir + '/BigBuckBunny_25fps_H264_4.yuv'},
              1: {
               'content_id': 1,
               'score': 58.9655172413793,
               'path': dis_dir + '/BigBuckBunny_25fps_SDH264HD_4.yuv'},
              2: {
               'content_id': 1,
               'score': 49.310344827586206,
               'path': dis_dir + '/BigBuckBunny_25fps_H264_3.yuv'},
              3: {
               'content_id': 1,
               'score': 44.13793103448276,
               'path': dis_dir + '/BigBuckBunny_25fps_SDH264HD_3.yuv'},
              4: {
               'content_id': 1,
               'score': 26.03448275862069,
               'path': dis_dir + '/BigBuckBunny_25fps_H264_2.yuv'},
              5: {
               'content_id': 1,
               'score': 22.93103448275862,
               'path': dis_dir + '/BigBuckBunny_25fps_SDH264HD_2.yuv'},
              6: {
               'content_id': 1,
               'score': 7.586206896551724,
               'path': dis_dir + '/BigBuckBunny_25fps_H264_1.yuv'},
              7: {
               'content_id': 1,
               'score': 3.4482758620689657,
               'path': dis_dir + '/BigBuckBunny_25fps_SDH264HD_1.yuv'},
              8: {
               'content_id': 2,
               'score': 70.6896551724138,
               'path': dis_dir + '/BirdsInCage_30fps_H264_4.yuv'},
              9: {
               'content_id': 2,
               'score': 57.06896551724138,
               'path': dis_dir + '/BirdsInCage_30fps_SDH264HD_4.yuv'},
              10: {
               'content_id': 2,
               'score': 53.44827586206897,
               'path': dis_dir + '/BirdsInCage_30fps_H264_3.yuv'},
              11: {
               'content_id': 2,
               'score': 36.724137931034484,
               'path': dis_dir + '/BirdsInCage_30fps_SDH264HD_3.yuv'},
              12: {
               'content_id': 2,
               'score': 34.310344827586206,
               'path': dis_dir + '/BirdsInCage_30fps_H264_2.yuv'},
              13: {
               'content_id': 2,
               'score': 12.931034482758621,
               'path': dis_dir + '/BirdsInCage_30fps_SDH264HD_2.yuv'},
              14: {
               'content_id': 2,
               'score': 11.03448275862069,
               'path': dis_dir + '/BirdsInCage_30fps_H264_1.yuv'},
              15: {
               'content_id': 2,
               'score': 6.379310344827587,
               'path': dis_dir + '/BirdsInCage_30fps_SDH264HD_1.yuv'},
              16: {
               'content_id': 0,
               'score': 69.65517241379311,
               'path': dis_dir + '/BQTerrace_30fps_H264_4.yuv'},
              17: {
               'content_id': 0,
               'score': 56.55172413793103,
               'path': dis_dir + '/BQTerrace_30fps_SDH264HD_4.yuv'},
              18: {
               'content_id': 0,
               'score': 53.62068965517241,
               'path': dis_dir + '/BQTerrace_30fps_H264_3.yuv'},
              19: {
               'content_id': 0,
               'score': 38.793103448275865,
               'path': dis_dir + '/BQTerrace_30fps_SDH264HD_3.yuv'},
              20: {
               'content_id': 0,
               'score': 31.551724137931036,
               'path': dis_dir + '/BQTerrace_30fps_H264_2.yuv'},
              21: {
               'content_id': 0,
               'score': 18.793103448275865,
               'path': dis_dir + '/BQTerrace_30fps_SDH264HD_2.yuv'},
              22: {
               'content_id': 0,
               'score': 8.96551724137931,
               'path': dis_dir + '/BQTerrace_30fps_H264_1.yuv'},
              23: {
               'content_id': 0,
               'score': 3.4482758620689657,
               'path': dis_dir + '/BQTerrace_30fps_SDH264HD_1.yuv'},
              24: {
               'content_id': 3,
               'score': 69.13793103448276,
               'path': dis_dir + '/CrowdRun_25fps_H264_4.yuv'},
              25: {
               'content_id': 3,
               'score': 56.37931034482759,
               'path': dis_dir + '/CrowdRun_25fps_SDH264HD_4.yuv'},
              26: {
               'content_id': 3,
               'score': 53.793103448275865,
               'path': dis_dir + '/CrowdRun_25fps_H264_3.yuv'},
              27: {
               'content_id': 3,
               'score': 38.62068965517241,
               'path': dis_dir + '/CrowdRun_25fps_SDH264HD_3.yuv'},
              28: {
               'content_id': 3,
               'score': 31.551724137931036,
               'path': dis_dir + '/CrowdRun_25fps_H264_2.yuv'},
              29: {
               'content_id': 3,
               'score': 19.82758620689655,
               'path': dis_dir + '/CrowdRun_25fps_SDH264HD_2.yuv'},
              30: {
               'content_id': 3,
               'score': 10.517241379310345,
               'path': dis_dir + '/CrowdRun_25fps_H264_1.yuv'},
              31: {
               'content_id': 3,
               'score': 2.9310344827586206,
               'path': dis_dir + '/CrowdRun_25fps_SDH264HD_1.yuv'},
              32: {
               'content_id': 4,
               'score': 66.2962962962963,
               'path': dis_dir + '/DanceKiss_25fps_H264_4.yuv'},
              33: {
               'content_id': 4,
               'score': 62.03703703703703,
               'path': dis_dir + '/DanceKiss_25fps_SDH264HD_4.yuv'},
              34: {
               'content_id': 4,
               'score': 46.11111111111111,
               'path': dis_dir + '/DanceKiss_25fps_H264_3.yuv'},
              35: {
               'content_id': 4,
               'score': 46.2962962962963,
               'path': dis_dir + '/DanceKiss_25fps_SDH264HD_3.yuv'},
              36: {
               'content_id': 4,
               'score': 25.925925925925924,
               'path': dis_dir + '/DanceKiss_25fps_H264_2.yuv'},
              37: {
               'content_id': 4,
               'score': 23.518518518518515,
               'path': dis_dir + '/DanceKiss_25fps_SDH264HD_2.yuv'},
              38: {
               'content_id': 4,
               'score': 3.5185185185185186,
               'path': dis_dir + '/DanceKiss_25fps_H264_1.yuv'},
              39: {
               'content_id': 4,
               'score': 7.962962962962963,
               'path': dis_dir + '/DanceKiss_25fps_SDH264HD_1.yuv'},
              40: {
               'content_id': 5,
               'score': 68.14814814814815,
               'path': dis_dir + '/ElFuente1_30fps_H264_4.yuv'},
              41: {
               'content_id': 5,
               'score': 60.370370370370374,
               'path': dis_dir + '/ElFuente1_30fps_SDH264HD_4.yuv'},
              42: {
               'content_id': 5,
               'score': 46.66666666666667,
               'path': dis_dir + '/ElFuente1_30fps_H264_3.yuv'},
              43: {
               'content_id': 5,
               'score': 44.25925925925925,
               'path': dis_dir + '/ElFuente1_30fps_SDH264HD_3.yuv'},
              44: {
               'content_id': 5,
               'score': 28.703703703703702,
               'path': dis_dir + '/ElFuente1_30fps_H264_2.yuv'},
              45: {
               'content_id': 5,
               'score': 22.40740740740741,
               'path': dis_dir + '/ElFuente1_30fps_SDH264HD_2.yuv'},
              46: {
               'content_id': 5,
               'score': 2.962962962962963,
               'path': dis_dir + '/ElFuente1_30fps_H264_1.yuv'},
              47: {
               'content_id': 5,
               'score': 7.4074074074074066,
               'path': dis_dir + '/ElFuente1_30fps_SDH264HD_1.yuv'},
              48: {
               'content_id': 6,
               'score': 64.25925925925925,
               'path': dis_dir + '/ElFuente2_30fps_H264_4.yuv'},
              49: {
               'content_id': 6,
               'score': 61.11111111111111,
               'path': dis_dir + '/ElFuente2_30fps_SDH264HD_4.yuv'},
              50: {
               'content_id': 6,
               'score': 45.0,
               'path': dis_dir + '/ElFuente2_30fps_H264_3.yuv'},
              51: {
               'content_id': 6,
               'score': 44.25925925925925,
               'path': dis_dir + '/ElFuente2_30fps_SDH264HD_3.yuv'},
              52: {
               'content_id': 6,
               'score': 28.518518518518515,
               'path': dis_dir + '/ElFuente2_30fps_H264_2.yuv'},
              53: {
               'content_id': 6,
               'score': 24.629629629629626,
               'path': dis_dir + '/ElFuente2_30fps_SDH264HD_2.yuv'},
              54: {
               'content_id': 6,
               'score': 7.037037037037037,
               'path': dis_dir + '/ElFuente2_30fps_H264_1.yuv'},
              55: {
               'content_id': 6,
               'score': 4.444444444444445,
               'path': dis_dir + '/ElFuente2_30fps_SDH264HD_1.yuv'},
              56: {
               'content_id': 8,
               'score': 69.25925925925925,
               'path': dis_dir + '/Kimono1_24fps_H264_4.yuv'},
              57: {
               'content_id': 8,
               'score': 61.48148148148148,
               'path': dis_dir + '/Kimono1_24fps_SDH264HD_4.yuv'},
              58: {
               'content_id': 8,
               'score': 48.51851851851852,
               'path': dis_dir + '/Kimono1_24fps_H264_3.yuv'},
              59: {
               'content_id': 8,
               'score': 42.96296296296297,
               'path': dis_dir + '/Kimono1_24fps_SDH264HD_3.yuv'},
              60: {
               'content_id': 8,
               'score': 26.11111111111111,
               'path': dis_dir + '/Kimono1_24fps_H264_2.yuv'},
              61: {
               'content_id': 8,
               'score': 23.14814814814815,
               'path': dis_dir + '/Kimono1_24fps_SDH264HD_2.yuv'},
              62: {
               'content_id': 8,
               'score': 7.962962962962963,
               'path': dis_dir + '/Kimono1_24fps_H264_1.yuv'},
              63: {
               'content_id': 8,
               'score': 3.333333333333333,
               'path': dis_dir + '/Kimono1_24fps_SDH264HD_1.yuv'},
              64: {
               'content_id': 7,
               'score': 65.76923076923077,
               'path': dis_dir + '/FoxBird_25fps_H264_4.yuv'},
              65: {
               'content_id': 7,
               'score': 63.846153846153854,
               'path': dis_dir + '/FoxBird_25fps_SDH264HD_4.yuv'},
              66: {
               'content_id': 7,
               'score': 43.46153846153846,
               'path': dis_dir + '/FoxBird_25fps_H264_3.yuv'},
              67: {
               'content_id': 7,
               'score': 45.96153846153846,
               'path': dis_dir + '/FoxBird_25fps_SDH264HD_3.yuv'},
              68: {
               'content_id': 7,
               'score': 28.846153846153847,
               'path': dis_dir + '/FoxBird_25fps_H264_2.yuv'},
              69: {
               'content_id': 7,
               'score': 15.0,
               'path': dis_dir + '/FoxBird_25fps_SDH264HD_2.yuv'},
              70: {
               'content_id': 7,
               'score': 16.153846153846153,
               'path': dis_dir + '/FoxBird_25fps_H264_1.yuv'},
              71: {
               'content_id': 7,
               'score': 0.7692307692307693,
               'path': dis_dir + '/FoxBird_25fps_SDH264HD_1.yuv'},
              72: {
               'content_id': 9,
               'score': 70.76923076923077,
               'path': dis_dir + '/OldTownCross_25fps_H264_4.yuv'},
              73: {
               'content_id': 9,
               'score': 57.11538461538461,
               'path': dis_dir + '/OldTownCross_25fps_SDH264HD_4.yuv'},
              74: {
               'content_id': 9,
               'score': 55.76923076923077,
               'path': dis_dir + '/OldTownCross_25fps_H264_3.yuv'},
              75: {
               'content_id': 9,
               'score': 40,
               'path': dis_dir + '/OldTownCross_25fps_SDH264HD_3.yuv'},
              76: {
               'content_id': 9,
               'score': 32.30769230769231,
               'path': dis_dir + '/OldTownCross_25fps_H264_2.yuv'},
              77: {
               'content_id': 9,
               'score': 19.038461538461537,
               'path': dis_dir + '/OldTownCross_25fps_SDH264HD_2.yuv'},
              78: {
               'content_id': 9,
               'score': 9.230769230769232,
               'path': dis_dir + '/OldTownCross_25fps_H264_1.yuv'},
              79: {
               'content_id': 9,
               'score': 2.5,
               'path': dis_dir + '/OldTownCross_25fps_SDH264HD_1.yuv'},
              80: {
               'content_id': 10,
               'score': 68.07692307692308,
               'path': dis_dir + '/Seeking_25fps_H264_4.yuv'},
              81: {
               'content_id': 10,
               'score': 61.73076923076923,
               'path': dis_dir + '/Seeking_25fps_SDH264HD_4.yuv'},
              82: {
               'content_id': 10,
               'score': 49.03846153846154,
               'path': dis_dir + '/Seeking_25fps_H264_3.yuv'},
              83: {
               'content_id': 10,
               'score': 40.38461538461539,
               'path': dis_dir + '/Seeking_25fps_SDH264HD_3.yuv'},
              84: {
               'content_id': 10,
               'score': 30,
               'path': dis_dir + '/Seeking_25fps_H264_2.yuv'},
              85: {
               'content_id': 10,
               'score': 21.346153846153847,
               'path': dis_dir + '/Seeking_25fps_SDH264HD_2.yuv'},
              86: {
               'content_id': 10,
               'score': 8.653846153846153,
               'path': dis_dir + '/Seeking_25fps_H264_1.yuv'},
              87: {
               'content_id': 10,
               'score': 3.076923076923077,
               'path': dis_dir + '/Seeking_25fps_SDH264HD_1.yuv'},
              88: {
               'content_id': 11,
               'score': 69.23076923076923,
               'path': dis_dir + '/Tennis_24fps_H264_4.yuv'},
              89: {
               'content_id': 11,
               'score': 61.92307692307693,
               'path': dis_dir + '/Tennis_24fps_SDH264HD_4.yuv'},
              90: {
               'content_id': 11,
               'score': 45.19230769230769,
               'path': dis_dir + '/Tennis_24fps_H264_3.yuv'},
              91: {
               'content_id': 11,
               'score': 43.26923076923077,
               'path': dis_dir + '/Tennis_24fps_SDH264HD_3.yuv'},
              92: {
               'content_id': 11,
               'score': 26.538461538461537,
               'path': dis_dir + '/Tennis_24fps_H264_2.yuv'},
              93: {
               'content_id': 11,
               'score': 25.76923076923077,
               'path': dis_dir + '/Tennis_24fps_SDH264HD_2.yuv'},
              94: {
               'content_id': 11,
               'score': 3.4615384615384617,
               'path': dis_dir + '/Tennis_24fps_H264_1.yuv'},
              95: {
               'content_id': 11,
               'score': 6.923076923076923,
               'path': dis_dir + '/Tennis_24fps_SDH264HD_1.yuv'}}