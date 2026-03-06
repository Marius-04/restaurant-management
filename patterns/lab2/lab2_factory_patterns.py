"""
LABORATORUL 2 - Factory Method & Abstract Factory
Restaurant Management System
"""

from abc import ABC, abstractmethod
from typing import List

# ============================================================================
# FACTORY METHOD - Creare Mâncăruri
# ============================================================================

class Produs(ABC):
    """Interfață pentru produse meniu"""
    @abstractmethod
    def get_pret(self) -> float: pass
    @abstractmethod
    def get_descriere(self) -> str: pass
    @abstractmethod
    def prepare(self) -> str: pass

class Paste(Produs):
    def __init__(self, nume, pret):
        self.nume = nume
        self.pret = pret
    def get_pret(self): return self.pret
    def get_descriere(self): return f"🍝 {self.nume}"
    def prepare(self): return f"Se fierb {self.nume}..."
    def __str__(self): return f"{self.get_descriere()} - {self.pret:.2f} lei"

class Pizza(Produs):
    def __init__(self, nume, pret):
        self.nume = nume
        self.pret = pret
    def get_pret(self): return self.pret
    def get_descriere(self): return f"🍕 {self.nume}"
    def prepare(self): return f"Se coacă {self.nume}..."
    def __str__(self): return f"{self.get_descriere()} - {self.pret:.2f} lei"

class Salata(Produs):
    def __init__(self, nume, pret):
        self.nume = nume
        self.pret = pret
    def get_pret(self): return self.pret
    def get_descriere(self): return f"🥗 {self.nume}"
    def prepare(self): return f"Se prepară {self.nume}..."
    def __str__(self): return f"{self.get_descriere()} - {self.pret:.2f} lei"

class Factory(ABC):
    """Factory abstractă"""
    @abstractmethod
    def create_product(self, nume: str, pret: float) -> Produs: pass

class PasteFactory(Factory):
    def create_product(self, nume, pret):
        return Paste(nume, pret)

class PizzaFactory(Factory):
    def create_product(self, nume, pret):
        return Pizza(nume, pret)

class SalataFactory(Factory):
    def create_product(self, nume, pret):
        return Salata(nume, pret)

# ============================================================================
# ABSTRACT FACTORY - UI Multi-platform
# ============================================================================

class Button(ABC):
    @abstractmethod
    def render(self): pass

class Menu(ABC):
    @abstractmethod
    def render(self): pass

class WindowsButton(Button):
    def render(self): return "🪟 Windows Button"

class WindowsMenu(Menu):
    def render(self): return "🪟 Windows Menu"

class MacButton(Button):
    def render(self): return "🍎 Mac Button"

class MacMenu(Menu):
    def render(self): return "🍎 Mac Menu"

class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: pass
    @abstractmethod
    def create_menu(self) -> Menu: pass

class WindowsUIFactory(UIFactory):
    def create_button(self): return WindowsButton()
    def create_menu(self): return WindowsMenu()

class MacUIFactory(UIFactory):
    def create_button(self): return MacButton()
    def create_menu(self): return MacMenu()

class RestaurantApp:
    def __init__(self, factory: UIFactory):
        self.button = factory.create_button()
        self.menu = factory.create_menu()
    
    def render(self):
        print(f"  {self.button.render()}")
        print(f"  {self.menu.render()}")

# ============================================================================
# DEMONSTRAȚIE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("LAB 2 - FACTORY METHOD & ABSTRACT FACTORY")
    print("="*70)
    
    # Factory Method
    print("\n✅ FACTORY METHOD:\n")
    
    factories = {
        "Paste": PasteFactory(),
        "Pizza": PizzaFactory(),
        "Salata": SalataFactory()
    }
    
    products = []
    for tip, factory in factories.items():
        if tip == "Paste":
            p = factory.create_product("Spaghetti Carbonara", 24.99)
        elif tip == "Pizza":
            p = factory.create_product("Margherita", 20.00)
        else:
            p = factory.create_product("Cezar", 15.99)
        products.append(p)
        print(f"  {p}")
        print(f"  Prep: {p.prepare()}\n")
    
    # Abstract Factory
    print("\n✅ ABSTRACT FACTORY:\n")
    
    print("  Windows App:")
    win_app = RestaurantApp(WindowsUIFactory())
    win_app.render()
    
    print("\n  Mac App:")
    mac_app = RestaurantApp(MacUIFactory())
    mac_app.render()
    
    print("\n" + "="*70)
    print("✅ LAB 2 - COMPLET")
    print("="*70 + "\n")
