# Smart Motion Capture System

This project presents a stereo vision–based Smart Motion Capture system designed to predict a dart’s three-dimensional trajectory and its point of impact on a dartboard. Developed as part of an intra-school Science Journal program in a two-member team, the objective was to build a precise and scalable motion-tracking framework that could later support automated hardware, such as a dynamically adjustable dartboard for consistent bullseyes.

Two RGB webcams were rigidly mounted on a one-meter rod using custom 3D-printed fixtures to eliminate degrees of freedom and ensure stable calibration. To establish an accurate pixel-to-angle mapping, an A2-sized grid board was fabricated and manually calibrated using a laser level. Multiple captures were taken to obtain a reliable reference image, after which Cartesian coordinates were manually annotated due to the grid’s lack of automatic detectability.

Using this pixel–angle dataset, a quadratic regression model was derived to map image coordinates to angular measurements for each camera. A Python-based pipeline then reconstructs 3D positions through trigonometric triangulation, models the dart’s parabolic trajectory across frames, and computes its intersection with the dartboard plane.

The current implementation achieves an average positional error of approximately 1.24 cm under controlled conditions.

---
## Project Status

This project is currently under active development.

Implemented:
- Stereo triangulation
- Dart tip detection
- 3D reconstruction

In Progress:
- Dartboard plane triangulation
- Real-time optimization
- Automated impact prediction

---

## Technical Overview

### Stereo Camera Configuration

Two synchronized RGB webcams (Logitech C920) are positioned at a fixed baseline distance.

```python
BASELINE = 111.9  # cm
```

Camera feeds are captured using OpenCV:

```python
cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)
```

---

### Dart Tip Detection

The system identifies the dart tip through HSV color thresholding and contour analysis.

```python
mask = cv2.inRange(hsv, (35, 50, 50), (85, 255, 255))
```

Contours are filtered using geometric heuristics such as contour area and aspect ratio.

---

### Pixel-to-Angle Mapping

A quadratic regression model converts image-space coordinates into angular measurements.

```python
Anglex = (
    0.038002 * x
    - 0.001274 * y_inv
    - 0.000001 * x**2
)
```

The regression coefficients were experimentally derived through manual calibration.

---

### 3D Triangulation

Depth estimation is performed using stereo triangulation based on angular disparity between cameras.

```python
Z = (BASELINE * math.cos(ax1) * math.cos(ax2)) / math.sin(delta)
```

The reconstructed spatial coordinates are represented as:

```python
(X, Y, Z)
```

---

### Visualization Pipeline

The reconstructed coordinates are visualized in real time using a live 3D Matplotlib plot alongside OpenCV camera feeds.

---

### CAD Design
![Camera Lock Mount](https://github.com/abisheikashok/-Smart-Motion-Capture-System/blob/752beec581bf4c9687b445ee4616782097070732/CAD%20Design.png)(https://github.com/abisheikashok/-Smart-Motion-Capture-System/blob/b41ed5e3cfe2660e48bb3dea2031848e713ede65/Rod%20attachment%201.stl)


### Triangulation Mathematics
![Diagram and Math](https://github.com/abisheikashok/-Smart-Motion-Capture-System/blob/aa2d4a5c110eca87cadbd1d43dbfea511b78fc9b/Diagram%26Math.png)

### Experimental Setup
![Setup](https://github.com/abisheikashok/-Smart-Motion-Capture-System/blob/aa2d4a5c110eca87cadbd1d43dbfea511b78fc9b/Setup.png)

### Physical Demonstration
![Demonstration](https://github.com/abisheikashok/-Smart-Motion-Capture-System/blob/aa2d4a5c110eca87cadbd1d43dbfea511b78fc9b/Demonstration.jpg)

### Result
![Result](https://github.com/abisheikashok/-Smart-Motion-Capture-System/blob/ebf1b810f0b6fdcf6f48177a9d4155627b631c71/Result_position.jpg)

---

## Current Limitations

- Dartboard plane triangulation is still under development
- Marker correspondence between stereo frames remains computationally unstable
- Real-time performance at 30 FPS is not yet consistently achieved
- Detection robustness is sensitive to lighting variation and motion blur

---

## Ongoing Development

Current development is focused on:

- Reliable dartboard plane reconstruction
- Multi-marker stereo correspondence
- Computational optimization for low-latency processing
- Improved trajectory prediction accuracy
- Hardware scalability for automated dartboard systems

---

## Technologies Used

- Python
- OpenCV
- NumPy
- Matplotlib
- Stereo Vision Geometry
- Regression-Based Camera Calibration

---

## Author

Ashok Abisheik

---

```
