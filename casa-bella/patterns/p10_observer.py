"""
10. OBSERVER  (Behavioral)
--------------------------------------------------------------
`order_bus` notifică toți subscriberii la evenimente de comandă.

Folosit în: app/services.py → emit la creare/schimbare status.
"""
from dataclasses import dataclass, field
from typing import Callable, List, Optional


@dataclass
class OrderEvent:
    type: str                    # "created" | "status_changed"
    order_id: str
    payload: dict = field(default_factory=dict)


class _OrderEventBus:
    def __init__(self):
        self._subs: List[Callable[[OrderEvent], None]] = []
        self.history: List[OrderEvent] = []

    def subscribe(self, fn):
        self._subs.append(fn)
        return lambda: self._subs.remove(fn)

    def publish(self, e: OrderEvent):
        self.history.append(e)
        for fn in list(self._subs):
            fn(e)


order_bus = _OrderEventBus()
