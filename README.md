# Smart Motion Capture System

This project presents a stereo vision–based motion capture system to predict a dart’s 3D trajectory and impact point on a dartboard. The long-term objective is to establish the foundation for future hardware integration, where a sliding dartboard could automatically reposition itself to score bullseyes every time. The system includes two RGB webcams mounted on a 1 m rod with fixed 3D-printed attachments, so there were no degrees of freedom. A custom A2 calibration grid was printed, captured by the camera, and manually annotated Cartesian reference points to establish an accurate pixel-to-angle regression model.

A Python program then processed the pixel positions from the camera feeds to calculate the corresponding angles using the derived equation and computed the 3D coordinates using a trigonometric formula, achieving an error of 1.24 cm when tested with a green ball. I am implementing an approach which triangulates both the dartboard and the dart across frames to model the dart’s parabolic flight and determined its intersection with the dartboard plane equation. The dartboard has to be triangulated by detecting three distinct reference markers (such as LEDs or retroreflective tape) attached on the edges, so both cameras could map the correct points to be triangulated. I am still continuing to refine the system and am currently facing a challenge with the computational lag that prevents real-time 30 fps tracking.

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

### Triangulation Mathematics
![Diagram and Math](https://github.com/abisheikashok/-Smart-Motion-Capture-System/blob/aa2d4a5c110eca87cadbd1d43dbfea511b78fc9b/Diagram%26Math.png)

### CAD Design (Click on the image to view the model)
[![Camera Lock Mount](https://github.com/abisheikashok/-Smart-Motion-Capture-System/blob/752beec581bf4c9687b445ee4616782097070732/CAD%20Design.png)](https://github.com/abisheikashok/-Smart-Motion-Capture-System/blob/b41ed5e3cfe2660e48bb3dea2031848e713ede65/Rod%20attachment%201.stl)

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
- Stereo Vision Geometry (Triangulation)
- Regression-Based Camera Calibration

---

## Contributors

| Contributor | Profile | Contributions |
|---|---|---|
| Ashok Abisheik | [GitHub](https://github.com/abisheikashok) | Stereo vision pipeline, triangulation, OpenCV implementation, calibration modeling |
| Shreyas Panda |  | Hardware setup, CAD mounting system, calibration support |

---

```
