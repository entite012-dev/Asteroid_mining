import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import requests

# Load and train model (same as before)
df = pd.read_csv("historical_clean.csv")
df["date_num"] = pd.to_datetime(df["date"]).astype(np.int64) // 10**9
ra = df["ra"].values
ra_unwrapped = np.unwrap(ra * (2 * np.pi / 24)) * (24 / (2 * np.pi))
df["ra_unwrapped"] = ra_unwrapped
t_min = df["date_num"].min()
t_max = df["date_num"].max()
df["t"] = (df["date_num"] - t_min) / (t_max - t_min)
for i in range(1, 8):
    df[f"sin_{i}t"] = np.sin(2 * i * np.pi * df["t"])
    df[f"cos_{i}t"] = np.cos(2 * i * np.pi * df["t"])
df["t2"] = df["t"] ** 2
df["t3"] = df["t"] ** 3
features = ["t", "t2", "t3"] + [f"sin_{i}t" for i in range(1,8)] + [f"cos_{i}t" for i in range(1,8)]
X = df[features].values
model_ra = RandomForestRegressor(n_estimators=200, random_state=42)
model_dec = RandomForestRegressor(n_estimators=200, random_state=42)
model_ra.fit(X, df["ra_unwrapped"].values)
model_dec.fit(X, df["dec"].values)

# Get today's actual position from Horizons
url = "https://ssd.jpl.nasa.gov/api/horizons.api"
params = {
    "format": "json",
    "COMMAND": "'375103'",
    "OBJ_DATA": "'NO'",
    "MAKE_EPHEM": "'YES'",
    "EPHEM_TYPE": "'OBSERVER'",
    "CENTER": "'500@399'",
    "START_TIME": "'2026-05-09'",
    "STOP_TIME": "'2026-05-10'",
    "STEP_SIZE": "'1d'",
    "QUANTITIES": "'1'"
}
response = requests.get(url, params=params)
data = response.json()
raw = data["result"]
start = raw.find("$$SOE") + 5
end = raw.find("$$EOE")
line = raw[start:end].strip().split("\n")[0].split()
actual_ra = float(line[2]) + float(line[3])/60 + float(line[4])/3600
sign = -1 if line[5].startswith("-") else 1
actual_dec = sign * (abs(float(line[5])) + float(line[6])/60 + float(line[7])/3600)

# Predict today
today_ts = int(pd.Timestamp("2026-05-09").timestamp())
t_today = (today_ts - t_min) / (t_max - t_min)
x_today = [t_today, t_today**2, t_today**3]
for i in range(1, 8):
    x_today.append(np.sin(2 * i * np.pi * t_today))
    x_today.append(np.cos(2 * i * np.pi * t_today))

pred_ra = model_ra.predict([x_today])[0] % 24
pred_dec = model_dec.predict([x_today])[0]

print("=" * 40)
print("LAYER 1 VALIDATION RESULTS")
print("=" * 40)
print(f"Actual  RA:  {actual_ra:.4f} hours")
print(f"Predicted RA:{pred_ra:.4f} hours")
print(f"RA difference: {abs(actual_ra - pred_ra):.4f} hours")
print()
print(f"Actual  DEC:  {actual_dec:.4f} degrees")
print(f"Predicted DEC:{pred_dec:.4f} degrees")
print(f"DEC difference: {abs(actual_dec - pred_dec):.4f} degrees")
print("=" * 40)