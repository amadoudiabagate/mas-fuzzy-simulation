""" Computes the fuzzy-based satisfaction score for each completed patient. """

# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Any, Dict, Optional
from mesa import Agent
from skfuzzy import control as ctrl

# Use the shared fuzzy system defined in the project
from fuzzy_logic.fuzzy_system import build_system, VAR_LABELS

class PatientSatisfactionEvaluationAgent(Agent):
    """Evaluates patient satisfaction using the fuzzy system defined in `fuzzy_logic/`.

    Expected model attributes (optional, flexible):
      - psea_inputs: list of dicts with keys mapped to the fuzzy inputs
           Keys can be exactly the VAR_LABELS values (e.g. 'Communication and Information')
           or short aliases: {'ci','ra','sc','ei','po','cb','pi','rr'}.
           Values can be in [0,10] or [0,1] (auto-rescaled to [0,10]).
           Optional 'patient_id' is propagated to outputs.
      - psea_outputs: list where results are appended as dicts
    """
    def __init__(self, unique_id, model, config: Optional[Dict[str, Any]] = None, logger=None):
        super().__init__(unique_id, model)
        self.config = dict(output_scale=10, grid='base')
        if config:
            self.config.update(config)
        self.logger = logger

        # Build fuzzy system once; reuse the simulator
        self._system, self._vars_map, self._U = build_system(step=self.config.get('grid', 'base'))
        self._sim = ctrl.ControlSystemSimulation(self._system)

        # Input key normalization map (aliases -> canonical VAR_LABELS)
        self._keymap = {
            'ci': VAR_LABELS['ci'],
            'ra': VAR_LABELS['ra'],
            'sc': VAR_LABELS['sc'],
            'ei': VAR_LABELS['ei'],
            'po': VAR_LABELS['po'],
            'cb': VAR_LABELS['cb'],
            'pi': VAR_LABELS['pi'],
            'rr': VAR_LABELS['rr'],
        }

    def _log(self, msg: str):
        log = getattr(self, "logger", None)
        if callable(log):
            try:
                log(f"[{self.unique_id}:PSEA] {msg}")
            except Exception:
                pass

    def _normalize_inputs(self, inp: Dict[str, Any]) -> Dict[str, float]:
        """Return a dict with canonical keys (VAR_LABELS values) and values on [0,10]."""
        out = {}
        for k, v in list(inp.items()):
            if k == 'patient_id':
                continue
            # Map alias -> canonical label if needed
            key = self._keymap.get(k, k)
            try:
                val = float(v)
            except Exception:
                continue
            # Auto-rescale 0–1 to 0–10
            if 0.0 <= val <= 1.0 and self.config.get('assume_unit_scale', True):
                val *= 10.0
            out[key] = max(0.0, min(10.0, val))
        return out

    def _ensure_outputs(self):
        if not hasattr(self.model, "psea_outputs"):
            setattr(self.model, "psea_outputs", [])

    def step(self):
        # Consume at most one input per step (conservative)
        inputs_queue = getattr(self.model, "psea_inputs", [])
        if not inputs_queue:
            return
        payload = inputs_queue.pop(0)

        patient_id = payload.get("patient_id", None)
        inputs_0_10 = self._normalize_inputs(payload)

        # Feed the fuzzy simulator
        for key, val in inputs_0_10.items():
            self._sim.input[key] = val
        self._sim.compute()

        score_0_10 = self._sim.output[VAR_LABELS['os']]
        # Scale if requested
        if int(self.config.get('output_scale', 10)) == 1:
            score = score_0_10 / 10.0
        else:
            score = score_0_10

        self._ensure_outputs()
        self.model.psea_outputs.append({
            "patient_id": patient_id,
            "score": score,
            "scale": int(self.config.get('output_scale', 10))
        })