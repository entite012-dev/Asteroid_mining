import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

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

features = ["t", "t2", "t3"] + \
           [f"sin_{i}t" for i in range(1,8)] + \
           [f"cos_{i}t" for i in range(1,8)]

# Split — train on 2020-2025, test on 2026
train = df[df["date"] < "2026-01-01"]
test  = df[df["date"] >= "2026-01-01"]

X_train = train[features].values
X_test  = test[features].values
y_ra_train  = train["ra_unwrapped"].values
y_ra_test   = test["ra_unwrapped"].values
y_dec_train = train["dec"].values
y_dec_test  = test["dec"].values

model_ra  = RandomForestRegressor(n_estimators=200, random_state=42)
model_dec = RandomForestRegressor(n_estimators=200, random_state=42)

model_ra.fit(X_train, y_ra_train)
model_dec.fit(X_train, y_dec_train)

ra_error  = mean_absolute_error(y_ra_test, model_ra.predict(X_test))
dec_error = mean_absolute_error(y_dec_test, model_dec.predict(X_test))

print(f"Real RA error on 2026 data:  {ra_error:.4f} hours")
print(f"Real DEC error on 2026 data: {dec_error:.4f} degrees")

# Predict today
today_ts = int(pd.Timestamp("2026-05-09").timestamp())
t_today = (today_ts - t_min) / (t_max - t_min)
x_today = [t_today, t_today**2, t_today**3]
for i in range(1, 8):
    x_today.append(np.sin(2 * i * np.pi * t_today))
    x_today.append(np.cos(2 * i * np.pi * t_today))

pred_ra  = model_ra.predict([x_today])[0] % 24
pred_dec = model_dec.predict([x_today])[0]

print(f"\nPredicted position today 2026-05-09:")
print(f"RA:  {pred_ra:.4f} hours")
print(f"DEC: {pred_dec:.4f} degrees")