""" Offers lightweight medical intelligence signals for decision support. """

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
        """Log message if agent has a logger callable."""
        logger = getattr(agent, "logger", None)
        if callable(logger):
            try:
                logger(f"[{agent.unique_id}:{agent.__class__.__name__}] {msg}" )
            except Exception:
                pass


class MedicalIntelligenceAgent(Agent):
    """Lightweight clinical decision support based on simple signals.

    Expected (optional) model attributes:
      - observed_patients: list of patients
      - cdss_outputs: list of dicts
    """
    def __init__(self, unique_id, model, config: Optional[Dict[str, Any]] = None, logger=None):
        super().__init__(unique_id, model)
        self.config = config or {}
        self.logger = logger

    def step(self):
        m = self.model
        if not _SafeOps.has(m, "cdss_outputs"):
            m.cdss_outputs = []
        pool = getattr(m, "observed_patients", [])
        for p in pool[:1]:
            hr = getattr(p, "heart_rate", 70)
            risk = "high" if hr > 110 else "medium" if hr > 90 else "low"
            m.cdss_outputs.append({"pid": getattr(p, "pid", id(p)), "risk": risk})
            _SafeOps.log(self, f"Patient {getattr(p, 'pid', id(p))} risk assessed: {risk}")
