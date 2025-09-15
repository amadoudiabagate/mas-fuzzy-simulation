from fuzzy_logic.fuzzy_system import evaluate, VAR_LABELS

def test_basic_monotonicity():
    low = evaluate({VAR_LABELS['ci']: 1, VAR_LABELS['sc']: 1})
    high = evaluate({VAR_LABELS['ci']: 9, VAR_LABELS['sc']: 9})
    assert high[VAR_LABELS['os']] > low[VAR_LABELS['os']]

def test_output_key_exists():
    out = evaluate({VAR_LABELS['ci']: 5, VAR_LABELS['sc']: 5})
    assert VAR_LABELS['os'] in out