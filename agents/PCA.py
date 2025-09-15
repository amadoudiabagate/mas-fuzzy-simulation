""" Runs clinical consultations, issues diagnoses, and creates prescriptions when needed. """

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
        logger = getattr(agent, "logger", None)
        if callable(logger):
            try:
                logger(f"[{agent.unique_id}:{agent.__class__.__name__}] {msg}")
            except Exception:
                pass


class PrescriptionConsultationAgent(Agent):
    """Consultations, diagnosis, and prescription issuing.

    Expected (optional) model attributes:
      - consultation_queue: list of patients
      - post_consultation_queue: list of patients
      - doctors_available: int
      - pending_prescriptions: list of dicts
    """
    def __init__(self, unique_id, model, config: Optional[Dict[str, Any]] = None, logger=None):
        super().__init__(unique_id, model)
        self.config = config or {}
        self.logger = logger
        self.rand = random.Random(self.config.get("seed", 0))

    def step(self):
        m = self.model
        if not _SafeOps.has(m, "consultation_queue"):
            return
        if getattr(m, "doctors_available", 0) <= 0:
            return
        patient = _SafeOps.pop_queue(m.consultation_queue)
        if not patient:
            return
        if not _SafeOps.dec_slot(m, "doctors_available", 1):
            _SafeOps.push_queue(m.consultation_queue, patient)
            return
        _SafeOps.log(self, "Consulting patient")
        service_ticks = 1 + (hash((self.unique_id, getattr(patient, 'pid', id(patient)))) % 3)
        if _SafeOps.has(m, "pending_prescriptions"):
            rx = {
                "patient_id": getattr(patient, "pid", id(patient)),
                "drug": "RX-A" if (service_ticks % 2 == 0) else "RX-B",
                "qty": 1 + (service_ticks % 2),
            }
            m.pending_prescriptions.append(rx)
        _SafeOps.inc_slot(m, "doctors_available", 1)
        if _SafeOps.has(m, "post_consultation_queue"):
            _SafeOps.push_queue(m.post_consultation_queue, patient)
