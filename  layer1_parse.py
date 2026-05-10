import pandas as pd

with open("historical_raw.txt", "r") as f:
    raw = f.read()

start = raw.find("$$SOE") + 5
end = raw.find("$$EOE")
block = raw[start:end].strip()

rows = []
for line in block.split("\n"):
    line = line.strip()
    if not line:
        continue
    parts = line.split()
    if len(parts) >= 8:
        date = parts[0]
        # RA = hours + minutes/60 + seconds/3600
        ra = float(parts[2]) + float(parts[3])/60 + float(parts[4])/3600
        # DEC = degrees + minutes/60 + seconds/3600 with sign
        sign = -1 if parts[5].startswith("-") else 1
        dec = sign * (abs(float(parts[5])) + float(parts[6])/60 + float(parts[7])/3600)
        rows.append({
            "date": date,
            "ra": ra,
            "dec": dec
        })

df = pd.DataFrame(rows)
df.to_csv("historical_clean.csv", index=False)
print(f"Saved {len(df)} rows!")
print(df.head(10))