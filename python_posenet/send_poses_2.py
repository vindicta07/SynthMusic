import cv2
import time
import poseModule as pm
from pythonosc import udp_client
from pythonosc import osc_message_builder
from calc_values import empty_values

# OSC Setup
ip = "127.0.0.1"
port = 3333
client = udp_client.SimpleUDPClient(ip, port)

# Video Capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)  # Targeting a high frame rate
cv2.setUseOptimized(True)

detector = pm.poseDetector(detectionCon=0.7, trackCon=0.7)

# Exponential moving average for smoothing
def smooth_value(new_val, prev_val, alpha=0.5):
    return alpha * new_val + (1 - alpha) * prev_val

prev_values = empty_values()

while True:
    success, img = cap.read()
    if not success:
        continue
    
    img = detector.findPose(img)
    frame_shape = (cap.get(3), cap.get(4))
    lmList = detector.findPosition(img, draw=False)
    
    if len(lmList) != 0:
        # Only use hand keypoints (wrist, fingers)
        hand_points = [lmList[15], lmList[16], lmList[17], lmList[18], lmList[19], lmList[20],
                       lmList[21], lmList[22], lmList[23], lmList[24]]
        useful_values = [p[1] for p in hand_points]  # Extracting X-coordinates for control
        
        # Apply smoothing
        useful_values = [smooth_value(useful_values[i], prev_values[i]) for i in range(len(useful_values))]
        prev_values = useful_values
    else:
        useful_values = empty_values()
    
    for i, value in enumerate(useful_values):
        client.send_message(f"/{i}", value)
    
    cv2.imshow('Hand Gesture Music Control', cv2.flip(img, 1))
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
