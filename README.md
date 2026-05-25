# Smart Motion Capture System

A stereo vision–based motion capture system for reconstructing a dart’s 3D trajectory and predicting its impact position on a dartboard using dual RGB cameras and real-time triangulation.

The long-term goal of this project is to build the foundation for an automated dartboard system capable of repositioning itself for bullseye alignment. The current implementation focuses on stereo calibration, dart tip detection, 3D reconstruction, and trajectory estimation using computer vision and geometric triangulation.

---

## Features

- Stereo camera–based 3D reconstruction
- Real-time dart tip detection using OpenCV
- Pixel-to-angle regression calibration model
- Stereo triangulation for spatial coordinate estimation
- Live 3D visualization using Matplotlib
- Custom hardware mounting system with fixed stereo geometry

---

## Project Status

### Implemented

- Stereo triangulation
- Dart tip detection
- 3D coordinate reconstruction
- Regression-based camera calibration
- Live coordinate visualization

### In Progress

- Dartboard plane triangulation
- Real-time optimization for stable 30 FPS tracking
- Dart trajectory prediction
- Automated impact point estimation

---

## Hardware Setup

The system uses:

- 2 × Logitech C920 RGB webcams
- Fixed 1 m baseline mounting rod
- Custom 3D-printed camera mounts
- A2 calibration grid for regression mapping

The cameras are rigidly fixed with no degrees of freedom to maintain consistent stereo geometry.

```python
BASELINE = 111.9  # cm
```

Camera capture configuration:

```python
cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
```

---

## System Pipeline

### 1. Dart Tip Detection

The dart tip is detected through HSV thresholding and contour analysis.

```python
mask = cv2.inRange(hsv, (35, 50, 50), (85, 255, 255))
```

Contours are filtered using:

- Contour area
- Aspect ratio
- Geometric heuristics

Example:

```python
for c in contours:
    area = cv2.contourArea(c)

    if area < 200:
        continue

    x, y, w, h = cv2.boundingRect(c)
    aspect_ratio = h / (w + 1e-5)
```

---

### 2. Pixel-to-Angle Calibration

A quadratic regression model converts image-space pixel coordinates into angular measurements.

```python
Anglex = (
    0.038002 * x
    - 0.001274 * y_inv
    - 0.000001 * x**2
    + 0.000001 * x * y_inv
    - 35.921325
)
```

The regression coefficients were experimentally derived through manual calibration using a custom A2 Cartesian reference grid.

---

### 3. Stereo Triangulation

3D position estimation is computed using angular disparity between both cameras.

```python
Z = (BASELINE * math.cos(ax1) * math.cos(ax2)) / math.sin(delta)
```

The reconstructed coordinates are represented as:

```python
(X, Y, Z)
```

Core triangulation implementation:

```python
def calculate_3d_position(ax1, ay1, ax2, ay2):
    delta = ax1 - ax2

    if abs(delta) < 1e-4:
        return None

    Z = (BASELINE * math.cos(ax1) * math.cos(ax2)) / math.sin(delta)
    Z = abs(Z)

    X = Z * math.tan(ax1)
    Y = Z * math.tan(ay1)

    return X, Y, Z
```

---

### 4. Visualization Pipeline

The reconstructed coordinates are visualized in real time using:

- OpenCV camera feeds
- Live 3D Matplotlib plotting
- Coordinate display overlays

```python
ax.scatter(X, Y, Z, s=80)
```

---

## Experimental Results

- Approximate reconstruction error: **1.24 cm**
- Successful stereo tracking of a green dart
- Real-time coordinate visualization

---

## Future Development

Current development focuses on:

- Dartboard plane reconstruction
- Multi-marker stereo correspondence
- Parabolic trajectory modeling
- Dartboard impact prediction
- Real-time computational optimization
- Hardware scalability for automated dartboard systems

The intended future approach triangulates both the dart and dartboard across frames to estimate the dart’s trajectory and determine the intersection point with the dartboard plane equation.

---

## Current Limitations

- Dartboard triangulation is still under development
- Marker correspondence across stereo frames remains unstable
- Real-time 30 FPS tracking is not consistently achieved
- Detection robustness is sensitive to:
  - Lighting variation
  - Motion blur
  - Occlusion

---

## Repository Structure

```text
Smart-Motion-Capture-System/
│
├── main/
│   ├── Dart_coordinate_prediction_only.py
│   ├── regression.py
│   └── README.md
│
├── assets/
│   ├── CAD Design.png
│   ├── Demonstration.jpg
│   ├── Diagram&Math.png
│   ├── Rod attachment 1.stl
│   ├── Rod attachment 2.stl
│   └── Setup.png
│
├── calibration/
│   ├── Grid_image.jpg
│   └── logitechc920.xlsx
│
└── results/
    └── Result_position.jpg
```
---

## Media

### Triangulation Mathematics

![Diagram and Math](https://github.com/abisheikashok/Smart-Motion-Capture-System/blob/main/assets/Diagram%26Math.png)

---

### CAD Design

[![Camera Lock Mount](https://github.com/abisheikashok/Smart-Motion-Capture-System/blob/main/assets/CAD%20Design.png)](https://github.com/abisheikashok/Smart-Motion-Capture-System/blob/main/assets/Rod%20attachment%201.stl)

---

### Experimental Setup

![Setup](https://github.com/abisheikashok/Smart-Motion-Capture-System/blob/main/assets/Setup.png)

---

### Physical Demonstration

![Demonstration](https://github.com/abisheikashok/Smart-Motion-Capture-System/blob/main/assets/Demonstration.jpg)

---

### Result

![Result](https://github.com/abisheikashok/Smart-Motion-Capture-System/blob/main/results/Result_position.jpg)

---

## Technologies Used

- Python
- OpenCV
- NumPy
- Matplotlib
- Stereo Vision Geometry
- Regression-Based Camera Calibration

---

## Contributors

| Contributor | Profile | Contributions |
|---|---|---|
| Ashok Abisheik | [GitHub](https://github.com/abisheikashok) | Stereo vision pipeline, triangulation, OpenCV implementation, calibration modeling |
| Shreyas Panda || Hardware setup, CAD mounting system, calibration support |

---

## Repository

GitHub Repository:  
https://github.com/abisheikashok/Smart-Motion-Capture-System
