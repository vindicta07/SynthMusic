import math

def calc_body_area(x11, x12, x23, x24, y12, y24, frame_shape):
	'''Calculates the body area of the trapezium from right shoulder, 
	left shoulder, right hip and left hip landmarks'''
	length_shoulders = abs(x11 - x12) / (0.1 * frame_shape[0])
	length_hips = abs(x23 - x24) / (0.1 * frame_shape[0])
	height_body = abs(y12 - y24) / (0.1 * frame_shape[1])

	# area of trapezium, which is the body
	body_area = (0.5 * (length_shoulders + length_hips)) * height_body

	return int(body_area)


def calc_useful_pose_values(detector, img, lmlst, frame_shape):
	''' calculates useful values from the list of landmarks. 
	L = left, R = right, U = upper, L = lower '''

	# angles from arms 
	angle_arm_UL = int(detector.findAngle(img, 11, 12, 14, draw=False))
	angle_arm_LL = int(detector.findAngle(img, 12, 14, 16, draw=False))
	angle_arm_UR = int(detector.findAngle(img, 12, 11, 13, draw=False))
	angle_arm_LR = int(detector.findAngle(img, 11, 13, 15, draw=False))

	# angles from legs 
	angle_leg_UL = int(detector.findAngle(img, 23, 24, 26, draw=False))
	angle_leg_LL = int(detector.findAngle(img, 24, 26, 28, draw=False))
	angle_leg_UR = int(detector.findAngle(img, 24, 23, 25, draw=False))
	angle_leg_LR = int(detector.findAngle(img, 23, 25, 27, draw=False))

	# area of the body trapezium
	body_area = calc_body_area(lmlst[11][1], lmlst[12][1], lmlst[23][1],
							lmlst[24][1], lmlst[12][2], lmlst[24][2], 
							frame_shape)

	noseX = int(lmlst[0][1])
	noseY = int(lmlst[0][2])

	useful_values = [noseX, noseY, body_area, angle_arm_UL, angle_arm_LL, angle_arm_UR, 
						angle_arm_LR, angle_leg_UL, angle_leg_LL, angle_leg_UR, angle_leg_LR]

	return useful_values

def empty_values():
	return 11*[0]
