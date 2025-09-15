""" Routes patients across services while respecting simple capacity hints. """

# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Any, Dict, Optional
from mesa import Agent
import random

class _SafeOps:
    @staticmethod
    def pop_queue(q: Any):
        try:
            return q.pop(0) if q else None
        except Exception:
            return None

    @staticmethod
    def push_queue(q: Any, item: Any):
        try:
            q.append(item)
        except Exception:
            pass

    @staticmethod
    def dec_slot(model: Any, name: str, amount: int = 1) -> bool:
        v = max(0, int(getattr(model, name, 0)))
        if v >= amount:
            setattr(model, name, v - amount)
            return True
        return False

    @staticmethod
    def inc_slot(model: Any, name: str, amount: int = 1):
        v = max(0, int(getattr(model, name, 0)))
        setattr(model, name, v + amount)

    @staticmethod
    def has(model: Any, name: str) -> bool:
        return hasattr(model, name)

    @staticmethod
    def log(agent: Agent, msg: str):
        """Log message safely if agent has a logger."""
        logger = getattr(agent, "logger", None)
        if callable(logger):
            try:
                logger(f"[{agent.unique_id}:{agent.__class__.__name__}] {msg}")
            except Exception:
                pass


class ServiceCoordinationAgent(Agent):
    """Routes patients between services and arbitrates resource use.

    Expected (optional) model attributes:
      - triage_queue: list of patients
      - consultation_queue: list of patients
      - inpatient_queue: list of patients
      - beds_available: int
    """
    def __init__(self, unique_id, model, config: Optional[Dict[str, Any]] = None, logger=None):
        super().__init__(unique_id, model)
        self.config = config or {}
        self.logger = logger

    def step(self):
        m = self.model
        triage_q = getattr(m, "triage_queue", None)
        if not triage_q:
            return
        patient = _SafeOps.pop_queue(triage_q)
        if not patient:
            return
        acuity = getattr(patient, "acuity", "consultation")
        if acuity == "emergency" and getattr(m, "beds_available", 0) > 0:
            _SafeOps.dec_slot(m, "beds_available", 1)
            _SafeOps.push_queue(getattr(m, "inpatient_queue", []), patient)
        else:
            _SafeOps.push_queue(getattr(m, "consultation_queue", []), patient)
