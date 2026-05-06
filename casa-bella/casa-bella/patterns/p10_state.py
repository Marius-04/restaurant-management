"""10. STATE
Validam tranzitiile valide ale unei comenzi (FSM).
"""
TRANSITIONS = {
    "pending":    ["confirmed", "cancelled"],
    "confirmed":  ["preparing", "cancelled"],
    "preparing":  ["ready", "cancelled"],
    "ready":      ["delivering"],
    "delivering": ["delivered"],
    "delivered":  [],
    "cancelled":  [],
}

class OrderStateMachine:
    def __init__(self, current: str): self.current = current
    def can(self, to: str) -> bool: return to in TRANSITIONS.get(self.current, [])
    def next_options(self): return TRANSITIONS.get(self.current, [])
