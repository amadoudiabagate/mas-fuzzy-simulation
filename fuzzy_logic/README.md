# fuzzy_logic — Modular Fuzzy Inference (Clinic satisfaction)

This package modularizes the fuzzy logic system from your base script into a clean, testable structure.

## Structure
```
fuzzy_logic/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── membership_functions.py
│   └── rule_base.py
├── fuzzy_system.py
├── utils/
│   ├── __init__.py
│   └── visualization.py
└── tests/
    ├── __init__.py
    └── test_fuzzy_system.py
```

## Usage
Install dependencies (in your project):
```
pip install scikit-fuzzy matplotlib numpy
```

Generate membership plots and a demo surface:
```python
from fuzzy_logic.fuzzy_system import build_system, VAR_LABELS
from fuzzy_logic.utils.visualization import save_membership_plots, save_surface

system, vars_map, U = build_system(step='fine')
save_membership_plots(U, vars_map, outdir="output/figures/fuzzy_logic")
save_surface(system, VAR_LABELS['ci'], VAR_LABELS['sc'], outdir="output/figures/fuzzy_logic")
```

Evaluate the system for a given set of inputs:
```python
from fuzzy_logic.fuzzy_system import evaluate, VAR_LABELS
result = evaluate({
    VAR_LABELS['ci']: 7,
    VAR_LABELS['sc']: 6,
    VAR_LABELS['po']: 8,
    VAR_LABELS['ra']: 7,
})
print(result)  # {'Overall satisfaction': ...}
```

## Notes
- Univers **0..10** (base resolution `np.arange(0,11,1)`), with an optional finer grid (`step='fine'`).
- Figures are saved to `output/figures/fuzzy_logic` (folders created automatically).
- Designed to align with the rules and sets used in your original script.