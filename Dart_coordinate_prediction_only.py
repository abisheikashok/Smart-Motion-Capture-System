import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


# CAMERA SETUP

cap1 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)

for cap in (cap1, cap2):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)

IMAGE_H = 1080
BASELINE = 111.9  # cm


# ANGLE CALCULATION
def calculate_angles(x, y):
    y_inv = IMAGE_H - y

    Anglex = (
        0.038002 * x
        - 0.001274 * y_inv
        - 0.000001 * x**2
        + 0.000001 * x * y_inv
        - 35.921325
    )

    Angley = (
        -0.000720 * x
        - 0.039996 * y_inv
        + 0.000001 * x * y_inv
        + 21.683713
    )

    return math.radians(Anglex), math.radians(Angley)


# TRIANGULATION

def calculate_3d_position(ax1, ay1, ax2, ay2):
    delta = ax1 - ax2
    if abs(delta) < 1e-4:
        return None

    Z = (BASELINE * math.cos(ax1) * math.cos(ax2)) / math.sin(delta)
    Z = abs(Z)

    X = Z * math.tan(ax1)
    Y = Z * math.tan(ay1)

    return X, Y, Z


# DART TIP DETECTION

def detect_dart_tip(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (35, 50, 50), (85, 255, 255))

    mask = cv2.medianBlur(mask, 7)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    best = None
    best_score = 0

    for c in contours:
        area = cv2.contourArea(c)
        if area < 200:
            continue

        x, y, w, h = cv2.boundingRect(c)
        aspect_ratio = h / (w + 1e-5)
        score = area * aspect_ratio

        if score > best_score:
            best_score = score
            best = c

    if best is None:
        return None

    tip = tuple(best[best[:,:,1].argmin()][0])
    return int(tip[0]), int(tip[1])


# COORDINATE DISPLAY WINDOW

def draw_coordinates_window(X, Y, Z):
    window = np.zeros((300, 600, 3), dtype=np.uint8)

    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1.3
    thickness = 3
    color = (0, 255, 0)

    cv2.putText(window, f"X: {X:.1f} cm", (40, 80), font, scale, color, thickness)
    cv2.putText(window, f"Y: {Y:.1f} cm", (40, 150), font, scale, color, thickness)
    cv2.putText(window, f"Z: {Z:.1f} cm", (40, 220), font, scale, color, thickness)

    cv2.imshow("3D Coordinates", window)


# 3D POINT VISUALIZATION SETUP

plt.ion()
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection="3d")

ax.set_xlabel("X (cm)")
ax.set_ylabel("Y (cm)")
ax.set_zlabel("Z (cm)")
ax.set_title("Live Dart MoCap Point")


# MAIN LOOP

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    if not ret1 or not ret2:
        break

    tip1 = detect_dart_tip(frame1)
    tip2 = detect_dart_tip(frame2)

    if tip1 and tip2:
        x1, y1 = tip1
        x2, y2 = tip2

        cv2.circle(frame1, tip1, 6, (0, 255, 0), -1)
        cv2.circle(frame2, tip2, 6, (0, 255, 0), -1)

        ax1, ay1 = calculate_angles(x1, y1)
        ax2, ay2 = calculate_angles(x2, y2)

        coords = calculate_3d_position(ax1, ay1, ax2, ay2)

        if coords:
            X, Y, Z = coords

            # Update 3D Graph
            ax.cla()
            ax.set_xlabel("X (cm)")
            ax.set_ylabel("Y (cm)")
            ax.set_zlabel("Z (cm)")
            ax.set_title("Live Dart Position")

            ax.scatter(X, Y, Z, s=80)
            ax.set_xlim(-100, 100)
            ax.set_ylim(-100, 100)
            ax.set_zlim(0, 300)

            plt.pause(0.001)

            # Update Coordinate Window
            draw_coordinates_window(X, Y, Z)

    cv2.imshow("Left Camera", cv2.resize(frame1, (960, 540)))
    cv2.imshow("Right Camera", cv2.resize(frame2, (960, 540)))

    if cv2.waitKey(1) & 0xFF == 27:
        break


# CLEANUP

cap1.release()
cap2.release()
cv2.destroyAllWindows()
plt.ioff()
plt.show()
