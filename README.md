# 🎵 SynthMusic - Gesture-Controlled Music Synthesizer

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green.svg)](https://opencv.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose%20Detection-orange.svg)](https://mediapipe.dev)
[![OSC](https://img.shields.io/badge/OSC-Audio%20Protocol-purple.svg)](https://opensoundcontrol.stanford.edu)

An innovative real-time gesture-controlled music synthesizer that transforms body movements into musical expressions using computer vision and pose estimation technology. 

## 🚀 Features

- **Real-time Pose Detection**: Advanced body pose tracking using MediaPipe
- **Gesture-to-Music Mapping**: Convert body movements into musical parameters
- **OSC Integration**: Seamless communication with music production software
- **Multi-body Part Tracking**: Independent control for arms, legs, and torso
- **Optimized Performance**: Efficient processing with configurable frame rates
- **Visual Feedback**: Live pose visualization and detection status

## 🛠️ Technology Stack

- **Computer Vision**: OpenCV, MediaPipe
- **Audio Communication**: python-osc
- **Core Language**: Python 3.7+
- **Pose Estimation**: MediaPipe Pose solution
- **Real-time Processing**: Optimized frame processing pipeline

## 📋 Prerequisites

- Python 3.7 or higher
- Webcam or camera device
- Compatible DAW or music software supporting OSC

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vindicta07/SynthMusic.git
   cd SynthMusic
   ```

2. **Install required dependencies**
   ```bash
   pip install opencv-python mediapipe python-osc
   ```

3. **Verify camera setup**
   ```bash
   python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error')"
   ```

## 🎯 Quick Start

1. **Basic pose detection**
   ```bash
   python changes/send_poses.py
   ```

2. **Advanced detection with body part filtering**
   ```bash
   python changes/send_poses_2.py
   ```

3. **Configure OSC settings** (default: localhost:3333)
   ```python
   ip = "127.0.0.1"
   port = 3333
   ```

## 📊 OSC Message Format

The system sends OSC messages in the following format:

| Body Part | OSC Address | Parameters | Description |
|-----------|-------------|------------|-------------|
| Nose | `/nose` | `[x, y]` | Head position coordinates |
| Left Arm | `/left_arm` | `[upper_angle, lower_angle]` | Arm joint angles |
| Right Arm | `/right_arm` | `[upper_angle, lower_angle]` | Arm joint angles |
| Left Leg | `/left_leg` | `[upper_angle, lower_angle]` | Leg joint angles |
| Right Leg | `/right_leg` | `[upper_angle, lower_angle]` | Leg joint angles |

### Individual Parameter Messages
```
/0 - Nose X coordinate
/1 - Nose Y coordinate  
/2 - Body area
/3 - Left upper arm angle
/4 - Left lower arm angle
/5 - Right upper arm angle
/6 - Right lower arm angle
/7 - Left upper leg angle
/8 - Left lower leg angle
/9 - Right upper leg angle
/10 - Right lower leg angle
```

## 🏗️ Project Structure

```
SynthMusic/
├── changes/
│   ├── poseModule.py          # Core pose detection class
│   ├── calc_values.py         # Pose calculation utilities
│   ├── send_poses.py          # Basic OSC sender
│   └── send_poses_2.py        # Advanced OSC sender with filtering
├── puredata/                  # PureData patches (if applicable)
├── sounds/                    # Audio samples and resources
└── README.md                  # Project documentation
```

## 🎛️ Configuration

### Camera Settings
```python
# Adjust camera index (0 for default, 1 for external)
cap = cv2.VideoCapture(1)

# Modify resolution for performance
img = cv2.resize(img, (480, 360))
```

### Pose Detection Parameters
```python
detector = pm.poseDetector(
    model_complexity=0,        # 0=Light, 1=Full, 2=Heavy
    detectionCon=0.5,         # Detection confidence
    trackCon=0.5              # Tracking confidence
)
```

### OSC Configuration
```python
ip = "127.0.0.1"    # Target IP address
port = 3333         # Target port
```

## 🎵 Music Software Integration

### Recommended DAWs
- **Ableton Live**: Use Max for Live OSC devices
- **Reaper**: OSC_ReaJS plugin
- **Pure Data**: Direct OSC integration
- **Max/MSP**: Native OSC support
- **TouchDesigner**: Built-in OSC operators

### Example Integration (Pure Data)
```
[udpreceive 3333]
|
[oscparse]
|
[route /nose /left_arm /right_arm]
```

## 🔬 Advanced Usage

### Custom Gesture Mapping
```python
# Extend calc_values.py for custom calculations
def custom_gesture_value(lmList):
    # Your custom pose calculation logic
    return calculated_value
```

### Performance Optimization
```python
# Reduce processing frequency
if frame_count % 3 == 0:  # Process every 3rd frame
    # Pose detection logic
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is part of Google Summer of Code 2025. Please refer to the repository for specific licensing terms.

## 🙏 Acknowledgments

- **MediaPipe Team** for the excellent pose estimation solution
- **OpenCV Community** for computer vision tools
- **OSC Community** for the Open Sound Control protocol
- **Google Summer of Code** for supporting this project

## 🐛 Troubleshooting

### Common Issues

**Camera not detected**
```bash
# List available cameras
python -c "import cv2; [print(f'Camera {i}: {cv2.VideoCapture(i).isOpened()}') for i in range(5)]"
```

**OSC messages not received**
- Verify IP address and port configuration
- Check firewall settings
- Ensure receiving application is listening on correct port

**Low performance**
- Reduce camera resolution
- Increase frame skip interval
- Lower MediaPipe model complexity

## 📧 Contact

**Developer**: vindicta07  
**Project Link**: [https://github.com/vindicta07/SynthMusic](https://github.com/vindicta07/SynthMusic)

---

*Transform your movements into music with SynthMusic - Where gesture meets harmony* 🎭🎵
