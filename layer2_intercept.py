import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from astroquery.jplhorizons import Horizons

print("=" * 60)
print("🛸  SPACE STATION — INTERCEPT CALCULATOR")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# Load decisions
df = pd.read_csv("layer2_decisions.csv")

# Get top M-type target
target = df[df["type"] == "M"].iloc[0]
target_name = target["name"]
clean_id = target_name.split("(")[-1].replace(")", "").strip()

print(f"\n🎯 Target: {target_name}")
print(f"   EM Score: {target['em_score']}/100")
print(f"   Size: {target['size_km']:.3f} km")

# ==========================================
# FETCH FUTURE POSITIONS — NEXT 12 MONTHS
# ==========================================

print("\n📡 Fetching future trajectory...")

obj = Horizons(
    id=clean_id,
    location="500@10",
    epochs={
        "start": "2026-05-10",
        "stop":  "2027-05-10",
        "step":  "30d"
    }
)
vec = obj.vectors()

positions = []
for row in vec:
    positions.append({
        "date": str(row["datetime_str"]),
        "x": float(row["x"]),
        "y": float(row["y"]),
        "z": float(row["z"]),
        "vx": float(row["vx"]),
        "vy": float(row["vy"]),
        "vz": float(row["vz"]),
    })

pos_df = pd.DataFrame(positions)

# Earth position is approximately 1 AU from sun
# Calculate distance from Earth at each point
# Earth moves too — approximate Earth as circular orbit
def earth_position(date_str):
    # Clean Horizons date format
    clean = date_str.replace("A.D. ", "").strip()
    clean = clean.replace("-Jan-", "-01-").replace("-Feb-", "-02-")
    clean = clean.replace("-Mar-", "-03-").replace("-Apr-", "-04-")
    clean = clean.replace("-May-", "-05-").replace("-Jun-", "-06-")
    clean = clean.replace("-Jul-", "-07-").replace("-Aug-", "-08-")
    clean = clean.replace("-Sep-", "-09-").replace("-Oct-", "-10-")
    clean = clean.replace("-Nov-", "-11-").replace("-Dec-", "-12-")
    t = pd.Timestamp(clean[:10])
    day_of_year = t.day_of_year
    angle = 2 * np.pi * day_of_year / 365.25
    return np.array([np.cos(angle), np.sin(angle), 0.0])

pos_df["earth_x"] = pos_df["date"].apply(lambda d: earth_position(d[:20])[0])
pos_df["earth_y"] = pos_df["date"].apply(lambda d: earth_position(d[:20])[1])

pos_df["dist_from_earth_au"] = np.sqrt(
    (pos_df["x"] - pos_df["earth_x"])**2 +
    (pos_df["y"] - pos_df["earth_y"])**2 +
    pos_df["z"]**2
)
pos_df["dist_from_earth_km"] = pos_df["dist_from_earth_au"] * 150e6

# ==========================================
# FIND BEST LAUNCH WINDOW
# ==========================================

# Best window = when asteroid is closest to Earth
best_idx = pos_df["dist_from_earth_km"].idxmin()
best = pos_df.iloc[best_idx]

print("\n" + "=" * 60)
print("🪟  LAUNCH WINDOW ANALYSIS")
print("=" * 60)

for _, row in pos_df.iterrows():
    marker = " ⬅ BEST WINDOW" if row["date"] == best["date"] else ""
    print(f"{row['date'][:20]} | Distance: {row['dist_from_earth_km']:>20,.0f} km{marker}")

# ==========================================
# INTERCEPT ROUTE
# ==========================================

print("\n" + "=" * 60)
print("🚀  INTERCEPT ROUTE")
print("=" * 60)

# Travel time estimation
# Current spacecraft can do ~20 km/s
SPACECRAFT_SPEED = 20  # km/s
SECONDS_PER_DAY = 86400

travel_km = best["dist_from_earth_km"]
travel_seconds = travel_km / SPACECRAFT_SPEED
travel_days = travel_seconds / SECONDS_PER_DAY

launch_date = datetime.now() + timedelta(days=30)
arrival_date = launch_date + timedelta(days=travel_days)

print(f"Target:          {target_name}")
print(f"Best approach:   {best['date'][:20]}")
print(f"Distance:        {best['dist_from_earth_km']:,.0f} km")
print(f"Travel time:     {travel_days:.0f} days ({travel_days/365:.1f} years)")
print(f"Launch date:     {launch_date.strftime('%Y-%m-%d')}")
print(f"Arrival date:    {arrival_date.strftime('%Y-%m-%d')}")
print(f"Asteroid pos:    X={best['x']:.4f} Y={best['y']:.4f} Z={best['z']:.4f} AU")

# ==========================================
# ENERGY ESTIMATION
# ==========================================

print("\n" + "=" * 60)
print("⚡  ENERGY ESTIMATION")
print("=" * 60)

# EM machine power needed based on asteroid size and speed
asteroid_mass_kg = (4/3) * np.pi * (target["size_km"]*1000/2)**3 * 5000
em_force_needed = asteroid_mass_kg * 0.001  # tiny deceleration needed
em_power_mw = em_force_needed / 1e6

print(f"Asteroid mass:     {asteroid_mass_kg:.2e} kg")
print(f"EM force needed:   {em_force_needed:.2e} Newtons")
print(f"EM power needed:   {em_power_mw:.2f} Megawatts")

# Save intercept plan
intercept_plan = {
    "target": target_name,
    "launch_date": launch_date.strftime("%Y-%m-%d"),
    "arrival_date": arrival_date.strftime("%Y-%m-%d"),
    "travel_days": round(travel_days),
    "distance_km": round(best["dist_from_earth_km"]),
    "asteroid_mass_kg": asteroid_mass_kg,
    "em_power_mw": em_power_mw,
    "target_x": best["x"],
    "target_y": best["y"],
    "target_z": best["z"]
}

pd.DataFrame([intercept_plan]).to_csv("intercept_plan.csv", index=False)
print("\n✅ Intercept plan saved to intercept_plan.csv")
print("=" * 60)