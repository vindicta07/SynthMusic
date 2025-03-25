import cv2
import time
import poseModule as pm
from pythonosc import udp_client
from calc_values import calc_useful_pose_values

ip = "127.0.0.1"
port = 3333
client = udp_client.SimpleUDPClient(ip, port)

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

    if len(lmList) != 0:
        useful_values = calc_useful_pose_values(detector, img, lmList, frame_shape)
    else:
        useful_values = 11 * [0]

    if frame_count % 2 == 0:
        for i, value in enumerate(useful_values):
            client.send_message(f"/{i}", value)

    frame_count += 1

    # Optional: Display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    print(f"FPS: {int(fps)}")

    cv2.imshow('MediaPipe Pose', img)
    if cv2.waitKey(5) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
