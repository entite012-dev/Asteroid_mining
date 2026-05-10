import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("historical_clean.csv")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.plot(df["date"], df["ra"], color="blue")
ax1.set_title("Right Ascension over time")
ax1.set_ylabel("RA (hours)")
ax1.tick_params(axis='x', rotation=45)

ax2.plot(df["date"], df["dec"], color="orange")
ax2.set_title("Declination over time")
ax2.set_ylabel("DEC (degrees)")
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig("orbit_pattern.png")
print("Plot saved as orbit_pattern.png")
