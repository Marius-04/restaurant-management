"""8. OBSERVER
Bus de evenimente: subscriberii primesc notificari cand se schimba comenzi.
"""
from dataclasses import dataclass

@dataclass
class OrderEvent:
    type: str
    order_id: str
    detail: str = ""

class _Bus:
    def __init__(self): self.subs = []
    def subscribe(self, fn):
        self.subs.append(fn)
        return lambda: self.subs.remove(fn)
    def publish(self, e: OrderEvent):
        for fn in list(self.subs): fn(e)

order_bus = _Bus()
