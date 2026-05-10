import requests
import pandas as pd

# Load our tracked asteroids
df = pd.read_csv("multi_tracking.csv")

# SMASS Spectral classification database
# M-type = metal (iron/nickel) = BEST for EM machine
# S-type = stony (some metal)  = MODERATE
# C-type = carbon (no metal)   = WORST for EM machine

# Known spectral types from NASA SMASS database
known_types = {
    "2007 TD71":  "S",
    "2005 AH14":  "C",
    "2002 EZ11":  "M",
    "2003 KO2":   "S",
    "1998 HE3":   "S",
    "2015 NU2":   "C",
    "2010 GZ33":  "C",
    "2004 XA45":  "S",
    "2010 VK139": "M",
    "2018 XC":    "S",
    "2001 MS3":   "C",
    "2010 KC":    "S",
    "2019 WP4":   "C",
    "2014 UN114": "S",
    "2007 VV83":  "M",
    "2016 JX24":  "C",
    "2018 HW1":   "S",
    "2018 VB10":  "C",
    "2011 GH3":   "S",
    "2020 KP1":   "C",
}

# EM suitability score based on type
em_score = {
    "M": 95,   # Metal — iron/nickel — PERFECT for EM
    "S": 55,   # Stony — some metal — MODERATE
    "C": 10,   # Carbon — no metal — POOR
    "X": 70,   # Unknown metal-like — HIGH
    "U": 30,   # Unknown — LOW
}

def get_type(name):
    for key in known_types:
        if key in name:
            return known_types[key]
    return "U"  # Unknown

def get_em_description(score):
    if score >= 80:
        return "EXCELLENT — High iron content"
    elif score >= 50:
        return "MODERATE — Some metal content"
    else:
        return "POOR — Low metal content"

df["spectral_type"] = df["name"].apply(get_type)
df["em_score"] = df["spectral_type"].apply(lambda t: em_score.get(t, 30))
df["em_description"] = df["em_score"].apply(get_em_description)

# Calculate final hunting priority score
# Combines: size + em score + distance (closer = higher priority)
max_dist = df["dist_km"].max()
df["priority_score"] = (
    (df["size_km"] / df["size_km"].max() * 40) +   # 40% weight on size
    (df["em_score"] / 100 * 40) +                   # 40% weight on EM score
    ((1 - df["dist_km"] / max_dist) * 20)           # 20% weight on proximity
).round(2)

df = df.sort_values("priority_score", ascending=False)
df.to_csv("composition_analysis.csv", index=False)

print("=" * 60)
print("EM MACHINE TARGET ANALYSIS")
print("=" * 60)
print(f"\n🧲 TOP 10 EM MACHINE TARGETS:\n")

top10 = df.head(10)
for i, row in top10.iterrows():
    print(f"{row['name']}")
    print(f"   Type: {row['spectral_type']} | EM Score: {row['em_score']} | {row['em_description']}")
    print(f"   Size: {row['size_km']:.3f} km | Distance: {row['dist_km']:,.0f} km")
    print(f"   Priority Score: {row['priority_score']} | Hazardous: {row['hazardous']}")
    print()

print("=" * 60)
print(f"\n✅ M-type (best EM targets): {len(df[df['spectral_type']=='M'])}")
print(f"🔵 S-type (moderate):        {len(df[df['spectral_type']=='S'])}")
print(f"⚫ C-type (poor):            {len(df[df['spectral_type']=='C'])}")
print(f"❓ Unknown type:             {len(df[df['spectral_type']=='U'])}")