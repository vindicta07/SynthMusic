import cv2
import time
import mediapipe as mp
from pythonosc import udp_client
from pythonosc import osc_message_builder

# OSC Setup
ip = "127.0.0.1"
port = 3333
client = udp_client.SimpleUDPClient(ip, port)

# Video Capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)  # Targeting a high frame rate
cv2.setUseOptimized(True)

# MediaPipe Hands Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Exponential moving average for smoothing
def smooth_value(new_val, prev_val, alpha=0.5):
    return alpha * new_val + (1 - alpha) * prev_val

prev_values = []
prev_time = 0

while True:
    success, img = cap.read()
    if not success:
        continue
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    hand_landmarks = []
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                hand_landmarks.append((id, cx, cy))
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
    
    if hand_landmarks:
        useful_values = [p[1] for p in hand_landmarks]  # Extracting X-coordinates for control
        
        # Ensure prev_values has the same length as useful_values
        if len(prev_values) != len(useful_values):
            prev_values = useful_values[:]
        
        # Apply smoothing
        useful_values = [smooth_value(useful_values[i], prev_values[i]) for i in range(len(useful_values))]
        prev_values = useful_values[:]
    else:
        useful_values = [0] * len(prev_values)
    
    for i, value in enumerate(useful_values):
        client.send_message(f"/{i}", value)
    
    # FPS Calculation
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Hand Gesture Music Control', cv2.flip(img, 1))
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
