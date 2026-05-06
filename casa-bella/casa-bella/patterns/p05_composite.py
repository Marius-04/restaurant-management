"""5. COMPOSITE
Meniul ca arbore: Categorii (compozite) + Produse (frunze) tratate uniform.
"""
from abc import ABC, abstractmethod
from typing import List

class MenuComponent(ABC):
    @abstractmethod
    def display(self, indent=0) -> str: ...
    @abstractmethod
    def count(self) -> int: ...

class MenuLeaf(MenuComponent):
    def __init__(self, product): self.product = product
    def display(self, indent=0): return " "*indent + f"- {self.product.name} ({self.product.price} Lei)"
    def count(self): return 1

class MenuCategory(MenuComponent):
    def __init__(self, name: str):
        self.name = name; self.children: List[MenuComponent] = []
    def add(self, c: MenuComponent): self.children.append(c); return self
    def display(self, indent=0):
        out = [" "*indent + f"# {self.name}"]
        for c in self.children: out.append(c.display(indent+2))
        return "\n".join(out)
    def count(self): return sum(c.count() for c in self.children)
