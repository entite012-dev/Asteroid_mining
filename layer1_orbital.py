from astroquery.jplhorizons import Horizons
import pandas as pd
import numpy as np

# Fetch orbital elements directly
obj = Horizons(
    id="375103",
    location="500@10",
    epochs={"start": "2026-05-09",
            "stop": "2026-06-15",
            "step": "1d"}
)

# Get vectors (x,y,z position in space)
vec = obj.vectors()

df = pd.DataFrame({
    "date": vec["datetime_str"],
    "x": vec["x"],
    "y": vec["y"],
    "z": vec["z"],
    "vx": vec["vx"],
    "vy": vec["vy"],
    "vz": vec["vz"]
})

df.to_csv("orbital_vectors.csv", index=False)
print(df.head(10))