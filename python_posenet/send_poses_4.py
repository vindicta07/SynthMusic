#!/usr/bin/env python3
import cv2
import time
import numpy as np
import pyliblo3 as liblo
import mediapipe as mp
from poseModule import poseDetector

# OSC Setup with pyliblo
target = liblo.Address("127.0.0.1", 3333)  # PureData listening port

# GPU-accelerated MediaPipe config
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose

# Video Capture Optimizations
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)

def calc_arm_angle(shoulder, elbow, wrist):
    # Vectorized angle calculation
    a = np.array([shoulder.x, shoulder.y])
    b = np.array([elbow.x, elbow.y])
    c = np.array([wrist.x, wrist.y])
    
    ba = a - b
    bc = c - b
    
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.degrees(np.arccos(cosine_angle))

# MediaPipe GPU Context Managers
with mp_pose.Pose(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    model_complexity=1
) as pose, mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    # Performance tracking
    latency_history = []
    frame_count = 0
    start_time = time.perf_counter()

    while cap.isOpened():
        frame_start = time.perf_counter()
        success, frame = cap.read()
        if not success:
            continue

        # GPU-accelerated processing
        frame.flags.writeable = False
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Parallel processing
        pose_results = pose.process(frame_rgb)
        hand_results = hands.process(frame_rgb)
        processing_done = time.perf_counter()

        # Create OSC Bundle
        bundle = liblo.Bundle()
        bundle.add(liblo.Message('/timestamp', liblo.time()))

        # Process hands (maintain PureData compatibility)
        if hand_results.multi_hand_landmarks:
            for hand_id, hand in enumerate(hand_results.multi_hand_landmarks):
                for id, lm in enumerate(hand.landmark):
                    # Maintain original integer coordinates for PureData
                    h, w = frame.shape[:2]
                    cx = int(lm.x * w)
                    cy = int(lm.y * h)
                    # Original message format: /landmark_index value
                    bundle.add(liblo.Message(f"/{id + hand_id*21}", cx))

        # Process pose (new parameters)
        if pose_results.pose_landmarks:
            h, w = frame.shape[:2]
            landmarks = pose_results.pose_landmarks.landmark
            
            # Normalized parameters (0-1)
            bundle.add(liblo.Message('/pose/nose_x', landmarks[0].x))
            bundle.add(liblo.Message('/pose/nose_y', landmarks[0].y))
            
            # Arm angles (using your existing calculation)
            left_arm_angle = calc_arm_angle(
                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW],
                landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
            )
            bundle.add(liblo.Message('/pose/left_arm', left_arm_angle))

        # Send atomic bundle
        liblo.send(target, bundle)
        
        # Latency measurement
        send_done = time.perf_counter()
        latency = (send_done - frame_start) * 1000  # ms
        latency_history.append(latency)
        frame_count += 1

        # Performance monitoring
        if frame_count % 60 == 0:
            avg_latency = np.mean(latency_history[-60:])
            print(f"Latency: {avg_latency:.2f}ms | FPS: {1/(time.perf_counter()-start_time):.1f}")
            start_time = time.perf_counter()

# def calc_arm_angle(shoulder, elbow, wrist):
#     # Vectorized angle calculation
#     a = np.array([shoulder.x, shoulder.y])
#     b = np.array([elbow.x, elbow.y])
#     c = np.array([wrist.x, wrist.y])
    
#     ba = a - b
#     bc = c - b
    
#     cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
#     return np.degrees(np.arccos(cosine_angle))

# Cleanup
cap.release()