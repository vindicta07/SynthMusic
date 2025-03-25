import math

def calc_body_area(x11, x12, x23, x24, y12, y24, frame_shape):
    # Calculate using frame dimensions directly
    length_shoulders = abs(x11 - x12) / (0.1 * frame_shape[0])
    length_hips = abs(x23 - x24) / (0.1 * frame_shape[0])
    height_body = abs(y12 - y24) / (0.1 * frame_shape[1])
    return int(0.5 * (length_shoulders + length_hips) * height_body)

def calc_useful_pose_values(detector, img, lmlst, frame_shape):
    # If detector is None, skip angle calculation
    get_angle = lambda p1, p2, p3: int(detector.findAngle(img, p1, p2, p3, draw=False)) if detector is not None else 0

    angle_arm_UL = get_angle(11, 12, 14)
    angle_arm_LL = get_angle(12, 14, 16)
    angle_arm_UR = get_angle(12, 11, 13)
    angle_arm_LR = get_angle(11, 13, 15)

    angle_leg_UL = get_angle(23, 24, 26)
    angle_leg_LL = get_angle(24, 26, 28)
    angle_leg_UR = get_angle(24, 23, 25)
    angle_leg_LR = get_angle(23, 25, 27)

    # Compute body area using specified landmark indices
    body_area = calc_body_area(lmlst[11][1], lmlst[12][1], lmlst[23][1],
                               lmlst[24][1], lmlst[12][2], lmlst[24][2], frame_shape)

    noseX, noseY = int(lmlst[0][1]), int(lmlst[0][2])

    return [noseX, noseY, body_area,
            angle_arm_UL, angle_arm_LL, angle_arm_UR, angle_arm_LR,
            angle_leg_UL, angle_leg_LL, angle_leg_UR, angle_leg_LR]

def empty_values():
    return [0] * 11
