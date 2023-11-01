from videolib import standards

dataset_name = 'CC_HD'

path_to_dataset = '[path to dataset]'
ref_dir = path_to_dataset + '/ORIG_MP4'
dis_dir = path_to_dataset + '/TEST_MP4/CC-HD'

ref_standard = standards.sRGB_10
dis_standard = standards.sRGB_10

width = 1920
height = 1080

ref_videos = {0: {
               'content_name': 'S01AirAcrobatic',
               'path': ref_dir + '/S01AirAcrobatic_3840x2160_60fps_10bit_420.yuv'},
              1: {
               'content_name': 'S02CatRobot1',
               'path': ref_dir + '/S02CatRobot1_3840x2160_60fps_10bit_420.yuv'},
              2: {
               'content_name': 'S03Myanmar4',
               'path': ref_dir + '/S03Myanmar4_3840x2160_60fps_10bit_420.yuv'},
              3: {
               'content_name': 'S04CalmingWater',
               'path': ref_dir + '/S04CalmingWater_3840x2160_60fps_10bit_420.yuv'},
              4: {
               'content_name': 'S05ToddlerFountain2',
               'path': ref_dir + '/S05ToddlerFountain2_3840x2160_60fps_10bit_420.yuv'},
              5: {
               'content_name': 'S06LampLeaves',
               'path': ref_dir + '/S06LampLeaves_3840x2160_60fps_10bit_420.yuv'},
              6: {
               'content_name': 'S07DaylightRoad2',
               'path': ref_dir + '/S07DaylightRoad2_3840x2160_60fps_10bit_420.yuv'},
              7: {
               'content_name': 'S08RedRock3',
               'path': ref_dir + '/S08RedRock3_3840x2160_60fps_10bit_420.yuv'},
              8: {
               'content_name': 'S09RollerCoaster2',
               'path': ref_dir + '/S09RollerCoaster2_3840x2160_60fps_10bit_420.yuv'},
              9: {
               'content_name': 'S11AirAcrobatic',
               'path': ref_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420.yuv'},
              10: {
               'content_name': 'S12CatRobot1',
               'path': ref_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420.yuv'},
              11: {
               'content_name': 'S13Myanmar4',
               'path': ref_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420.yuv'},
              12: {
               'content_name': 'S14CalmingWater',
               'path': ref_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420.yuv'},
              13: {
               'content_name': 'S15ToddlerFountain2',
               'path': ref_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420.yuv'},
              14: {
               'content_name': 'S16LampLeaves',
               'path': ref_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420.yuv'},
              15: {
               'content_name': 'S17DaylightRoad2',
               'path': ref_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420.yuv'},
              16: {
               'content_name': 'S18RedRock3',
               'path': ref_dir + '/S18RedRock3_1920x1080_60fps_10bit_420.yuv'},
              17: {
               'content_name': 'S19RollerCoaster2',
               'path': ref_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420.yuv'}}

dis_videos = {0: {
               'content_id': 9,
               'score': 30.900000000000006,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_AV1_R1_QP63.yuv'},
              1: {
               'content_id': 9,
               'score': 23.900000000000006,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_AV1_R2_QP60.yuv'},
              2: {
               'content_id': 9,
               'score': 18.480000000000004,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_AV1_R3_QP52.yuv'},
              3: {
               'content_id': 9,
               'score': 12.049999999999997,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_AV1_R4_QP44.yuv'},
              4: {
               'content_id': 9,
               'score': 24.900000000000006,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_HM_R1_qp06.yuv'},
              5: {
               'content_id': 9,
               'score': 20.569999999999993,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_HM_R2_qp07.yuv'},
              6: {
               'content_id': 9,
               'score': 12.810000000000002,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_HM_R3_qp07.yuv'},
              7: {
               'content_id': 9,
               'score': 7.950000000000003,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_HM_R4_qp08.yuv'},
              8: {
               'content_id': 9,
               'score': 19.14,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_VTM401_R1.yuv'},
              9: {
               'content_id': 9,
               'score': 16.950000000000003,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_VTM401_R2.yuv'},
              10: {
               'content_id': 9,
               'score': 15.430000000000007,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_VTM401_R3.yuv'},
              11: {
               'content_id': 9,
               'score': 7.810000000000002,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_VTM401_R4.yuv'},
              12: {
               'content_id': 10,
               'score': 44.57,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_AV1_R1_QP63.yuv'},
              13: {
               'content_id': 10,
               'score': 33.620000000000005,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_AV1_R2_QP60.yuv'},
              14: {
               'content_id': 10,
               'score': 18.67,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_AV1_R3_QP54.yuv'},
              15: {
               'content_id': 10,
               'score': 8.239999999999995,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_AV1_R4_QP44.yuv'},
              16: {
               'content_id': 10,
               'score': 38.48,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_HM_R1_qp02.yuv'},
              17: {
               'content_id': 10,
               'score': 30.569999999999993,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_HM_R2_qp07.yuv'},
              18: {
               'content_id': 10,
               'score': 20.189999999999998,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_HM_R3_qp06.yuv'},
              19: {
               'content_id': 10,
               'score': 10.14,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_HM_R4_qp04.yuv'},
              20: {
               'content_id': 10,
               'score': 19.569999999999993,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_VTM401_R1.yuv'},
              21: {
               'content_id': 10,
               'score': 13.14,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_VTM401_R2.yuv'},
              22: {
               'content_id': 10,
               'score': 8.760000000000005,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_VTM401_R3.yuv'},
              23: {
               'content_id': 10,
               'score': 3.430000000000007,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_VTM401_R4.yuv'},
              24: {
               'content_id': 11,
               'score': 52.71,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_AV1_R1_QP63.yuv'},
              25: {
               'content_id': 11,
               'score': 38.76,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_AV1_R2_QP60.yuv'},
              26: {
               'content_id': 11,
               'score': 15.810000000000002,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_AV1_R3_QP54.yuv'},
              27: {
               'content_id': 11,
               'score': 11.900000000000006,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_AV1_R4_QP48.yuv'},
              28: {
               'content_id': 11,
               'score': 31.189999999999998,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_HM_R1_qp06.yuv'},
              29: {
               'content_id': 11,
               'score': 14.329999999999998,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_HM_R2_qp08.yuv'},
              30: {
               'content_id': 11,
               'score': 13.86,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_HM_R3_qp07.yuv'},
              31: {
               'content_id': 11,
               'score': 6.480000000000004,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_HM_R4_qp07.yuv'},
              32: {
               'content_id': 11,
               'score': 22.430000000000007,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_VTM401_R1.yuv'},
              33: {
               'content_id': 11,
               'score': 2.6700000000000017,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_VTM401_R2.yuv'},
              34: {
               'content_id': 11,
               'score': 5.519999999999996,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_VTM401_R3.yuv'},
              35: {
               'content_id': 11,
               'score': 4.290000000000006,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_VTM401_R4.yuv'},
              36: {
               'content_id': 12,
               'score': 57.67,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_HM_R1_qp06.yuv'},
              37: {
               'content_id': 12,
               'score': 40.14,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_HM_R2_qp02.yuv'},
              38: {
               'content_id': 12,
               'score': 22.67,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_HM_R3_qp03.yuv'},
              39: {
               'content_id': 12,
               'score': 10.430000000000007,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_HM_R4_qp08.yuv'},
              40: {
               'content_id': 12,
               'score': 66.0,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_VTM401_R1.yuv'},
              41: {
               'content_id': 12,
               'score': 46.57,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_VTM401_R2.yuv'},
              42: {
               'content_id': 12,
               'score': 22.519999999999996,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_VTM401_R3.yuv'},
              43: {
               'content_id': 12,
               'score': 15.569999999999993,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_VTM401_R4.yuv'},
              44: {
               'content_id': 12,
               'score': 51.48,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_AV1_R1_QP63.yuv'},
              45: {
               'content_id': 12,
               'score': 37.24,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_AV1_R2_QP58.yuv'},
              46: {
               'content_id': 12,
               'score': 23.0,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_AV1_R3_QP50.yuv'},
              47: {
               'content_id': 12,
               'score': 11.14,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_AV1_R4_QP42.yuv'},
              48: {
               'content_id': 13,
               'score': 50.43,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_AV1_R1_QP60.yuv'},
              49: {
               'content_id': 13,
               'score': 23.569999999999993,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_AV1_R2_QP52.yuv'},
              50: {
               'content_id': 13,
               'score': 18.519999999999996,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_AV1_R3_QP46.yuv'},
              51: {
               'content_id': 13,
               'score': 11.0,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_AV1_R4_QP40.yuv'},
              52: {
               'content_id': 13,
               'score': 49.29,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_HM_R1_qp05.yuv'},
              53: {
               'content_id': 13,
               'score': 25.709999999999994,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_HM_R2_qp05.yuv'},
              54: {
               'content_id': 13,
               'score': 15.620000000000005,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_HM_R3_qp08.yuv'},
              55: {
               'content_id': 13,
               'score': 11.670000000000002,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_HM_R4_qp07.yuv'},
              56: {
               'content_id': 13,
               'score': 45.19,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_VTM401_R1.yuv'},
              57: {
               'content_id': 13,
               'score': 20.379999999999995,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_VTM401_R2.yuv'},
              58: {
               'content_id': 13,
               'score': 15.709999999999994,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_VTM401_R3.yuv'},
              59: {
               'content_id': 13,
               'score': 9.620000000000005,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_VTM401_R4.yuv'},
              60: {
               'content_id': 14,
               'score': 27.0,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_AV1_R1_QP62.yuv'},
              61: {
               'content_id': 14,
               'score': 13.950000000000003,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_AV1_R2_QP56.yuv'},
              62: {
               'content_id': 14,
               'score': 9.14,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_AV1_R3_QP50.yuv'},
              63: {
               'content_id': 14,
               'score': 7.950000000000003,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_AV1_R4_QP42.yuv'},
              64: {
               'content_id': 14,
               'score': 32.19,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_HM_R1_qp03.yuv'},
              65: {
               'content_id': 14,
               'score': 20.099999999999994,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_HM_R2_qp07.yuv'},
              66: {
               'content_id': 14,
               'score': 12.0,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_HM_R3_qp06.yuv'},
              67: {
               'content_id': 14,
               'score': 9.239999999999995,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_HM_R4_qp02.yuv'},
              68: {
               'content_id': 14,
               'score': 17.900000000000006,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_VTM401_R1.yuv'},
              69: {
               'content_id': 14,
               'score': 12.189999999999998,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_VTM401_R2.yuv'},
              70: {
               'content_id': 14,
               'score': 5.810000000000002,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_VTM401_R3.yuv'},
              71: {
               'content_id': 14,
               'score': 6.430000000000007,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_VTM401_R4.yuv'},
              72: {
               'content_id': 15,
               'score': 43.19,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_AV1_R1_QP63.yuv'},
              73: {
               'content_id': 15,
               'score': 32.620000000000005,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_AV1_R2_QP60.yuv'},
              74: {
               'content_id': 15,
               'score': 15.86,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_AV1_R3_QP52.yuv'},
              75: {
               'content_id': 15,
               'score': 5.140000000000001,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_AV1_R4_QP42.yuv'},
              76: {
               'content_id': 15,
               'score': 40.29,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_HM_R1_qp08.yuv'},
              77: {
               'content_id': 15,
               'score': 27.290000000000006,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_HM_R2_qp02.yuv'},
              78: {
               'content_id': 15,
               'score': 12.810000000000002,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_HM_R3_qp07.yuv'},
              79: {
               'content_id': 15,
               'score': 5.140000000000001,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_HM_R4_qp04.yuv'},
              80: {
               'content_id': 15,
               'score': 23.049999999999997,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_VTM401_R1.yuv'},
              81: {
               'content_id': 15,
               'score': 10.810000000000002,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_VTM401_R2.yuv'},
              82: {
               'content_id': 15,
               'score': 6.329999999999998,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_VTM401_R3.yuv'},
              83: {
               'content_id': 15,
               'score': 3.6700000000000017,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_VTM401_R4.yuv'},
              84: {
               'content_id': 16,
               'score': 52.14,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_AV1_R1_QP63.yuv'},
              85: {
               'content_id': 16,
               'score': 37.1,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_AV1_R2_QP60.yuv'},
              86: {
               'content_id': 16,
               'score': 22.189999999999998,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_AV1_R3_QP52.yuv'},
              87: {
               'content_id': 16,
               'score': 10.0,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_AV1_R4_QP44.yuv'},
              88: {
               'content_id': 16,
               'score': 43.19,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_HM_R1_qp06.yuv'},
              89: {
               'content_id': 16,
               'score': 27.049999999999997,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_HM_R2_qp06.yuv'},
              90: {
               'content_id': 16,
               'score': 14.86,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_HM_R3_qp03.yuv'},
              91: {
               'content_id': 16,
               'score': 9.950000000000003,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_HM_R4_qp07.yuv'},
              92: {
               'content_id': 16,
               'score': 25.86,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_VTM401_R1.yuv'},
              93: {
               'content_id': 16,
               'score': 20.049999999999997,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_VTM401_R2.yuv'},
              94: {
               'content_id': 16,
               'score': 9.329999999999998,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_VTM401_R3.yuv'},
              95: {
               'content_id': 16,
               'score': 6.480000000000004,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_VTM401_R4.yuv'},
              96: {
               'content_id': 17,
               'score': 37.1,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_AV1_R1_QP63.yuv'},
              97: {
               'content_id': 17,
               'score': 14.569999999999993,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_AV1_R2_QP58.yuv'},
              98: {
               'content_id': 17,
               'score': 7.0,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_AV1_R3_QP50.yuv'},
              99: {
               'content_id': 17,
               'score': 3.1899999999999977,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_AV1_R4_QP42.yuv'},
              100: {
               'content_id': 17,
               'score': 30.049999999999997,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_HM_R1_qp08.yuv'},
              101: {
               'content_id': 17,
               'score': 16.14,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_HM_R2_qp07.yuv'},
              102: {
               'content_id': 17,
               'score': 8.189999999999998,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_HM_R3_qp08.yuv'},
              103: {
               'content_id': 17,
               'score': 3.519999999999996,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_HM_R4_qp02.yuv'},
              104: {
               'content_id': 17,
               'score': 15.709999999999994,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_VTM401_R1.yuv'},
              105: {
               'content_id': 17,
               'score': 7.140000000000001,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_VTM401_R2.yuv'},
              106: {
               'content_id': 17,
               'score': 2.6700000000000017,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_VTM401_R3.yuv'},
              107: {
               'content_id': 17,
               'score': 0.14000000000000057,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_VTM401_R4.yuv'}}
