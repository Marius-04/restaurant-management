"""
LABORATORUL 4 - Adapter, Composite & Façade
Restaurant Management System
"""

from abc import ABC, abstractmethod
from typing import List

# ============================================================================
# ADAPTER - Integrare Payment Gateways
# ============================================================================

class OldPaymentSystem:
    def ship(self, destination, amount):
        return f"Plată procesată: {amount}lei la {destination}"

class PaymentInterface(ABC):
    @abstractmethod
    def pay(self, amount): pass

class PaymentAdapter(PaymentInterface):
    def __init__(self, old_system):
        self.old_system = old_system
    
    def pay(self, amount):
        return self.old_system.ship("Restaurant", amount)

class ModernPaymentSystem(PaymentInterface):
    def pay(self, amount):
        return f"✅ Plată modernă: {amount:.2f} lei"

# ============================================================================
# COMPOSITE - Meniu Ierarhic
# ============================================================================

class MenuItem(ABC):
    @abstractmethod
    def render(self, indent=0): pass

class Product(MenuItem):
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def render(self, indent=0):
        return " " * indent + f"🍽️ {self.name} - {self.price:.2f} lei"

class Category(MenuItem):
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon
        self.items: List[MenuItem] = []
    
    def add_item(self, item):
        self.items.append(item)
    
    def render(self, indent=0):
        result = " " * indent + f"{self.icon} {self.name}\n"
        for item in self.items:
            result += item.render(indent + 2) + "\n"
        return result

class Menu(MenuItem):
    def __init__(self, name):
        self.name = name
        self.categories: List[Category] = []
    
    def add_category(self, cat):
        self.categories.append(cat)
    
    def render(self, indent=0):
        result = f"\n{'='*50}\n{self.name}\n{'='*50}\n"
        for cat in self.categories:
            result += cat.render() + "\n"
        return result

# ============================================================================
# FAÇADE - Simplificare Sistem Complex
# ============================================================================

class OrderSystem:
    def create_order(self, client): return f"✅ Comandă creată pentru {client}"

class PaymentService:
    def process(self, amount): return f"✅ Plată: {amount:.2f} lei"

class DeliveryService:
    def schedule(self, address): return f"✅ Livrare la {address}"

class NotificationService:
    def notify(self, msg): return f"📧 {msg}"

class RestaurantFacade:
    def __init__(self):
        self.orders = OrderSystem()
        self.payment = PaymentService()
        self.delivery = DeliveryService()
        self.notify = NotificationService()
    
    def complete_order(self, client, amount, address):
        print(f"\n🎯 COMANDĂ COMPLETĂ:\n")
        print(f"  {self.orders.create_order(client)}")
        print(f"  {self.payment.process(amount)}")
        print(f"  {self.delivery.schedule(address)}")
        print(f"  {self.notify.notify(f'Comandă confirmată pentru {client}')}\n")

# ============================================================================
# DEMONSTRAȚIE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("LAB 4 - ADAPTER, COMPOSITE & FAÇADE")
    print("="*70)
    
    # Adapter
    print("\n✅ ADAPTER:\n")
    
    old_sys = OldPaymentSystem()
    adapter = PaymentAdapter(old_sys)
    
    print(f"  Old system: {adapter.pay(100)}")
    
    modern = ModernPaymentSystem()
    print(f"  Modern system: {modern.pay(100)}\n")
    
    # Composite
    print("✅ COMPOSITE:\n")
    
    meniu = Menu("🍽️ MENIU RESTAURANT")
    
    paste = Category("🍝 Paste", "🍝")
    paste.add_item(Product("Spaghetti", 24.99))
    paste.add_item(Product("Fettuccine", 22.50))
    meniu.add_category(paste)
    
    pizza = Category("🍕 Pizza", "🍕")
    pizza.add_item(Product("Margherita", 20.00))
    pizza.add_item(Product("Pepperoni", 24.50))
    meniu.add_category(pizza)
    
    print(meniu.render())
    
    # Façade
    print("✅ FAÇADE:\n")
    
    facade = RestaurantFacade()
    facade.complete_order("Ion Popescu", 75.50, "Strada Principală, 10")
    
    print("="*70)
    print("✅ LAB 4 - COMPLET")
    print("="*70 + "\n")
