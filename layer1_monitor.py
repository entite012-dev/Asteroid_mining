import subprocess
import time
from datetime import datetime

# How often to scan (seconds)
SCAN_INTERVAL = 3600  # every 1 hour

def run_pipeline():
    print("\n" + "=" * 60)
    print(f"🛰️  ASTEROID HUNTER — LIVE MONITOR")
    print(f"Scan started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    steps = [
        ("touch layer1_data.py",        "📡 Fetching live NASA data"),
        ("layer1_multi.py",       "🌍 Tracking all asteroids"),
        ("layer1_composition.py", "🔬 Analyzing composition"),
        ("layer1_alerts.py",      "🚨 Checking alerts"),
    ]

    for script, description in steps:
        print(f"\n{description}...")
        result = subprocess.run(
            ["python", script],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ Done")
        else:
            print(f"❌ Error in {script}")
            print(result.stderr[:200])

    # Log scan
    with open("monitor_log.txt", "a") as f:
        f.write(f"{datetime.now()} — Scan complete\n")

    print(f"\n✅ Full scan complete!")
    print(f"Next scan in {SCAN_INTERVAL//60} minutes")
    print("=" * 60)

# Run immediately then loop
print("🚀 Starting Asteroid Hunter Monitor...")
print("Press CTRL+C to stop\n")

while True:
    try:
        run_pipeline()
        time.sleep(SCAN_INTERVAL)
    except KeyboardInterrupt:
        print("\n\n🛑 Monitor stopped by user")
        print("Layer 1 complete! 🌟")
        break