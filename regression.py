import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# =========================
# LOAD DATA
# =========================

file_path = r"C:\Abisheik\Smart Motion Capture System\callibration\logitechc920.xlsx"

df = pd.read_excel(file_path)

# Remove accidental spaces in column names
df.columns = df.columns.str.strip()

required_columns = ['Angle X', 'Pixel X', 'Pixel Y']

# Check columns exist
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")

# =========================
# CLEAN DATA
# =========================

df_clean = df[required_columns].copy()

# Replace inf values with NaN
df_clean.replace([np.inf, -np.inf], np.nan, inplace=True)

# Remove NaN rows
df_clean.dropna(inplace=True)

# Convert to float
angle = df_clean['Angle X'].astype(float).values
pixel_x = df_clean['Pixel X'].astype(float).values
pixel_y = df_clean['Pixel Y'].astype(float).values

# Check enough points
if len(angle) < 6:
    raise ValueError("Need at least 6 valid points for quadratic fitting")

# =========================
# MODEL DEFINITIONS
# =========================

def quadratic_model(X, a, b, c, d, e, f):
    px, py = X
    return (
        a * px +
        b * py +
        c * px**2 +
        d * py**2 +
        e * px * py +
        f
    )

def simple_model(X, a, b, c, d):
    px, py = X
    return (
        a * px +
        b * py +
        c * px * py +
        d
    )

# =========================
# FIT MODEL
# =========================

try:
    params, _ = curve_fit(
        quadratic_model,
        (pixel_x, pixel_y),
        angle,
        maxfev=10000
    )

    model_type = "quadratic"
    print("Quadratic model fitted successfully.")

except Exception as err:

    print("Quadratic fitting failed:")
    print(err)

    params, _ = curve_fit(
        simple_model,
        (pixel_x, pixel_y),
        angle,
        maxfev=10000
    )

    model_type = "simple"
    print("Fallback simple model fitted.")

# =========================
# PREDICTION FUNCTION
# =========================

def predict_angle(x, y):

    if model_type == "quadratic":
        return quadratic_model((x, y), *params)

    return simple_model((x, y), *params)

# =========================
# EQUATION STRING
# =========================

def full_equation():

    if model_type == "quadratic":

        return (
            f"Angle = "
            f"{params[0]:.6f}*x + "
            f"{params[1]:.6f}*y + "
            f"{params[2]:.6f}*x² + "
            f"{params[3]:.6f}*y² + "
            f"{params[4]:.6f}*x*y + "
            f"{params[5]:.6f}"
        )

    return (
        f"Angle = "
        f"{params[0]:.6f}*x + "
        f"{params[1]:.6f}*y + "
        f"{params[2]:.6f}*x*y + "
        f"{params[3]:.6f}"
    )

# =========================
# TEST PREDICTION
# =========================

center_x = 960
center_y = 540

predicted = predict_angle(center_x, center_y)

print(f"\nPredicted Angle: {predicted:.2f} degrees")

# =========================
# PRINT PARAMETERS
# =========================

print("\nModel Type:", model_type)

print("\nParameters:")
for i, p in enumerate(params):
    print(f"p{i}: {p:.6f}")

print("\nEquation:")
print(full_equation())

# =========================
# R-SQUARED
# =========================

if model_type == "quadratic":
    predictions = quadratic_model((pixel_x, pixel_y), *params)
else:
    predictions = simple_model((pixel_x, pixel_y), *params)

ss_res = np.sum((angle - predictions) ** 2)
ss_tot = np.sum((angle - np.mean(angle)) ** 2)

r_squared = 1 - (ss_res / ss_tot)

print(f"\nR² Score: {r_squared:.4f}")