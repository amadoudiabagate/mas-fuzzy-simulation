""" Coordinates laboratory and imaging requests and returns results. """

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
                logger(f"[{agent.unique_id}:{agent.__class__.__name__}] {msg}")
            except Exception:
                pass


class LaboratoryRadiologyAgent(Agent):
    """Coordinates laboratory and radiology orders and results.

    Expected (optional) model attributes:
      - pending_lab_orders: list of dicts
      - lab_results: list of dicts
    """
    def __init__(self, unique_id, model, config: Optional[Dict[str, Any]] = None, logger=None):
        super().__init__(unique_id, model)
        self.config = config or {}
        self.logger = logger

    def step(self):
        m = self.model
        if not _SafeOps.has(m, "pending_lab_orders"):
            return
        orders = list(getattr(m, "pending_lab_orders", []))
        m.pending_lab_orders = []
        if not _SafeOps.has(m, "lab_results"):
            m.lab_results = []
        for order in orders:
            res = {"order_id": order.get("id"), "status":"done", "value":"N/A"}
            m.lab_results.append(res)
            _SafeOps.log(self, f"Processed lab order {order.get('id')}")
