"""
12. STATE  (Behavioral)
--------------------------------------------------------------
Comanda își schimbă comportamentul în funcție de starea curentă.
Tranzițiile valide sunt definite explicit.

Folosit în: Admin → butoanele "→ next".
"""
ORDER_TRANSITIONS = {
    "pending":    ["confirmed", "cancelled"],
    "confirmed":  ["preparing", "cancelled"],
    "preparing":  ["ready", "cancelled"],
    "ready":      ["delivering", "delivered"],
    "delivering": ["delivered"],
    "delivered":  [],
    "cancelled":  [],
}


class OrderStateMachine:
    def __init__(self, current: str = "pending"):
        self._current = current

    @property
    def state(self): return self._current

    def can_transition_to(self, nxt: str) -> bool:
        return nxt in ORDER_TRANSITIONS.get(self._current, [])

    def transition_to(self, nxt: str):
        if not self.can_transition_to(nxt):
            raise ValueError(f"Tranziție invalidă: {self._current} → {nxt}")
        self._current = nxt

    def next_options(self):
        return list(ORDER_TRANSITIONS.get(self._current, []))
