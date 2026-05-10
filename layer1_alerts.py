import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Load composition analysis
df = pd.read_csv("composition_analysis.csv")

# Alert thresholds
ALERT_RULES = {
    "min_em_score": 55,
    "min_size_km": 0.05,
    "max_dist_km": 160_000_000,
    "min_priority": 35
}

def check_alerts(df):
    alerts = []
    for _, row in df.iterrows():
        triggered = []

        if row["em_score"] >= ALERT_RULES["min_em_score"]:
            triggered.append(f"EM Score {row['em_score']}/100")

        if row["size_km"] >= ALERT_RULES["min_size_km"]:
            triggered.append(f"Size {row['size_km']:.3f} km")

        if row["dist_km"] <= ALERT_RULES["max_dist_km"]:
            triggered.append(f"Close approach {row['dist_km']:,.0f} km")

        if row["priority_score"] >= ALERT_RULES["min_priority"]:
            triggered.append(f"Priority {row['priority_score']}")

        if len(triggered) >= 3:
            alerts.append({
                "name": row["name"],
                "type": row["spectral_type"],
                "em_score": row["em_score"],
                "size_km": row["size_km"],
                "dist_km": row["dist_km"],
                "priority": row["priority_score"],
                "hazardous": row["hazardous"],
                "reasons": triggered
            })

    return alerts

alerts = check_alerts(df)

print("=" * 60)
print("🚨 ASTEROID HUNTER — ALERT SYSTEM")
print(f"Scan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

if alerts:
    print(f"\n⚠️  {len(alerts)} TARGETS TRIGGERED ALERTS!\n")
    for a in alerts:
        print(f"🎯 {a['name']}")
        print(f"   Type: {a['type']} | EM: {a['em_score']}/100 | Priority: {a['priority']}")
        print(f"   Size: {a['size_km']:.3f} km | Distance: {a['dist_km']:,.0f} km")
        print(f"   Hazardous: {a['hazardous']}")
        print(f"   Triggered: {' | '.join(a['reasons'])}")
        print()
else:
    print("\n✅ No alerts — no targets meet criteria right now")

# Save alerts to file
alerts_df = pd.DataFrame(alerts)
if len(alerts_df) > 0:
    alerts_df.to_csv("active_alerts.csv", index=False)
    print(f"Alerts saved to active_alerts.csv")

print("=" * 60)