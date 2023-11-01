from videolib import standards

dataset_name = 'IVP'

path_to_dataset = '[path to dataset]'
ref_dir = path_to_dataset + '/ref'
dis_dir = path_to_dataset + '/dis'

width = 1920
height = 1088

ref_standard = standards.sRGB
dis_standard = standards.sRGB

ref_videos = {0: {
               'content_name': 'bus',
               'path': ref_dir + '/bus.yuv'},
              1: {
               'content_name': 'laser',
               'path': ref_dir + '/laser.yuv'},
              2: {
               'content_name': 'overbridge',
               'path': ref_dir + '/overbridge.yuv'},
              3: {
               'content_name': 'robot',
               'path': ref_dir + '/robot.yuv'},
              4: {
               'content_name': 'shelf',
               'path': ref_dir + '/shelf.yuv'},
              5: {
               'content_name': 'square',
               'path': ref_dir + '/square.yuv'},
              6: {
               'content_name': 'toys',
               'path': ref_dir + '/toys_calendar.yuv'},
              7: {
               'content_name': 'tractor',
               'path': ref_dir + '/tractor.yuv'},
              8: {
               'content_name': 'train',
               'path': ref_dir + '/train.yuv'},
              9: {
               'content_name': 'tube',
               'path': ref_dir + '/tube.yuv'}}

dis_videos = {0: {
               'content_id': 0,
               'score': 0.9141,
               'path': dis_dir + '/bus_dirac_1.yuv'},
              1: {
               'content_id': 0,
               'score': 1.761,
               'path': dis_dir + '/bus_dirac_2.yuv'},
              2: {
               'content_id': 0,
               'score': 2.545,
               'path': dis_dir + '/bus_dirac_3.yuv'},
              3: {
               'content_id': 0,
               'score': -0.060209000000000006,
               'path': dis_dir + '/bus_h264_1.yuv'},
              4: {
               'content_id': 0,
               'score': 0.29378000000000004,
               'path': dis_dir + '/bus_h264_2.yuv'},
              5: {
               'content_id': 0,
               'score': 0.42517,
               'path': dis_dir + '/bus_h264_3.yuv'},
              6: {
               'content_id': 0,
               'score': 1.7095,
               'path': dis_dir + '/bus_h264_4.yuv'},
              7: {
               'content_id': 0,
               'score': 0.037114,
               'path': dis_dir + '/bus_mpeg2_1.yuv'},
              8: {
               'content_id': 0,
               'score': 0.61435,
               'path': dis_dir + '/bus_mpeg2_2.yuv'},
              9: {
               'content_id': 0,
               'score': 1.5951,
               'path': dis_dir + '/bus_mpeg2_3.yuv'},
              10: {
               'content_id': 1,
               'score': 1.0207,
               'path': dis_dir + '/laser_dirac_1.yuv'},
              11: {
               'content_id': 1,
               'score': 1.3519999999999999,
               'path': dis_dir + '/laser_dirac_2.yuv'},
              12: {
               'content_id': 1,
               'score': 2.2344,
               'path': dis_dir + '/laser_dirac_3.yuv'},
              13: {
               'content_id': 1,
               'score': -0.22218000000000002,
               'path': dis_dir + '/laser_h264_1.yuv'},
              14: {
               'content_id': 1,
               'score': -0.1119,
               'path': dis_dir + '/laser_h264_2.yuv'},
              15: {
               'content_id': 1,
               'score': 0.14479,
               'path': dis_dir + '/laser_h264_3.yuv'},
              16: {
               'content_id': 1,
               'score': 0.6521399999999999,
               'path': dis_dir + '/laser_h264_4.yuv'},
               17: {
               'content_id': 1,
               'score': 0.15281,
               'path': dis_dir + '/laser_mpeg2_1.yuv'},
              18: {
               'content_id': 1,
               'score': 0.13569,
               'path': dis_dir + '/laser_mpeg2_2.yuv'},
              19: {
               'content_id': 1,
               'score': 1.7343,
               'path': dis_dir + '/laser_mpeg2_3.yuv'},
              20: {
               'content_id': 2,
               'score': 1.0332,
               'path': dis_dir + '/overbridge_dirac_1.yuv'},
              21: {
               'content_id': 2,
               'score': 2.0277,
               'path': dis_dir + '/overbridge_dirac_2.yuv'},
              22: {
               'content_id': 2,
               'score': 2.6435,
               'path': dis_dir + '/overbridge_dirac_3.yuv'},
              23: {
               'content_id': 2,
               'score': 0.11780999999999998,
               'path': dis_dir + '/overbridge_h264_1.yuv'},
              24: {
               'content_id': 2,
               'score': 0.7609899999999999,
               'path': dis_dir + '/overbridge_h264_2.yuv'},
              25: {
               'content_id': 2,
               'score': 1.9166,
               'path': dis_dir + '/overbridge_h264_3.yuv'},
              26: {
               'content_id': 2,
               'score': 2.7234,
               'path': dis_dir + '/overbridge_h264_4.yuv'},
              27: {
               'content_id': 2,
               'score': 0.11996,
               'path': dis_dir + '/overbridge_mpeg2_1.yuv'},
              28: {
               'content_id': 2,
               'score': 0.51262,
               'path': dis_dir + '/overbridge_mpeg2_2.yuv'},
              29: {
               'content_id': 2,
               'score': 1.9645,
               'path': dis_dir + '/overbridge_mpeg2_3.yuv'},
              30: {
               'content_id': 3,
               'score': 1.1488,
               'path': dis_dir + '/robot_dirac_1.yuv'},
              31: {
               'content_id': 3,
               'score': 2.2292,
               'path': dis_dir + '/robot_dirac_2.yuv'},
              32: {
               'content_id': 3,
               'score': 3.0489,
               'path': dis_dir + '/robot_dirac_3.yuv'},
              33: {
               'content_id': 3,
               'score': 0.11800000000000001,
               'path': dis_dir + '/robot_h264_1.yuv'},
              34: {
               'content_id': 3,
               'score': 0.080388,
               'path': dis_dir + '/robot_h264_2.yuv'},
              35: {
               'content_id': 3,
               'score': 0.6570199999999999,
               'path': dis_dir + '/robot_h264_3.yuv'},
              36: {
               'content_id': 3,
               'score': 1.0689,
               'path': dis_dir + '/robot_h264_4.yuv'},
              37: {
               'content_id': 3,
               'score': 0.68617,
               'path': dis_dir + '/robot_mpeg2_1.yuv'},
              38: {
               'content_id': 3,
               'score': 0.9264700000000001,
               'path': dis_dir + '/robot_mpeg2_2.yuv'},
              39: {
               'content_id': 3,
               'score': 1.526,
               'path': dis_dir + '/robot_mpeg2_3.yuv'},
              40: {
               'content_id': 4,
               'score': 1.2166,
               'path': dis_dir + '/shelf_dirac_1.yuv'},
              41: {
               'content_id': 4,
               'score': 2.4006,
               'path': dis_dir + '/shelf_dirac_2.yuv'},
              42: {
               'content_id': 4,
               'score': 3.0689,
               'path': dis_dir + '/shelf_dirac_3.yuv'},
              43: {
               'content_id': 4,
               'score': 0.052316999999999995,
               'path': dis_dir + '/shelf_h264_1.yuv'},
              44: {
               'content_id': 4,
               'score': 0.49,
               'path': dis_dir + '/shelf_h264_2.yuv'},
              45: {
               'content_id': 4,
               'score': 1.0759,
               'path': dis_dir + '/shelf_h264_3.yuv'},
              46: {
               'content_id': 4,
               'score': 1.4769999999999999,
               'path': dis_dir + '/shelf_h264_4.yuv'},
              47: {
               'content_id': 4,
               'score': 0.41581999999999997,
               'path': dis_dir + '/shelf_mpeg2_1.yuv'},
              48: {
               'content_id': 4,
               'score': 0.75784,
               'path': dis_dir + '/shelf_mpeg2_2.yuv'},
              49: {
               'content_id': 4,
               'score': 2.0495,
               'path': dis_dir + '/shelf_mpeg2_3.yuv'},
              50: {
               'content_id': 5,
               'score': 1.4949,
               'path': dis_dir + '/square_dirac_1.yuv'},
              51: {
               'content_id': 5,
               'score': 2.2675,
               'path': dis_dir + '/square_dirac_2.yuv'},
              52: {
               'content_id': 5,
               'score': 3.0699,
               'path': dis_dir + '/square_dirac_3.yuv'},
              53: {
               'content_id': 5,
               'score': 0.019668,
               'path': dis_dir + '/square_h264_1.yuv'},
              54: {
               'content_id': 5,
               'score': 0.1772,
               'path': dis_dir + '/square_h264_2.yuv'},
              55: {
               'content_id': 5,
               'score': 1.3519,
               'path': dis_dir + '/square_h264_3.yuv'},
              56: {
               'content_id': 5,
               'score': 2.6943,
               'path': dis_dir + '/square_h264_4.yuv'},
              57: {
               'content_id': 5,
               'score': 0.39878,
               'path': dis_dir + '/square_mpeg2_1.yuv'},
              58: {
               'content_id': 5,
               'score': 0.68497,
               'path': dis_dir + '/square_mpeg2_2.yuv'},
              59: {
               'content_id': 5,
               'score': 1.9805,
               'path': dis_dir + '/square_mpeg2_3.yuv'},
              60: {
               'content_id': 6,
               'score': 1.3051,
               'path': dis_dir + '/toys_calendar_dirac_1.yuv'},
              61: {
               'content_id': 6,
               'score': 2.1949,
               'path': dis_dir + '/toys_calendar_dirac_2.yuv'},
              62: {
               'content_id': 6,
               'score': 2.8141,
               'path': dis_dir + '/toys_calendar_dirac_3.yuv'},
              63: {
               'content_id': 6,
               'score': 0.35134,
               'path': dis_dir + '/toys_calendar_h264_1.yuv'},
              64: {
               'content_id': 6,
               'score': 0.80917,
               'path': dis_dir + '/toys_calendar_h264_2.yuv'},
              65: {
               'content_id': 6,
               'score': 2.3485,
               'path': dis_dir + '/toys_calendar_h264_3.yuv'},
              66: {
               'content_id': 6,
               'score': 2.7071,
               'path': dis_dir + '/toys_calendar_h264_4.yuv'},
              67: {
               'content_id': 6,
               'score': 0.27243,
               'path': dis_dir + '/toys_calendar_mpeg2_1.yuv'},
              68: {
               'content_id': 6,
               'score': 0.98525,
               'path': dis_dir + '/toys_calendar_mpeg2_2.yuv'},
              69: {
               'content_id': 6,
               'score': 2.4642,
               'path': dis_dir + '/toys_calendar_mpeg2_3.yuv'},
              70: {
               'content_id': 7,
               'score': 0.46593999999999997,
               'path': dis_dir + '/tractor_dirac_1.yuv'},
              71: {
               'content_id': 7,
               'score': 0.98649,
               'path': dis_dir + '/tractor_dirac_2.yuv'},
              72: {
               'content_id': 7,
               'score': 2.1238,
               'path': dis_dir + '/tractor_dirac_3.yuv'},
              73: {
               'content_id': 7,
               'score': 0.62056,
               'path': dis_dir + '/tractor_h264_1.yuv'},
              74: {
               'content_id': 7,
               'score': 0.97067,
               'path': dis_dir + '/tractor_h264_2.yuv'},
              75: {
               'content_id': 7,
               'score': 1.8136,
               'path': dis_dir + '/tractor_h264_3.yuv'},
              76: {
               'content_id': 7,
               'score': 2.1212,
               'path': dis_dir + '/tractor_h264_4.yuv'},
              77: {
               'content_id': 7,
               'score': -0.263,
               'path': dis_dir + '/tractor_mpeg2_1.yuv'},
              78: {
               'content_id': 7,
               'score': 0.30158,
               'path': dis_dir + '/tractor_mpeg2_2.yuv'},
              79: {
               'content_id': 7,
               'score': 1.4346,
               'path': dis_dir + '/tractor_mpeg2_3.yuv'},
              80: {
               'content_id': 8,
               'score': 2.4218,
               'path': dis_dir + '/train_dirac_1.yuv'},
              81: {
               'content_id': 8,
               'score': 2.8696,
               'path': dis_dir + '/train_dirac_2.yuv'},
              82: {
               'content_id': 8,
               'score': 3.2625,
               'path': dis_dir + '/train_dirac_3.yuv'},
              83: {
               'content_id': 8,
               'score': 1.4794,
               'path': dis_dir + '/train_h264_1.yuv'},
              84: {
               'content_id': 8,
               'score': 1.4380000000000002,
               'path': dis_dir + '/train_h264_2.yuv'},
              85: {
               'content_id': 8,
               'score': 1.6346,
               'path': dis_dir + '/train_h264_3.yuv'},
              86: {
               'content_id': 8,
               'score': 1.7017,
               'path': dis_dir + '/train_h264_4.yuv'},
              87: {
               'content_id': 8,
               'score': 0.2853,
               'path': dis_dir + '/train_mpeg2_1.yuv'},
              88: {
               'content_id': 8,
               'score': 0.6099100000000001,
               'path': dis_dir + '/train_mpeg2_2.yuv'},
              89: {
               'content_id': 8,
               'score': 1.3507,
               'path': dis_dir + '/train_mpeg2_3.yuv'},
              90: {
               'content_id': 9,
               'score': 1.3674,
               'path': dis_dir + '/tube_dirac_1.yuv'},
              91: {
               'content_id': 9,
               'score': 2.331,
               'path': dis_dir + '/tube_dirac_2.yuv'},
              92: {
               'content_id': 9,
               'score': 3.1556,
               'path': dis_dir + '/tube_dirac_3.yuv'},
              93: {
               'content_id': 9,
               'score': -0.093407,
               'path': dis_dir + '/tube_h264_1.yuv'},
              94: {
               'content_id': 9,
               'score': 0.43438999999999994,
               'path': dis_dir + '/tube_h264_2.yuv'},
              95: {
              'content_id': 9,
              'score': 2.305,
              'path': dis_dir + '/tube_h264_3.yuv'},
              96: { 
               'content_id': 9,
               'score': 2.4844,
               'path': dis_dir + '/tube_h264_4.yuv'},
              97: {
               'content_id': 9,
               'score': 0.17627,
               'path': dis_dir + '/tube_mpeg2_1.yuv'},
              98: {
               'content_id': 9,
               'score': 0.66698,
               'path': dis_dir + '/tube_mpeg2_2.yuv'},
              99: {
               'content_id': 9,
               'score': 1.9667,
               'path': dis_dir + '/tube_mpeg2_3.yuv'}}
