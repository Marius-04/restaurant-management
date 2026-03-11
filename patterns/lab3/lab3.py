"""
LABORATORUL 3 - Builder, Prototype & Singleton
Restaurant Management System
"""

from abc import ABC, abstractmethod
from copy import deepcopy
import threading

# ============================================================================
# BUILDER - Comenzi Personalizate
# ============================================================================

class Comanda:
    def __init__(self):
        self.tip = ""
        self.ingrediente = []
        self.pret = 0.0
        self.urgent = False

class ComandaBuilder(ABC):
    @abstractmethod
    def set_tip(self, tip): pass
    @abstractmethod
    def add_ingredient(self, ing): pass
    @abstractmethod
    def set_pret(self, pret): pass
    @abstractmethod
    def set_urgent(self, urgent): pass
    @abstractmethod
    def build(self): pass

class BurgerBuilder(ComandaBuilder):
    def __init__(self):
        self.comanda = Comanda()
    
    def set_tip(self, tip):
        self.comanda.tip = f"🍔 {tip}"
        return self
    
    def add_ingredient(self, ing):
        self.comanda.ingrediente.append(ing)
        return self
    
    def set_pret(self, pret):
        self.comanda.pret = pret
        return self
    
    def set_urgent(self, urgent):
        self.comanda.urgent = urgent
        return self
    
    def build(self):
        return self.comanda

class PizzaBuilder(ComandaBuilder):
    def __init__(self):
        self.comanda = Comanda()
    
    def set_tip(self, tip):
        self.comanda.tip = f"🍕 {tip}"
        return self
    
    def add_ingredient(self, ing):
        self.comanda.ingrediente.append(ing)
        return self
    
    def set_pret(self, pret):
        self.comanda.pret = pret
        return self
    
    def set_urgent(self, urgent):
        self.comanda.urgent = urgent
        return self
    
    def build(self):
        return self.comanda

# ============================================================================
# PROTOTYPE - Clonare Documente
# ============================================================================

class Cloneable(ABC):
    @abstractmethod
    def clone(self): pass

class Document(Cloneable):
    def __init__(self, titlu, continut, autori):
        self.titlu = titlu
        self.continut = continut
        self.autori = autori
    
    def clone(self):
        return Document(self.titlu, self.continut, self.autori[:])
    
    def deep_clone(self):
        return Document(self.titlu, self.continut, deepcopy(self.autori))

class DocumentRegistry:
    def __init__(self):
        self.prototypes = {}
    
    def register(self, name, doc):
        self.prototypes[name] = doc
    
    def clone(self, name):
        return self.prototypes[name].clone()

# ============================================================================
# SINGLETON - Configurare & Bază de date
# ============================================================================

class RestaurantConfig:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance
    
    def _init(self):
        self.name = "Restaurant Delicii"
        self.address = "Strada Principală, 123"
        self.phone = "0720-123-456"
        self.tax = 0.19

class OrderDatabase:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance
    
    def _init(self):
        self.orders = []
        self.total_revenue = 0.0
    
    def add_order(self, order_id, total):
        self.orders.append({"id": order_id, "total": total})
        self.total_revenue += total

# ============================================================================
# DEMONSTRAȚIE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("LAB 3 - BUILDER, PROTOTYPE & SINGLETON")
    print("="*70)
    
    # Builder
    print("\n✅ BUILDER:\n")
    
    burger = (BurgerBuilder()
              .set_tip("Clasic")
              .set_pret(18.99)
              .add_ingredient("Bacon")
              .add_ingredient("Cheddar")
              .set_urgent(False)
              .build())
    
    print(f"  Burger: {burger.tip}")
    print(f"  Ingrediente: {burger.ingrediente}")
    print(f"  Preț: {burger.pret:.2f} lei\n")
    
    # Prototype
    print("✅ PROTOTYPE:\n")
    
    doc = Document("Raport Anual", "Conținut...", ["Author1", "Author2"])
    registry = DocumentRegistry()
    registry.register("raport", doc)
    
    cloned = registry.clone("raport")
    print(f"  Original: {doc.titlu}, Autori: {doc.autori}")
    print(f"  Clonat: {cloned.titlu}, Autori: {cloned.autori}\n")
    
    # Singleton
    print("✅ SINGLETON:\n")
    
    config1 = RestaurantConfig()
    config2 = RestaurantConfig()
    
    print(f"  config1 is config2: {config1 is config2}")
    print(f"  Restaurant: {config1.name}\n")
    
    db1 = OrderDatabase()
    db1.add_order("CMD-001", 75.50)
    db2 = OrderDatabase()
    
    print(f"  db1 is db2: {db1 is db2}")
    print(f"  Total comenzi: {len(db2.orders)}\n")
    
    print("="*70)
    print("✅ LAB 3 - COMPLET")
    print("="*70 + "\n")
