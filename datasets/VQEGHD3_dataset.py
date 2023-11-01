from videolib import standards

dataset_name = 'VQEGHD3'

path_to_dataset = '[path to dataset]'

width = 1920
height = 1080

ref_standard = standards.sRGB
dis_standard = standards.sRGB

ref_videos = {1: {
               'content_name': 'vqeghd3_src01',
               'path': path_to_dataset + '/vqeghd3_src01_original.yuv'},
              2: {
               'content_name': 'vqeghd3_src02',
               'path': path_to_dataset + '/vqeghd3_src02_original.yuv'},
              3: {
               'content_name': 'vqeghd3_src03',
               'path': path_to_dataset + '/vqeghd3_src03_original.yuv'},
              4: {
               'content_name': 'vqeghd3_src04',
               'path': path_to_dataset + '/vqeghd3_src04_original.yuv'},
              5: {
               'content_name': 'vqeghd3_src05',
               'path': path_to_dataset + '/vqeghd3_src05_original.yuv'},
              6: {
               'content_name': 'vqeghd3_src06',
               'path': path_to_dataset + '/vqeghd3_src06_original.yuv'},
              7: {
               'content_name': 'vqeghd3_src07',
               'path': path_to_dataset + '/vqeghd3_src07_original.yuv'},
              8: {
               'content_name': 'vqeghd3_src08',
               'path': path_to_dataset + '/vqeghd3_src08_original.yuv'},
              9: {
               'content_name': 'vqeghd3_src09',
               'path': path_to_dataset + '/vqeghd3_src09_original.yuv'}}

dis_videos = {1: {
               'content_id': 1,
               'score': 100.0,
               'path': path_to_dataset + '/vqeghd3_src01_hrc04.yuv'},
              3: {
               'content_id': 1,
               'score': 95.0,
               'path': path_to_dataset + '/vqeghd3_src01_hrc07.yuv'},
              9: {
               'content_id': 1,
               'score': 42.5,
               'path': path_to_dataset + '/vqeghd3_src01_hrc16.yuv'},
              10: {
               'content_id': 1,
               'score': 51.666666660000004,
               'path': path_to_dataset + '/vqeghd3_src01_hrc17.yuv'},
              11: {
               'content_id': 1,
               'score': 42.5,
               'path': path_to_dataset + '/vqeghd3_src01_hrc18.yuv'},
              12: {
               'content_id': 1,
               'score': 66.66666666,
               'path': path_to_dataset + '/vqeghd3_src01_hrc19.yuv'},
              13: {
               'content_id': 1,
               'score': 76.66666666,
               'path': path_to_dataset + '/vqeghd3_src01_hrc20.yuv'},
              14: {
               'content_id': 1,
               'score': 90.83333334000001,
               'path': path_to_dataset + '/vqeghd3_src01_hrc21.yuv'},
              16: {
               'content_id': 2,
               'score': 97.5,
               'path': path_to_dataset + '/vqeghd3_src02_hrc04.yuv'},
              18: {
               'content_id': 2,
               'score': 100.0,
               'path': path_to_dataset + '/vqeghd3_src02_hrc07.yuv'},
              24: {
               'content_id': 2,
               'score': 43.333333339999996,
               'path': path_to_dataset + '/vqeghd3_src02_hrc16.yuv'},
              25: {
               'content_id': 2,
               'score': 45.833333339999996,
               'path': path_to_dataset + '/vqeghd3_src02_hrc17.yuv'},
              26: {
               'content_id': 2,
               'score': 57.5,
               'path': path_to_dataset + '/vqeghd3_src02_hrc18.yuv'},
              27: {
               'content_id': 2,
               'score': 69.16666666,
               'path': path_to_dataset + '/vqeghd3_src02_hrc19.yuv'},
              28: {
               'content_id': 2,
               'score': 84.16666665999999,
               'path': path_to_dataset + '/vqeghd3_src02_hrc20.yuv'},
              29: {
               'content_id': 2,
               'score': 90.0,
               'path': path_to_dataset + '/vqeghd3_src02_hrc21.yuv'},
              31: {
               'content_id': 3,
               'score': 99.16666665999999,
               'path': path_to_dataset + '/vqeghd3_src03_hrc04.yuv'},
              33: {
               'content_id': 3,
               'score': 100.0,
               'path': path_to_dataset + '/vqeghd3_src03_hrc07.yuv'},
              39: {
               'content_id': 3,
               'score': 50.0,
               'path': path_to_dataset + '/vqeghd3_src03_hrc16.yuv'},
              40: {
               'content_id': 3,
               'score': 59.166666660000004,
               'path': path_to_dataset + '/vqeghd3_src03_hrc17.yuv'},
              41: {
               'content_id': 3,
               'score': 66.66666666,
               'path': path_to_dataset + '/vqeghd3_src03_hrc18.yuv'},
              42: {
               'content_id': 3,
               'score': 85.0,
               'path': path_to_dataset + '/vqeghd3_src03_hrc19.yuv'},
              43: {
               'content_id': 3,
               'score': 91.66666665999999,
               'path': path_to_dataset + '/vqeghd3_src03_hrc20.yuv'},
              44: {
               'content_id': 3,
               'score': 95.83333334000001,
               'path': path_to_dataset + '/vqeghd3_src03_hrc21.yuv'},
              51: {
               'content_id': 4,
               'score': 97.5,
               'path': path_to_dataset + '/vqeghd3_src04_hrc04.yuv'},
              52: {
               'content_id': 4,
               'score': 99.16666667,
               'path': path_to_dataset + '/vqeghd3_src04_hrc07.yuv'},
              53: {
               'content_id': 4,
               'score': 59.16666667,
               'path': path_to_dataset + '/vqeghd3_src04_hrc16.yuv'},
              54: {
               'content_id': 4,
               'score': 65,
               'path': path_to_dataset + '/vqeghd3_src04_hrc17.yuv'},
              55: {
               'content_id': 4,
               'score': 78.333333336,
               'path': path_to_dataset + '/vqeghd3_src04_hrc18.yuv'},
              56: {
               'content_id': 4,
               'score': 87.5,
               'path': path_to_dataset + '/vqeghd3_src04_hrc19.yuv'},
              57: {
               'content_id': 4,
               'score': 89.16666667,
               'path': path_to_dataset + '/vqeghd3_src04_hrc20.yuv'},
              58: {
               'content_id': 4,
               'score': 94.16666667,
               'path': path_to_dataset + '/vqeghd3_src04_hrc21.yuv'},
              61: {
               'content_id': 5,
               'score': 100.83333334000001,
               'path': path_to_dataset + '/vqeghd3_src05_hrc04.yuv'},
              63: {
               'content_id': 5,
               'score': 93.33333334000001,
               'path': path_to_dataset + '/vqeghd3_src05_hrc07.yuv'},
              69: {
               'content_id': 5,
               'score': 42.5,
               'path': path_to_dataset + '/vqeghd3_src05_hrc16.yuv'},
              70: {
               'content_id': 5,
               'score': 48.333333339999996,
               'path': path_to_dataset + '/vqeghd3_src05_hrc17.yuv'},
              71: {
               'content_id': 5,
               'score': 60.0,
               'path': path_to_dataset + '/vqeghd3_src05_hrc18.yuv'},
              72: {
               'content_id': 5,
               'score': 76.66666666,
               'path': path_to_dataset + '/vqeghd3_src05_hrc19.yuv'},
              73: {
               'content_id': 5,
               'score': 88.33333334000001,
               'path': path_to_dataset + '/vqeghd3_src05_hrc20.yuv'},
              74: {
               'content_id': 5,
               'score': 90.83333334000001,
               'path': path_to_dataset + '/vqeghd3_src05_hrc21.yuv'},
              76: {
               'content_id': 6,
               'score': 99.16666665999999,
               'path': path_to_dataset + '/vqeghd3_src06_hrc04.yuv'},
              80: {
               'content_id': 6,
               'score': 35.83333334,
               'path': path_to_dataset + '/vqeghd3_src06_hrc07.yuv'},
              83: {
               'content_id': 6,
               'score': 48.333333339999996,
               'path': path_to_dataset + '/vqeghd3_src06_hrc16.yuv'},
              84: {
               'content_id': 6,
               'score': 54.166666660000004,
               'path': path_to_dataset + '/vqeghd3_src06_hrc17.yuv'},
              85: {
               'content_id': 6,
               'score': 52.5,
               'path': path_to_dataset + '/vqeghd3_src06_hrc18.yuv'},
              86: {
               'content_id': 6,
               'score': 74.16666666,
               'path': path_to_dataset + '/vqeghd3_src06_hrc19.yuv'},
              87: {
               'content_id': 6,
               'score': 85.83333334000001,
               'path': path_to_dataset + '/vqeghd3_src06_hrc20.yuv'},
              88: {
               'content_id': 6,
               'score': 97.5,
               'path': path_to_dataset + '/vqeghd3_src06_hrc21.yuv'},
              90: {
               'content_id': 7,
               'score': 104.16666665999999,
               'path': path_to_dataset + '/vqeghd3_src07_hrc04.yuv'},
              92: {
               'content_id': 7,
               'score': 96.66666665999999,
               'path': path_to_dataset + '/vqeghd3_src07_hrc07.yuv'},
              98: {
               'content_id': 7,
               'score': 51.666666660000004,
               'path': path_to_dataset + '/vqeghd3_src07_hrc16.yuv'},
              99: {
               'content_id': 7,
               'score': 58.333333339999996,
               'path': path_to_dataset + '/vqeghd3_src07_hrc17.yuv'},
              100: {
               'content_id': 7,
               'score': 66.66666666,
               'path': path_to_dataset + '/vqeghd3_src07_hrc18.yuv'},
              101: {
               'content_id': 7,
               'score': 81.66666665999999,
               'path': path_to_dataset + '/vqeghd3_src07_hrc19.yuv'},
              102: {
               'content_id': 7,
               'score': 88.33333334000001,
               'path': path_to_dataset + '/vqeghd3_src07_hrc20.yuv'},
              103: {
               'content_id': 7,
               'score': 93.33333334000001,
               'path': path_to_dataset + '/vqeghd3_src07_hrc21.yuv'},
              105: {
               'content_id': 8,
               'score': 103.33333334000001,
               'path': path_to_dataset + '/vqeghd3_src08_hrc04.yuv'},
              107: {
               'content_id': 8,
               'score': 101.66666665999999,
               'path': path_to_dataset + '/vqeghd3_src08_hrc07.yuv'},
              113: {
               'content_id': 8,
               'score': 47.5,
               'path': path_to_dataset + '/vqeghd3_src08_hrc16.yuv'},
              114: {
               'content_id': 8,
               'score': 52.5,
               'path': path_to_dataset + '/vqeghd3_src08_hrc17.yuv'},
              115: {
               'content_id': 8,
               'score': 56.666666660000004,
               'path': path_to_dataset + '/vqeghd3_src08_hrc18.yuv'},
              116: {
               'content_id': 8,
               'score': 70.83333334,
               'path': path_to_dataset + '/vqeghd3_src08_hrc19.yuv'},
              117: {
               'content_id': 8,
               'score': 80.0,
               'path': path_to_dataset + '/vqeghd3_src08_hrc20.yuv'},
              118: {
               'content_id': 8,
               'score': 85.83333334000001,
               'path': path_to_dataset + '/vqeghd3_src08_hrc21.yuv'},
              120: {
               'content_id': 9,
               'score': 101.66666665999999,
               'path': path_to_dataset + '/vqeghd3_src09_hrc04.yuv'},
              122: {
               'content_id': 9,
               'score': 98.33333334000001,
               'path': path_to_dataset + '/vqeghd3_src09_hrc07.yuv'},
              128: {
               'content_id': 9,
               'score': 56.666666660000004,
               'path': path_to_dataset + '/vqeghd3_src09_hrc16.yuv'},
              129: {
               'content_id': 9,
               'score': 56.666666660000004,
               'path': path_to_dataset + '/vqeghd3_src09_hrc17.yuv'},
              130: {
               'content_id': 9,
               'score': 65.0,
               'path': path_to_dataset + '/vqeghd3_src09_hrc18.yuv'},
              131: {
               'content_id': 9,
               'score': 78.33333334,
               'path': path_to_dataset + '/vqeghd3_src09_hrc19.yuv'},
              132: {
               'content_id': 9,
               'score': 87.5,
               'path': path_to_dataset + '/vqeghd3_src09_hrc20.yuv'},
              133: {
               'content_id': 9,
               'score': 100.0,
               'path': path_to_dataset + '/vqeghd3_src09_hrc21.yuv'}}