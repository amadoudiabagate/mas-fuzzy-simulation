""" Manages medications and consumable products, including simple stock checks. """

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


class MedicationProductManagementAgent(Agent):
    """Dispensing medications and maintaining product inventory.

    Expected (optional) model attributes:
      - pending_prescriptions: list of dicts
      - med_inventory: dict {drug: stock}
      - events: list (optional) for shortage logs
    """
    def __init__(self, unique_id, model, config: Optional[Dict[str, Any]] = None, logger=None):
        super().__init__(unique_id, model)
        self.config = config or {}
        self.logger = logger

    def step(self):
        m = self.model
        if not (_SafeOps.has(m, "pending_prescriptions") and _SafeOps.has(m, "med_inventory")):
            return
        todo = list(getattr(m, "pending_prescriptions", []))
        m.pending_prescriptions = []
        for rx in todo:
            drug = rx.get("drug", "UNKNOWN")
            qty = int(rx.get("qty", 1))
            inv = m.med_inventory.get(drug, 0)
            if inv >= qty:
                m.med_inventory[drug] = inv - qty
                _SafeOps.log(self, f"Dispensed {qty}x {drug}")
            else:
                if _SafeOps.has(m, "events"):
                    m.events.append({"type":"shortage","drug":drug,"need":qty,"have":inv})
                    _SafeOps.log(self, f"Shortage for {drug}: need {qty}, have {inv}")
