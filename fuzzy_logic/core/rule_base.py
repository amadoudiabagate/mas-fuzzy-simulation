from skfuzzy import control as ctrl

def build_rules(vars_map):
    ci = vars_map['Communication and Information']
    ra = vars_map['Reception and Accessibility']
    sc = vars_map['Staff competence']
    ei = vars_map['Environment and infrastructure']
    po = vars_map['Perceived Treatment Outcome']
    cb = vars_map['Cost and Billing']
    pi = vars_map['patient Involvement']
    rr = vars_map['Intention to Return and Recommend']
    os = vars_map['Overall satisfaction']

    rules = [
        # Very positive
        ctrl.Rule(ci['good'] & po['effective'] & ra['good'], os['high']),
        ctrl.Rule(pi['high'] & ci['good'], os['high']),
        ctrl.Rule(rr['high'] & ei['good'], os['high']),
        ctrl.Rule(ci['good'] & cb['affordable'] & po['effective'], os['high']),
        ctrl.Rule(sc['good'] & ra['acceptable'], os['high']),
        ctrl.Rule(ei['good'] & po['effective'], os['high']),
        ctrl.Rule(ci['good'] & pi['high'] & rr['high'], os['high']),
        ctrl.Rule(rr['high'] & cb['affordable'] & po['effective'], os['high']),
        ctrl.Rule(ci['acceptable'] & po['effective'] & pi['high'], os['high']),
        ctrl.Rule(ci['good'] & ei['good'], os['high']),

        # Moderate
        ctrl.Rule(ci['acceptable'] & po['ineffective'], os['medium']),
        ctrl.Rule(ra['acceptable'] & po['ineffective'], os['medium']),
        ctrl.Rule(cb['affordable'] & ci['acceptable'], os['medium']),
        ctrl.Rule(pi['medium'] & sc['acceptable'], os['medium']),
        ctrl.Rule(ei['acceptable'] & cb['affordable'], os['medium']),
        ctrl.Rule(sc['acceptable'] & rr['high'], os['medium']),
        ctrl.Rule(ci['acceptable'] & pi['medium'] & po['ineffective'], os['medium']),
        ctrl.Rule(ra['acceptable'] & rr['high'], os['medium']),
        ctrl.Rule(ci['poor'] & sc['good'], os['medium']),
        ctrl.Rule(ci['acceptable'] & cb['expensive'], os['medium']),

        # Negative
        ctrl.Rule(ci['poor'] | po['ineffective'], os['low']),
        ctrl.Rule(ei['poor'] & ra['poor'], os['low']),
        ctrl.Rule(cb['expensive'] & po['ineffective'], os['low']),
        ctrl.Rule(ci['poor'] & ra['poor'] & cb['expensive'], os['low']),
        ctrl.Rule(rr['low'] | ei['poor'], os['low']),
        ctrl.Rule(pi['low'] & ra['poor'], os['low']),
        ctrl.Rule(ci['poor'] & ei['poor'], os['low']),
        ctrl.Rule(ci['poor'] & cb['expensive'], os['low']),
        ctrl.Rule(po['ineffective'] & rr['low'], os['low']),
        ctrl.Rule(pi['low'] & po['ineffective'], os['low']),
    ]
    return rules