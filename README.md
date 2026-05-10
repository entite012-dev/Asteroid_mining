# Asteroid_mining
# Asteroid Mining Concept Simulation

A Python learning project that uses real NASA 
APIs to explore asteroid tracking and simplified 
mining concepts.

---

## Motivation

Surface mining causes significant environmental 
damage. This project explores asteroid mining 
as a concept worth studying — using real space 
data to build a basic simulation pipeline.

This is a self-directed learning project built 
to develop Python skills and explore space science.

---

## What This Project Does

Connects to NASA public APIs to fetch real 
near-Earth asteroid data, runs basic orbital 
predictions, and simulates a theoretical 
asteroid capture concept.

---

## Project Structure

### Layer 1 — Detection
- layer1_data.py — NASA NeoWs API connection
- layer1_historical.py — JPL Horizons data
- layer1_parse.py — Data cleaning
- layer1_predict.py — Basic prediction model
- layer1_physics.py — Orbital mechanics
- layer1_plot.py — Visualization
- layer1_multi.py — Multi asteroid tracker
- layer1_composition.py — Composition scoring
- layer1_alerts.py — Alert system
- layer1_monitor.py — Monitoring pipeline

### Layer 2 — Mission Planning
- layer2_station.py — Mission decisions
- layer2_intercept.py — Route calculator
- layer2_windows.py — Launch windows

### Layer 3 — Simulation
- layer3_em_machine.py — EM capture simulation

---

## Setup

Clone the repo:
git clone https://github.com/yourusername/asteroid-mining
cd asteroid-mining

Create virtual environment:
python -m venv asteroid_env
source asteroid_env/bin/activate

Install dependencies:
pip install -r requirements.txt

Get a free NASA API key at api.nasa.gov
Add it to layer1_data.py

Run the pipeline:
python layer1_data.py
python layer1_multi.py
python layer1_composition.py
python layer1_alerts.py
python layer2_station.py
python layer3_em_machine.py

---

## Data Sources

- NASA NeoWs API — near earth asteroid feed
- JPL Horizons API — historical orbital data
- SMASS — spectral composition database

All data is publicly available and free.

---

## Important Limitations

This is a student learning project.
Please read these carefully:

- EM capture physics is heavily simplified
- Energy calculations are rough approximations
- Solar farm concept is not engineered
- Composition types are partially estimated
- Mission timelines assume ideal conditions
- Results are not peer reviewed or validated

Do not treat any outputs as real 
engineering calculations.

---

## Skills Demonstrated

- REST API integration
- Data cleaning and parsing
- Basic orbital mechanics
- Machine learning basics
- Physics based modelling
- Automated pipeline design

---

## Status

Work in progress.
Physics models need significant 
improvement and proper validation.

---

## Author

Self directed learning project.
Built using publicly available 
NASA data and open source Python libraries.

---

## License

MIT License — free to use and learn from.
