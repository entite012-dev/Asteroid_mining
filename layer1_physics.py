from astroquery.jplhorizons import Horizons
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error

# Get historical vectors 2020-2025 for training
print("Fetching historical data...")
hist = Horizons(
    id="375103",
    location="500@10",
    epochs={"start": "2020-01-01",
            "stop": "2025-12-31",
            "step": "30d"}
)
hist_vec = hist.vectors()

# Get 2026 real positions for validation
print("Fetching 2026 validation data...")
val = Horizons(
    id="375103",
    location="500@10",
    epochs={"start": "2026-01-01",
            "stop": "2026-05-09",
            "step": "1d"}
)
val_vec = val.vectors()

# Simple physics prediction
# Use velocity to predict next position
# new_pos = old_pos + velocity * time
print("\nPhysics-based prediction validation:")
print("=" * 50)

errors_x = []
errors_y = []
errors_z = []

val_df = val_vec.to_pandas()

for i in range(1, len(val_df)):
    prev = val_df.iloc[i-1]
    curr = val_df.iloc[i]

    # Predict using velocity (1 day = 1 step)
    pred_x = prev["x"] + prev["vx"]
    pred_y = prev["y"] + prev["vy"]
    pred_z = prev["z"] + prev["vz"]

    errors_x.append(abs(pred_x - curr["x"]))
    errors_y.append(abs(pred_y - curr["y"]))
    errors_z.append(abs(pred_z - curr["z"]))

print(f"X position error: {np.mean(errors_x):.6f} AU")
print(f"Y position error: {np.mean(errors_y):.6f} AU")
print(f"Z position error: {np.mean(errors_z):.6f} AU")
print(f"\n1 AU = 150 million km")
print(f"X error in km: {np.mean(errors_x)*150e6:,.0f} km")
print(f"Y error in km: {np.mean(errors_y)*150e6:,.0f} km")

# Predict tomorrow May 10
today = val_df.iloc[-1]
pred_x = today["x"] + today["vx"]
pred_y = today["y"] + today["vy"]
pred_z = today["z"] + today["vz"]

print(f"\nPredicted position tomorrow 2026-05-10:")
print(f"X: {pred_x:.6f} AU")
print(f"Y: {pred_y:.6f} AU")
print(f"Z: {pred_z:.6f} AU")