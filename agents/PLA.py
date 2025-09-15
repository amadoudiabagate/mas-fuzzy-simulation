""" Oversees high-level planning and resolves basic conflicts. """

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


class PlanningAgent(Agent):
    """Coarse-grained orchestration and conflict resolution.

    Expected (optional) model attributes:
      - planning_log: list of dicts
      - consultation_queue: list
      - rooms_available: int
    """
    def __init__(self, unique_id, model, config: Optional[Dict[str, Any]] = None, logger=None):
        super().__init__(unique_id, model)
        self.config = config or {}
        self.logger = logger

    def step(self):
        m = self.model
        if not _SafeOps.has(m, "planning_log"):
            m.planning_log = []
        cq_len = len(getattr(m, "consultation_queue", []))
        rooms = getattr(m, "rooms_available", 0)
        decision = None
        if cq_len > 10 and rooms > 0:
            decision = {"action": "reprioritize", "from": "room", "to": "doctor"}
        if decision:
            m.planning_log.append(decision)
