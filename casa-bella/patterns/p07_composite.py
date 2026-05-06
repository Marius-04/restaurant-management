"""
07. COMPOSITE  (Structural)
--------------------------------------------------------------
Tratăm uniform frunzele (produse) și compușii (categorii) prin
interfața comună `MenuComponent`. Util pentru meniu ierarhic.

Folosit în: pagina /patterns → arborele meniului.
"""
from abc import ABC, abstractmethod
from typing import List


class MenuComponent(ABC):
    name: str
    @abstractmethod
    def get_price(self) -> float: ...
    @abstractmethod
    def print(self, indent: int = 0) -> str: ...


class LeafProduct(MenuComponent):
    def __init__(self, name: str, price: float):
        self.name = name
        self._price = price

    def get_price(self): return self._price
    def print(self, indent=0):
        return f"{' ' * indent}• {self.name} — {self._price:.2f} MDL"


class MenuCategory(MenuComponent):
    def __init__(self, name: str):
        self.name = name
        self._children: List[MenuComponent] = []

    def add(self, c: MenuComponent):
        self._children.append(c)
        return self

    def get_price(self):
        return sum(c.get_price() for c in self._children)

    def print(self, indent=0):
        head = f"{' ' * indent}▸ {self.name}"
        return "\n".join([head, *[c.print(indent + 2) for c in self._children]])
