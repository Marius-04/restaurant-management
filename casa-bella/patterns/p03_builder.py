"""
03. BUILDER  (Creational)
--------------------------------------------------------------
Construiește o comandă pas cu pas (items, plată, adresă, note)
cu API fluent. Permite obiecte complexe fără constructori uriași.

Folosit în: app/services.py → la finalizarea coșului.
"""
from dataclasses import dataclass, field
from typing import List, Tuple
from .p01_factory_method import MenuProduct


@dataclass
class Order:
    items: List[Tuple[MenuProduct, int]] = field(default_factory=list)
    payment_method: str = "cash"
    delivery_address: str = ""
    notes: str = ""
    total: float = 0.0


class OrderBuilder:
    def __init__(self):
        self._order = Order()

    def add_item(self, product: MenuProduct, qty: int = 1):
        self._order.items.append((product, qty))
        return self

    def with_payment(self, method: str):
        self._order.payment_method = method
        return self

    def with_address(self, address: str):
        self._order.delivery_address = address
        return self

    def with_notes(self, notes: str):
        self._order.notes = notes
        return self

    def build(self) -> Order:
        self._order.total = sum(p.price * q for p, q in self._order.items)
        return self._order
