import numpy as np
import skfuzzy as fuzz

def universe(step='base'):
    """Return the universe of discourse (0..10).
    step='base' -> np.arange(0, 11, 1) to match the original code.
    step='fine' -> np.linspace(0, 10, 101) for smoother plots.
    """
    if step == 'fine':
        return np.linspace(0, 10, 101)
    return np.arange(0, 11, 1)

def comm_info_terms(U):
    return {
        'poor':       fuzz.trimf(U, [0, 0, 5]),
        'acceptable': fuzz.trimf(U, [2, 5, 8]),
        'good':       fuzz.trimf(U, [5, 10, 10]),
    }

def reception_access_terms(U):
    return {
        'poor':       fuzz.trapmf(U, [0, 0, 2, 4]),
        'acceptable': fuzz.trapmf(U, [2, 4, 6, 8]),
        'good':       fuzz.trapmf(U, [6, 8, 10, 10]),
    }

def staff_comp_terms(U):
    return {
        'poor':       fuzz.gaussmf(U, 2, 1.5),
        'acceptable': fuzz.gaussmf(U, 5, 1.5),
        'good':       fuzz.gaussmf(U, 8, 1.5),
    }

def env_infra_terms(U):
    return {
        'poor':       fuzz.trapmf(U, [0, 0, 2, 4]),
        'acceptable': fuzz.trapmf(U, [3, 5, 7, 9]),
        'good':       fuzz.trapmf(U, [7, 9, 10, 10]),
    }

def perceived_outcome_terms(U):
    # effective vs ineffective via sigmoids
    return {
        'ineffective': fuzz.sigmf(U, -1.5, 5),
        'effective':   fuzz.sigmf(U,  1.5, 5),
    }

def cost_billing_terms(U):
    # affordable is inverse of expensive sigmoid
    return {
        'affordable':  1 - fuzz.sigmf(U, 1.5, 5),
        'expensive':   fuzz.sigmf(U, 1.5, 5),
    }

def patient_involvement_terms(U):
    return {
        'low':    fuzz.trimf(U, [0, 0, 5]),
        'medium': fuzz.trimf(U, [2, 5, 8]),
        'high':   fuzz.trimf(U, [5, 10, 10]),
    }

def return_reco_terms(U):
    return {
        'low':  fuzz.trapmf(U, [0, 0, 3, 5]),
        'high': fuzz.trapmf(U, [5, 7, 10, 10]),
    }

def overall_satisfaction_terms(U):
    return {
        'low':    fuzz.trimf(U, [0, 0, 5]),
        'medium': fuzz.trimf(U, [3, 5, 7]),
        'high':   fuzz.trimf(U, [5, 10, 10]),
    }