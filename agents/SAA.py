""" Performs identity verification and security checks before admission. """

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


class SecurityAccessAgent(Agent):
    """Performs identity verification and policy checks prior to admission.

    Expected (optional) model attributes:
      - security_queue: list of patients
      - admission_queue: list of patients
      - security_checks_done: int (optional counter)
    """
    def __init__(self, unique_id, model, config: Optional[Dict[str, Any]] = None, logger=None):
        super().__init__(unique_id, model)
        self.config = config or {}
        self.logger = logger

    def step(self):
        m = self.model
        q = getattr(m, "security_queue", None)
        if not q:
            return
        patient = _SafeOps.pop_queue(q)
        if not patient:
            return
        _SafeOps.push_queue(getattr(m, "admission_queue", []), patient)
        if _SafeOps.has(m, "security_checks_done"):
            try:
                m.security_checks_done += 1
            except Exception:
                pass
