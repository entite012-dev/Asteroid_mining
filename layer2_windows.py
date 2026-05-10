import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from astroquery.jplhorizons import Horizons

print("=" * 60)
print("🛸  SPACE STATION — LAUNCH WINDOWS & DELTA-V")
print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# Load intercept plan
plan = pd.read_csv("intercept_plan.csv").iloc[0]
target_name = plan["target"]
clean_id = target_name.split("(")[-1].replace(")", "").strip()

print(f"\n🎯 Target: {target_name}")

# ==========================================
# FETCH 2 YEAR TRAJECTORY
# ==========================================

print("📡 Fetching 2 year trajectory...")

obj = Horizons(
    id=clean_id,
    location="500@10",
    epochs={
        "start": "2026-05-10",
        "stop":  "2028-05-10",
        "step":  "15d"
    }
)
vec = obj.vectors()

def clean_date(date_str):
    clean = str(date_str).replace("A.D. ", "").strip()
    months = {
        "-Jan-": "-01-", "-Feb-": "-02-", "-Mar-": "-03-",
        "-Apr-": "-04-", "-May-": "-05-", "-Jun-": "-06-",
        "-Jul-": "-07-", "-Aug-": "-08-", "-Sep-": "-09-",
        "-Oct-": "-10-", "-Nov-": "-11-", "-Dec-": "-12-"
    }
    for k, v in months.items():
        clean = clean.replace(k, v)
    return clean[:10]

def earth_position(date_str):
    t = pd.Timestamp(date_str)
    angle = 2 * np.pi * t.day_of_year / 365.25
    return np.array([np.cos(angle), np.sin(angle), 0.0])

positions = []
for row in vec:
    date = clean_date(row["datetime_str"])
    earth = earth_position(date)
    x, y, z = float(row["x"]), float(row["y"]), float(row["z"])
    vx, vy, vz = float(row["vx"]), float(row["vy"]), float(row["vz"])

    dist_au = np.sqrt(
        (x - earth[0])**2 +
        (y - earth[1])**2 +
        z**2
    )

    # Delta-V calculation (Hohmann transfer approximation)
    # Earth orbital velocity = 29.78 km/s
    # Target distance in AU
    earth_v = 29.78
    asteroid_dist_sun = np.sqrt(x**2 + y**2 + z**2)
    transfer_orbit_a = (1 + asteroid_dist_sun) / 2
    delta_v = earth_v * (np.sqrt(2 * asteroid_dist_sun / (transfer_orbit_a * (1 + asteroid_dist_sun))) +
                         np.sqrt(1 / transfer_orbit_a) - 1 -
                         np.sqrt(2 / (1 + asteroid_dist_sun) - 1 / asteroid_dist_sun))

    positions.append({
        "date": date,
        "x": x, "y": y, "z": z,
        "vx": vx, "vy": vy, "vz": vz,
        "dist_from_earth_km": dist_au * 150e6,
        "delta_v_km_s": abs(delta_v)
    })

pos_df = pd.DataFrame(positions)

# ==========================================
# TOP 3 LAUNCH WINDOWS
# ==========================================

# Score each window — closer + lower delta_v = better
pos_df["window_score"] = (
    (1 - pos_df["dist_from_earth_km"] / pos_df["dist_from_earth_km"].max()) * 50 +
    (1 - pos_df["delta_v_km_s"] / pos_df["delta_v_km_s"].max()) * 50
)

# Get top 3 windows at least 60 days apart
top_windows = []
used_dates = []

sorted_df = pos_df.sort_values("window_score", ascending=False)

for _, row in sorted_df.iterrows():
    date = pd.Timestamp(row["date"])
    too_close = False
    for used in used_dates:
        if abs((date - used).days) < 60:
            too_close = True
            break
    if not too_close:
        top_windows.append(row)
        used_dates.append(date)
    if len(top_windows) == 3:
        break

print("\n" + "=" * 60)
print("🪟  TOP 3 LAUNCH WINDOWS")
print("=" * 60)

for i, w in enumerate(top_windows):
    travel_days = w["dist_from_earth_km"] / (20 * 86400)
    launch = pd.Timestamp(w["date"]) - timedelta(days=travel_days)
    print(f"\n#{i+1} Window")
    print(f"   Arrival date:    {w['date']}")
    print(f"   Launch date:     {launch.strftime('%Y-%m-%d')}")
    print(f"   Distance:        {w['dist_from_earth_km']:,.0f} km")
    print(f"   Delta-V needed:  {w['delta_v_km_s']:.2f} km/s")
    print(f"   Travel time:     {travel_days:.0f} days")
    print(f"   Window score:    {w['window_score']:.2f}/100")

# ==========================================
# DELTA-V FULL ANALYSIS
# ==========================================

best = top_windows[0]

print("\n" + "=" * 60)
print("⚡  DELTA-V FUEL ANALYSIS — BEST WINDOW")
print("=" * 60)

# Spacecraft mass assumptions
DRY_MASS_KG = 5000        # spacecraft without fuel
ISP = 450                  # specific impulse (seconds) — ion thruster
G0 = 9.81                  # gravity constant

delta_v = best["delta_v_km_s"] * 1000  # convert to m/s

# Tsiolkovsky rocket equation
# mass_ratio = e^(delta_v / (Isp * g0))
mass_ratio = np.exp(delta_v / (ISP * G0))
fuel_mass = DRY_MASS_KG * (mass_ratio - 1)
total_mass = DRY_MASS_KG + fuel_mass

print(f"Delta-V required:    {best['delta_v_km_s']:.2f} km/s")
print(f"Spacecraft dry mass: {DRY_MASS_KG:,} kg")
print(f"Fuel required:       {fuel_mass:,.0f} kg")
print(f"Total launch mass:   {total_mass:,.0f} kg")
print(f"Mass ratio:          {mass_ratio:.2f}")

# Save windows
windows_df = pd.DataFrame(top_windows)
windows_df.to_csv("launch_windows.csv", index=False)
print("\n✅ Launch windows saved to launch_windows.csv")
print("=" * 60)