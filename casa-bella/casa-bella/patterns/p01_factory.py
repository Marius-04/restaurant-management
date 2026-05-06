"""1. FACTORY METHOD
Cream produse (mancare/bautura) printr-o fabrica unica.
Locatie integrare: app/services.py -> add_to_cart()
"""
from dataclasses import dataclass

@dataclass
class MenuProduct:
    id: str
    name: str
    price: float
    type: str
    description: str = ""
    image: str = ""

class FoodProduct(MenuProduct):
    def __init__(self, **kw): super().__init__(type="food", **kw)

class DrinkProduct(MenuProduct):
    def __init__(self, **kw): super().__init__(type="drink", **kw)

class ProductFactory:
    @staticmethod
    def create(kind: str, **kw) -> MenuProduct:
        if kind == "food":  return FoodProduct(**kw)
        if kind == "drink": return DrinkProduct(**kw)
        raise ValueError(f"Tip necunoscut: {kind}")
