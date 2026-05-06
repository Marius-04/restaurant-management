"""2. BUILDER
Construim o comanda complexa pas cu pas (items, plata, adresa, note).
Locatie integrare: app/services.py -> Checkout
"""
from dataclasses import dataclass, field
from typing import List
from .p01_factory import MenuProduct

@dataclass
class CartLine:
    product: MenuProduct
    quantity: int

@dataclass
class Order:
    items: List[CartLine] = field(default_factory=list)
    payment_method: str = "cash"
    delivery_address: str = ""
    notes: str = ""
    status: str = "pending"
    @property
    def total(self) -> float:
        return round(sum(l.product.price * l.quantity for l in self.items), 2)

class OrderBuilder:
    def __init__(self): self._o = Order()
    def add(self, p: MenuProduct, qty: int = 1):
        for l in self._o.items:
            if l.product.id == p.id:
                l.quantity += qty; return self
        self._o.items.append(CartLine(p, qty)); return self
    def payment(self, m: str): self._o.payment_method = m; return self
    def address(self, a: str): self._o.delivery_address = a; return self
    def note(self, n: str): self._o.notes = n; return self
    def build(self) -> Order: return self._o
