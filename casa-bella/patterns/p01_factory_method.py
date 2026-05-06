"""
01. FACTORY METHOD  (Creational)
--------------------------------------------------------------
Creează produse de meniu (food / drink) fără ca apelantul
să cunoască clasele concrete.

Folosit în: app/services.py → la adăugarea în coș și la build-ul meniului.
"""
from dataclasses import dataclass


@dataclass
class MenuProduct:
    id: int
    name: str
    price: float
    type: str           # "food" | "drink"
    description: str = ""
    image: str = ""

    def label(self) -> str:
        return f"[{self.type.upper()}] {self.name}"


class FoodProduct(MenuProduct):
    def __init__(self, **kw):
        super().__init__(type="food", **kw)


class DrinkProduct(MenuProduct):
    def __init__(self, **kw):
        super().__init__(type="drink", **kw)


class ProductFactory:
    """Factory Method — alege clasa concretă în funcție de tip."""

    @staticmethod
    def create(kind: str, **data) -> MenuProduct:
        if kind == "food":
            return FoodProduct(**data)
        if kind == "drink":
            return DrinkProduct(**data)
        raise ValueError(f"Tip de produs necunoscut: {kind}")
