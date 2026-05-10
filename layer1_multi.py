from astroquery.jplhorizons import Horizons
import pandas as pd
import numpy as np
import time
import re

asteroids_df = pd.read_csv("asteroids.csv")

print(f"Tracking {len(asteroids_df)} asteroids...")
print("=" * 60)

def clean_id(name):
    # Try to extract designation like 2007 TD71
    match = re.search(r'\((\d{4}\s+\w+)\)', name)
    if match:
        return match.group(1)
    # Try numbered asteroid like 375103
    match = re.search(r'^(\d+)', name)
    if match:
        return match.group(1)
    # Just return cleaned name
    return name.strip("()")

results = []

for index, row in asteroids_df.iterrows():
    name = row["name"]
    clean = clean_id(name)
    print(f"Fetching: {name} → using id: {clean}")

    try:
        obj = Horizons(
            id=clean,
            location="500@10",
            epochs={"start": "2026-05-09",
                    "stop": "2026-05-10",
                    "step": "1d"}
        )
        vec = obj.vectors()
        v = vec[0]

        pred_x = float(v["x"]) + float(v["vx"])
        pred_y = float(v["y"]) + float(v["vy"])
        pred_z = float(v["z"]) + float(v["vz"])

        dist_au = np.sqrt(pred_x**2 + pred_y**2 + pred_z**2)
        dist_km = dist_au * 150e6

        results.append({
            "name": name,
            "id_used": clean,
            "x": round(float(v["x"]), 6),
            "y": round(float(v["y"]), 6),
            "z": round(float(v["z"]), 6),
            "pred_x": round(pred_x, 6),
            "pred_y": round(pred_y, 6),
            "pred_z": round(pred_z, 6),
            "dist_km": round(dist_km, 0),
            "hazardous": row["hazardous"],
            "size_km": row["size_km"],
            "speed_km_s": row["speed_km_s"]
        })

        print(f"  ✅ Distance: {dist_au:.4f} AU | {dist_km:,.0f} km")

    except Exception as e:
        print(f"  ❌ Failed: {e}")

    time.sleep(1)

results_df = pd.DataFrame(results)
results_df = results_df.sort_values("dist_km")
results_df.to_csv("multi_tracking.csv", index=False)

print("\n" + "=" * 60)
print(f"Successfully tracked {len(results_df)} asteroids!")
print("\nTop 5 closest:")
print(results_df[["name","dist_km","size_km","hazardous"]].head())