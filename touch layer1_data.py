import requests
import pandas as pd

API_KEY = "your_NASA_API_KEY_HERE"

url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2026-05-09&end_date=2026-05-16&api_key={API_KEY}"

response = requests.get(url)
data = response.json()

asteroids = []

for date, neos in data["near_earth_objects"].items():
    for neo in neos:
        ca = neo["close_approach_data"][0]
        asteroids.append({
            "name": neo["name"],
            "date": ca["close_approach_date"],
            "size_km": (neo["estimated_diameter"]["kilometers"]["estimated_diameter_min"] +
                       neo["estimated_diameter"]["kilometers"]["estimated_diameter_max"]) / 2,
            "speed_km_s": float(ca["relative_velocity"]["kilometers_per_second"]),
            "miss_distance_km": float(ca["miss_distance"]["kilometers"]),
            "hazardous": neo["is_potentially_hazardous_asteroid"]
        })

df = pd.DataFrame(asteroids)
df = df.sort_values("size_km", ascending=False)
df.to_csv("asteroids.csv", index=False)
print(f"Saved {len(df)} asteroids!")
print(df.head(10))