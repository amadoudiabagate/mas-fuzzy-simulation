import os
from skfuzzy import control as ctrl
from .core.membership_functions import (
    universe, comm_info_terms, reception_access_terms, staff_comp_terms,
    env_infra_terms, perceived_outcome_terms, cost_billing_terms,
    patient_involvement_terms, return_reco_terms, overall_satisfaction_terms,
)
from .core.rule_base import build_rules

OUTPUT_DIR = "output/figures/fuzzy_logic"
os.makedirs(OUTPUT_DIR, exist_ok=True)

VAR_LABELS = {
    'ci': 'Communication and Information',
    'ra': 'Reception and Accessibility',
    'sc': 'Staff competence',
    'ei': 'Environment and infrastructure',
    'po': 'Perceived Treatment Outcome',
    'cb': 'Cost and Billing',
    'pi': 'patient Involvement',
    'rr': 'Intention to Return and Recommend',
    'os': 'Overall satisfaction',
}

def _assign_terms(var, terms_dict):
    for name, mf in terms_dict.items():
        var[name] = mf

def build_system(step='base'):
    U = universe(step=step)

    ci = ctrl.Antecedent(U, VAR_LABELS['ci'])
    ra = ctrl.Antecedent(U, VAR_LABELS['ra'])
    sc = ctrl.Antecedent(U, VAR_LABELS['sc'])
    ei = ctrl.Antecedent(U, VAR_LABELS['ei'])
    po = ctrl.Antecedent(U, VAR_LABELS['po'])
    cb = ctrl.Antecedent(U, VAR_LABELS['cb'])
    pi = ctrl.Antecedent(U, VAR_LABELS['pi'])
    rr = ctrl.Antecedent(U, VAR_LABELS['rr'])
    os_ = ctrl.Consequent(U, VAR_LABELS['os'])

    _assign_terms(ci, comm_info_terms(U))
    _assign_terms(ra, reception_access_terms(U))
    _assign_terms(sc, staff_comp_terms(U))
    _assign_terms(ei, env_infra_terms(U))
    _assign_terms(po, perceived_outcome_terms(U))
    _assign_terms(cb, cost_billing_terms(U))
    _assign_terms(pi, patient_involvement_terms(U))
    _assign_terms(rr, return_reco_terms(U))
    _assign_terms(os_, overall_satisfaction_terms(U))

    vars_map = {
        VAR_LABELS['ci']: ci,
        VAR_LABELS['ra']: ra,
        VAR_LABELS['sc']: sc,
        VAR_LABELS['ei']: ei,
        VAR_LABELS['po']: po,
        VAR_LABELS['cb']: cb,
        VAR_LABELS['pi']: pi,
        VAR_LABELS['rr']: rr,
        VAR_LABELS['os']: os_,
    }

    rules = build_rules(vars_map)
    system = ctrl.ControlSystem(rules)
    return system, vars_map, U

def evaluate(inputs: dict, step='base'):
    system, vars_map, U = build_system(step=step)
    sim = ctrl.ControlSystemSimulation(system)
    # Map human labels to control variables
    for label, value in inputs.items():
        sim.input[label] = value
    sim.compute()
    return sim.output