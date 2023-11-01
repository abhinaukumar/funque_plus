from videolib import standards

dataset_name = 'CC_HDDO'

path_to_dataset = '[path to dataset]'
ref_dir = path_to_dataset + '/ORIG_MP4'
dis_dir = path_to_dataset + '/TEST_MP4/CC-HDDO'

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
               'dmos': 39.65,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_Codec1_HM_R1_1280x720_qp10.yuv'},
              1: {
               'content_id': 9,
               'dmos': 27.700000000000003,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_Codec1_HM_R2_1920x1080_qp12.yuv'},
              2: {
               'content_id': 9,
               'dmos': 20.099999999999994,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_Codec1_HM_R3_1920x1080_qp11.yuv'},
              3: {
               'content_id': 9,
               'dmos': 14.25,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_Codec1_HM_R4_1920x1080_qp11.yuv'},
              4: {
               'content_id': 9,
               'dmos': 11.0,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_Codec1_HM_R5_1920x1080_qp11.yuv'},
              5: {
               'content_id': 9,
               'dmos': 45.45,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_Codec2_AV1_R1_ratio1.5_QP63.yuv'},
              6: {
               'content_id': 9,
               'dmos': 29.950000000000003,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_Codec2_AV1_R2_ratio1.5_QP59.yuv'},
              7: {
               'content_id': 9,
               'dmos': 24.450000000000003,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_Codec2_AV1_R3_ratio1.5_QP53.yuv'},
              8: {
               'content_id': 9,
               'dmos': 26.900000000000006,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_Codec2_AV1_R4_ratio1.5_QP44.yuv'},
              9: {
               'content_id': 9,
               'dmos': 18.349999999999994,
               'path': dis_dir + '/S11AirAcrobatic_1920x1080_60fps_10bit_420_Codec2_AV1_R5_ratio1.5_QP36.yuv'},
              10: {
               'content_id': 10,
               'dmos': 55.1,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_Codec1_HM_R1_1280x720_qp11.yuv'},
              11: {
               'content_id': 10,
               'dmos': 46.45,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_Codec1_HM_R2_1920x1080_qp11.yuv'},
              12: {
               'content_id': 10,
               'dmos': 31.349999999999994,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_Codec1_HM_R3_1920x1080_qp11.yuv'},
              13: {
               'content_id': 10,
               'dmos': 19.549999999999997,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_Codec1_HM_R4_1920x1080_qp12.yuv'},
              14: {
               'content_id': 10,
               'dmos': 8.349999999999994,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_Codec1_HM_R5_1920x1080_qp11.yuv'},
              15: {
               'content_id': 10,
               'dmos': 62.05,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_Codec2_AV1_R1_ratio1.5_QP63.yuv'},
              16: {
               'content_id': 10,
               'dmos': 49.25,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_Codec2_AV1_R2_ratio1.5_QP59.yuv'},
              17: {
               'content_id': 10,
               'dmos': 28.299999999999997,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_Codec2_AV1_R2_ratio1_QP60.yuv'},
              18: {
               'content_id': 10,
               'dmos': 18.700000000000003,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_Codec2_AV1_R3_ratio1_QP54.yuv'},
              19: {
               'content_id': 10,
               'dmos': 11.75,
               'path': dis_dir + '/S12CatRobot1_1920x1080_60fps_10bit_420_Codec2_AV1_R4_ratio1_QP44.yuv'},
              20: {
               'content_id': 11,
               'dmos': 48.55,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_Codec1_HM_R1_1920x1080_qp11.yuv'},
              21: {
               'content_id': 11,
               'dmos': 34.650000000000006,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_Codec1_HM_R2_1920x1080_qp12.yuv'},
              22: {
               'content_id': 11,
               'dmos': 21.299999999999997,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_Codec1_HM_R3_1920x1080_qp11.yuv'},
              23: {
               'content_id': 11,
               'dmos': 5.0,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_Codec1_HM_R4_1920x1080_qp11.yuv'},
              24: {
               'content_id': 11,
               'dmos': 9.5,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_Codec1_HM_R5_1920x1080_qp11.yuv'},
              25: {
               'content_id': 11,
               'dmos': 66.7,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_Codec2_AV1_R1_ratio1.5_QP62.yuv'},
              26: {
               'content_id': 11,
               'dmos': 53.75,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_Codec2_AV1_R1_ratio1_QP63.yuv'},
              27: {
               'content_id': 11,
               'dmos': 40.2,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_Codec2_AV1_R2_ratio1_QP60.yuv'},
              28: {
               'content_id': 11,
               'dmos': 19.150000000000006,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_Codec2_AV1_R3_ratio1_QP54.yuv'},
              29: {
               'content_id': 11,
               'dmos': 14.700000000000003,
               'path': dis_dir + '/S13Myanmar4_1920x1080_60fps_10bit_420_Codec2_AV1_R4_ratio1_QP48.yuv'},
              30: {
               'content_id': 12,
               'dmos': 79.75,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_Codec1_HM_R1_960x544_qp11.yuv'},
              31: {
               'content_id': 12,
               'dmos': 64.05,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_Codec1_HM_R2_960x544_qp11.yuv'},
              32: {
               'content_id': 12,
               'dmos': 45.1,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_Codec1_HM_R3_960x544_qp10.yuv'},
              33: {
               'content_id': 12,
               'dmos': 26.200000000000003,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_Codec1_HM_R4_960x544_qp12.yuv'},
              34: {
               'content_id': 12,
               'dmos': 18.0,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_Codec1_HM_R5_1280x720_qp11.yuv'},
              35: {
               'content_id': 12,
               'dmos': 79.15,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_Codec2_AV1_R1_ratio2_QP63.yuv'},
              36: {
               'content_id': 12,
               'dmos': 61.6,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_Codec2_AV1_R2_ratio2_QP56.yuv'},
              37: {
               'content_id': 12,
               'dmos': 38.8,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_Codec2_AV1_R3_ratio2_QP46.yuv'},
              38: {
               'content_id': 12,
               'dmos': 31.700000000000003,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_Codec2_AV1_R4_ratio2_QP38.yuv'},
              39: {
               'content_id': 12,
               'dmos': 18.299999999999997,
               'path': dis_dir + '/S14CalmingWater_1920x1080_60fps_10bit_420_Codec2_AV1_R5_ratio1.5_QP36.yuv'},
              40: {
               'content_id': 13,
               'dmos': 75.3,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_Codec1_HM_R1_960x544_qp11.yuv'},
              41: {
               'content_id': 13,
               'dmos': 68.45,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_Codec1_HM_R2_960x544_qp11.yuv'},
              42: {
               'content_id': 13,
               'dmos': 46.5,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_Codec1_HM_R3_960x544_qp11.yuv'},
              43: {
               'content_id': 13,
               'dmos': 31.950000000000003,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_Codec1_HM_R4_960x544_qp10.yuv'},
              44: {
               'content_id': 13,
               'dmos': 20.700000000000003,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_Codec1_HM_R5_1280x720_qp11.yuv'},
              45: {
               'content_id': 13,
               'dmos': 75.9,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_Codec2_AV1_R1_ratio2_QP57.yuv'},
              46: {
               'content_id': 13,
               'dmos': 63.15,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_Codec2_AV1_R2_ratio2_QP49.yuv'},
              47: {
               'content_id': 13,
               'dmos': 45.65,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_Codec2_AV1_R3_ratio2_QP39.yuv'},
              48: {
               'content_id': 13,
               'dmos': 38.7,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_Codec2_AV1_R4_ratio2_QP33.yuv'},
              49: {
               'content_id': 13,
               'dmos': 22.099999999999994,
               'path': dis_dir + '/S15ToddlerFountain2_1920x1080_60fps_10bit_420_Codec2_AV1_R5_ratio1.5_QP32.yuv'},
              50: {
               'content_id': 14,
               'dmos': 51.5,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_Codec1_HM_R1_1280x720_qp11.yuv'},
              51: {
               'content_id': 14,
               'dmos': 27.700000000000003,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_Codec1_HM_R2_1280x720_qp11.yuv'},
              52: {
               'content_id': 14,
               'dmos': 20.549999999999997,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_Codec1_HM_R3_1920x1080_qp11.yuv'},
              53: {
               'content_id': 14,
               'dmos': 12.450000000000003,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_Codec1_HM_R4_1920x1080_qp12.yuv'},
              54: {
               'content_id': 14,
               'dmos': 9.450000000000003,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_Codec1_HM_R5_1920x1080_qp11.yuv'},
              55: {
               'content_id': 14,
               'dmos': 52.7,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_Codec2_AV1_R1_ratio2_QP58.yuv'},
              56: {
               'content_id': 14,
               'dmos': 44.8,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_Codec2_AV1_R2_ratio2_QP51.yuv'},
              57: {
               'content_id': 14,
               'dmos': 27.150000000000006,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_Codec2_AV1_R3_ratio1.5_QP48.yuv'},
              58: {
               'content_id': 14,
               'dmos': 20.650000000000006,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_Codec2_AV1_R4_ratio1.5_QP42.yuv'},
              59: {
               'content_id': 14,
               'dmos': 19.650000000000006,
               'path': dis_dir + '/S16LampLeaves_1920x1080_60fps_10bit_420_Codec2_AV1_R5_ratio1.5_QP33.yuv'},
              60: {
               'content_id': 15,
               'dmos': 53.65,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_Codec1_HM_R1_1280x720_qp11.yuv'},
              61: {
               'content_id': 15,
               'dmos': 44.75,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_Codec1_HM_R2_1920x1080_qp11.yuv'},
              62: {
               'content_id': 15,
               'dmos': 29.299999999999997,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_Codec1_HM_R3_1920x1080_qp11.yuv'},
              63: {
               'content_id': 15,
               'dmos': 16.950000000000003,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_Codec1_HM_R4_1920x1080_qp12.yuv'},
              64: {
               'content_id': 15,
               'dmos': 17.650000000000006,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_Codec1_HM_R5_1920x1080_qp10.yuv'},
              65: {
               'content_id': 15,
               'dmos': 60.85,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_Codec2_AV1_R1_ratio1.5_QP63.yuv'},
              66: {
               'content_id': 15,
               'dmos': 42.4,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_Codec2_AV1_R2_ratio1.5_QP60.yuv'},
              67: {
               'content_id': 15,
               'dmos': 32.55,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_Codec2_AV1_R2_ratio1_QP60.yuv'},
              68: {
               'content_id': 15,
               'dmos': 22.200000000000003,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_Codec2_AV1_R3_ratio1_QP52.yuv'},
              69: {
               'content_id': 15,
               'dmos': 13.299999999999997,
               'path': dis_dir + '/S17DaylightRoad2_1920x1080_60fps_10bit_420_Codec2_AV1_R4_ratio1_QP42.yuv'},
              70: {
               'content_id': 16,
               'dmos': 60.35,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_Codec1_HM_R1_1280x720_qp11.yuv'},
              71: {
               'content_id': 16,
               'dmos': 52.45,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_Codec1_HM_R2_1280x720_qp10.yuv'},
              72: {
               'content_id': 16,
               'dmos': 32.95,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_Codec1_HM_R3_1920x1080_qp11.yuv'},
              73: {
               'content_id': 16,
               'dmos': 19.400000000000006,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_Codec1_HM_R4_1920x1080_qp11.yuv'},
              74: {
               'content_id': 16,
               'dmos': 14.349999999999994,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_Codec1_HM_R5_1920x1080_qp11.yuv'},
              75: {
               'content_id': 16,
               'dmos': 69.3,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_Codec2_AV1_R1_ratio2_QP60.yuv'},
              76: {
               'content_id': 16,
               'dmos': 52.0,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_Codec2_AV1_R2_ratio1.5_QP60.yuv'},
              77: {
               'content_id': 16,
               'dmos': 32.25,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_Codec2_AV1_R3_ratio1.5_QP53.yuv'},
              78: {
               'content_id': 16,
               'dmos': 15.950000000000003,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_Codec2_AV1_R4_ratio1.5_QP44.yuv'},
              79: {
               'content_id': 16,
               'dmos': 17.349999999999994,
               'path': dis_dir + '/S18RedRock3_1920x1080_60fps_10bit_420_Codec2_AV1_R5_ratio1.5_QP36.yuv'},
              80: {
               'content_id': 17,
               'dmos': 62.15,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_Codec1_HM_R1_960x544_qp11.yuv'},
              81: {
               'content_id': 17,
               'dmos': 35.349999999999994,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_Codec1_HM_R2_960x544_qp11.yuv'},
              82: {
               'content_id': 17,
               'dmos': 18.299999999999997,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_Codec1_HM_R3_1280x720_qp11.yuv'},
              83: {
               'content_id': 17,
               'dmos': 15.650000000000006,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_Codec1_HM_R4_1280x720_qp09.yuv'},
              84: {
               'content_id': 17,
               'dmos': 10.349999999999994,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_Codec1_HM_R5_1920x1080_qp11.yuv'},
              85: {
               'content_id': 17,
               'dmos': 61.8,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_Codec2_AV1_R1_ratio2_QP62.yuv'},
              86: {
               'content_id': 17,
               'dmos': 34.599999999999994,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_Codec2_AV1_R2_ratio2_QP57.yuv'},
              87: {
               'content_id': 17,
               'dmos': 16.049999999999997,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_Codec2_AV1_R3_ratio1.5_QP52.yuv'},
              88: {
               'content_id': 17,
               'dmos': 19.0,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_Codec2_AV1_R4_ratio1.5_QP44.yuv'},
              89: {
               'content_id': 17,
               'dmos': 12.700000000000003,
               'path': dis_dir + '/S19RollerCoaster2_1920x1080_60fps_10bit_420_Codec2_AV1_R5_ratio1.5_QP35.yuv'}}
