import cv2
import time
import poseModule as pm
from pythonosc import udp_client
from calc_values import calc_useful_pose_values

# OSC Setup
ip = "127.0.0.1"
port = 3333
client = udp_client.SimpleUDPClient(ip, port)

# Initialize Pose Detector
cap = cv2.VideoCapture(1)
detector = pm.poseDetector(model_complexity=0)
frame_shape = (int(cap.get(3)), int(cap.get(4)))

frame_count = 0
pTime = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (480, 360))  # Downscale to reduce processing load
    img = detector.findPose(img, draw=False)
    lmList = detector.findPosition(img, draw=False)

    detected_parts = []  # Reset detected parts per frame
    osc_data = {}  # Store detected parts for OSC messaging

    if len(lmList) != 0:
        useful_values = calc_useful_pose_values(detector, img, lmList, frame_shape)

        # Check if each part is detected before adding to OSC
        if len(lmList) > 0 and lmList[0][1] > 0 and lmList[0][2] > 0:
            detected_parts.append("Nose")
            osc_data["/nose"] = [useful_values[0], useful_values[1]]

        if len(lmList) > 15 and all(lmList[i][1] > 0 for i in [11, 13, 15]):
            detected_parts.append("Left Arm")
            osc_data["/left_arm"] = [useful_values[3], useful_values[4]]

        if len(lmList) > 16 and all(lmList[i][1] > 0 for i in [12, 14, 16]):
            detected_parts.append("Right Arm")
            osc_data["/right_arm"] = [useful_values[5], useful_values[6]]

        if len(lmList) > 27 and all(lmList[i][1] > 0 for i in [23, 25, 27]):
            detected_parts.append("Left Leg")
            osc_data["/left_leg"] = [useful_values[7], useful_values[8]]

        if len(lmList) > 28 and all(lmList[i][1] > 0 for i in [24, 26, 28]):
            detected_parts.append("Right Leg")
            osc_data["/right_leg"] = [useful_values[9], useful_values[10]]

        if detected_parts:
            print("Detected Body Parts:", ", ".join(detected_parts))

    # Send OSC messages only for detected parts
    if frame_count % 2 == 0:
        for key, value in osc_data.items():
            client.send_message(key, value)

    frame_count += 1

    # Display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    print(f"FPS: {int(fps)}")

    cv2.imshow("MediaPipe Pose", img)
    if cv2.waitKey(5) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
