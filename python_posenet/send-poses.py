import cv2
import time
import poseModule as pm
from pythonosc import udp_client
from pythonosc import osc_message_builder
from calc_values import calc_useful_pose_values, empty_values

ip = "127.0.0.1"
port = 3333
client = udp_client.SimpleUDPClient(ip, port)
 
cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
while True:
    success, img = cap.read()
    img = detector.findPose(img)
    frame_shape = (cap.get(3), cap.get(4))
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) !=0:
        useful_values = calc_useful_pose_values(detector, img, lmList, frame_shape)
    else: 
        useful_values = 11*[0]
    for i, value in enumerate(useful_values):
        client.send_message(f"/{i}", value)
 
    cv2.imshow('MediaPipe Pose', cv2.flip(img, 1))
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
