import requests
import pandas as pd

url = "https://ssd.jpl.nasa.gov/api/horizons.api"

params = {
    "format": "json",
    "COMMAND": "'375103'",
    "OBJ_DATA": "'NO'",
    "MAKE_EPHEM": "'YES'",
    "EPHEM_TYPE": "'OBSERVER'",
    "CENTER": "'500@399'",
    "START_TIME": "'2020-01-01'",
    "STOP_TIME": "'2026-05-09'",
    "STEP_SIZE": "'1d'",
    "QUANTITIES": "'1'"
}

response = requests.get(url, params=params)
data = response.json()

with open("historical_raw.txt", "w") as f:
    f.write(data["result"])

print("Historical data saved!")
print(data["result"][:500])
