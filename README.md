# Clinic Multi-agent(s) System (12 agent(s))

This repository contains the Python code for the agent(s)-based clinic simulation and the fuzzy logic subsystem. It is prepared to support a research manuscript submission (e.g., *Informatica*).

## Project Structure
```
SMA_Clinic_12_Agents_EN/
  ├─ agent(s)/                      # agent(s) classes (English names)
  │   └─ Patient.py                 # Defines the Patient entity (not an agent)
  ├─ model.py                       # Mesa model (imports English agent(s) classes)
  ├─ README_EN.md                   # Mapping FR→EN (quick reference)
  ├─ README.md                      # This file (how to run, reproduce)
  ├─ requirements.txt               # Python dependencies
  └─ .gitignore                     # Common ignores for a clean repo
```

> **Note**  
> `Patient.py` defines the **Patient entity used in simulations** and is **not considered an agent**.  
> The system itself is composed of **12 agents** only, as described in the architecture.


## Environment & Installation
Python 3.9+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## How to Run
Run the Mesa model:
```bash
python model.py
```

> **Note**: If your original workflow uses notebooks or additional scripts, place them under `notebooks/` or update this README accordingly.

## Reproducibility Notes
- **Code**: Provided here with English agent(s) names for clarity and internationalization.
- **Data**: No raw patient data are included. You may add **synthetic** or **anonymized/aggregated** examples under a `data/` folder to illustrate usage without exposing sensitive information.

## Data & Ethics
Raw patient survey data are not shared due to privacy/ethics. Anonymized and aggregated datasets can be made available by the corresponding author upon reasonable request and in accordance with approved ethics and data-protection regulations.

## Citation
If you use this code, please cite the associated manuscript and acknowledge the repository in your references. You can also generate a Zenodo DOI and add it here later.

## License
MIT License (add your name and year below if you agree). See example:
```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
[...]
```


## Workflow Overview

1. **simulation**  
   Run the Mesa model to generate results as CSV:  
   ```bash
   python model.py
   ```  
   This will create files under `output/data/`.

2. **Analysis**  
   Use the analysis script to process the CSV and produce figures/tables:  
   ```bash
   python analysis/analysis_results.py
   ```  
   Results (figures, tables) will be saved under `output/figures/` and `output/tables/`.

> Note: The raw CSVs and generated figures/tables are ignored by Git to keep the repository clean. Only the code and pipeline are provided for reproducibility.


## Reproducible Workflow

### Step 1 — Run the simulation
This generates a CSV under `output/data/` with a timestamp in the filename.
```bash
python model.py
```

### Step 2 — Generate figures and tables from the CSV
Run the analysis script; it reads from `output/data/` and writes results under `output/figures/` and `output/tables/`.
```bash
python analysis/analysis_results.py
```

> Note: `output/` is ignored by Git on purpose (see `.gitignore`) because it contains generated artifacts.

### Alternative analysis script (no Word export)
To generate figures and tables without creating any Word files, run:
```bash
python analysis/analysis_results.py
```
