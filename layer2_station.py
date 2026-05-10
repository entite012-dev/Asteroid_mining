import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 60)
print("🛸  SPACE STATION — COMMAND CENTER")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# Load Layer 1 alerts
df = pd.read_csv("active_alerts.csv")

# Load tracking data
tracking = pd.read_csv("multi_tracking.csv")

# Load asteroids for speed data
asteroids = pd.read_csv("asteroids.csv")

# Merge tracking data
df = df.merge(tracking[["name","x","y","z","pred_x","pred_y","pred_z"]], 
              on="name", how="left")

# Merge speed data
df = df.merge(asteroids[["name","speed_km_s"]], 
              on="name", how="left")

# Fill any missing speeds
df["speed_km_s"] = df["speed_km_s"].fillna(15.0)

# Merge both datasets
df = df.merge(tracking[["name","x","y","z","pred_x","pred_y","pred_z"]], 
              on="name", how="left")

# ==========================================
# DECISION ENGINE
# ==========================================

def calculate_intercept_difficulty(row):
    # Closer + slower = easier to intercept
    dist_score = 1 - (row["dist_km"] / 200_000_000)
    speed_score = 1 - (row["speed_km_s"] / 35)
    return round((dist_score * 0.5 + speed_score * 0.5) * 100, 2)

def calculate_mission_value(row):
    # M-type large close asteroid = highest value
    em_weight    = row["em_score"] * 0.40
    size_weight  = (row["size_km"] / df["size_km"].max()) * 100 * 0.35
    dist_weight  = (1 - row["dist_km"] / df["dist_km"].max()) * 100 * 0.25
    return round(em_weight + size_weight + dist_weight, 2)

def mission_decision(row):
    if row["mission_value"] >= 60 and row["intercept_difficulty"] >= 40:
        return "🟢 LAUNCH MISSION"
    elif row["mission_value"] >= 40 and row["intercept_difficulty"] >= 30:
        return "🟡 MONITOR CLOSELY"
    else:
        return "🔴 LOW PRIORITY"

# Calculate scores
df["intercept_difficulty"] = df.apply(calculate_intercept_difficulty, axis=1)
df["mission_value"]        = df.apply(calculate_mission_value, axis=1)
df["decision"]             = df.apply(mission_decision, axis=1)
df["speed_km_s"]           = df["speed_km_s"].fillna(15.0)

# Sort by mission value
df = df.sort_values("mission_value", ascending=False)

# ==========================================
# COMMAND CENTER OUTPUT
# ==========================================

print("\n📋 MISSION DECISION BOARD:\n")

for _, row in df.iterrows():
    print(f"{row['decision']} — {row['name']}")
    print(f"   Mission Value:        {row['mission_value']}/100")
    print(f"   Intercept Difficulty: {row['intercept_difficulty']}/100")
    print(f"   EM Score:             {row['em_score']}/100")
    print(f"   Size:                 {row['size_km']:.3f} km")
    print(f"   Distance:             {row['dist_km']:,.0f} km")
    print(f"   Hazardous:            {row['hazardous']}")
    print()

# ==========================================
# FINAL COMMAND
# ==========================================

top = df.iloc[0]
print("=" * 60)
print("🎯 SPACE STATION PRIMARY TARGET:")
print("=" * 60)
print(f"Name:            {top['name']}")
print(f"Decision:        {top['decision']}")
print(f"Mission Value:   {top['mission_value']}/100")
print(f"EM Score:        {top['em_score']}/100")
print(f"Size:            {top['size_km']:.3f} km")
print(f"Distance:        {top['dist_km']:,.0f} km")
print(f"3D Position:     X={top.get('x','N/A')} Y={top.get('y','N/A')} Z={top.get('z','N/A')} AU")
print(f"Predicted Pos:   X={top.get('pred_x','N/A')} Y={top.get('pred_y','N/A')} Z={top.get('pred_z','N/A')} AU")
print("=" * 60)
print("\n🧲 SENDING TARGET TO EM MACHINE...")
print(f"TARGET LOCKED: {top['name']}")
print("=" * 60)

# Save decisions
df.to_csv("layer2_decisions.csv", index=False)
print("\n✅ Decisions saved to layer2_decisions.csv")