from abc import ABC, abstractmethod
from typing import List, Optional


# =====================
# INTERFEȚE (ISP)
# =====================
class IMenuItem(ABC):
    @abstractmethod
    def get_price(self) -> float:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def prepare(self) -> str:
        pass


class IPayment(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


# =====================
# CLASE ABSTRACTE
# =====================
class MenuItem(IMenuItem):
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price
        self._available = True

    def get_price(self) -> float:
        return self._price

    def get_name(self) -> str:
        return self._name

    @abstractmethod
    def get_description(self) -> str:
        pass


# =====================
# MOȘTENIRE (LSP)
# =====================
class Pizza(MenuItem):
    def __init__(self, name: str, price: float, toppings: List[str]):
        super().__init__(name, price)
        self.toppings = toppings

    def get_description(self) -> str:
        return f"Pizza {self._name} cu {', '.join(self.toppings)}"

    def prepare(self) -> str:
        return f"Coac pizza {self._name}"


class Pasta(MenuItem):
    def __init__(self, name: str, price: float, pasta_type: str):
        super().__init__(name, price)
        self.pasta_type = pasta_type

    def get_description(self) -> str:
        return f"Paste {self._name} ({self.pasta_type})"

    def prepare(self) -> str:
        return f"Fierb paste {self.pasta_type}"


# =====================
# PLĂȚI (OCP)
# =====================
class CashPayment(IPayment):
    def __init__(self, cash_given: float = 0):
        self.cash_given = cash_given

    def pay(self, amount: float) -> str:
        if self.cash_given >= amount:
            return f"Plătit {amount} MDL cash. Rest: {self.cash_given - amount} MDL"
        return f"Sumă insuficientă. Mai trebuie {amount - self.cash_given} MDL"


class CardPayment(IPayment):
    def __init__(self, card_number: str):
        self.card_number = card_number[-4:]

    def pay(self, amount: float) -> str:
        return f"Plătit {amount} MDL cu cardul ***{self.card_number}"


class MobilePayment(IPayment):  # OCP - putem adăuga metode noi
    def __init__(self, phone: str):
        self.phone = phone

    def pay(self, amount: float) -> str:
        return f"Plătit {amount} MDL cu mobile pay ({self.phone})"


# =====================
# CLIENT
# =====================
class Client:
    def __init__(self, name: str, phone: str):
        self.name = name
        self.phone = phone
        self.loyalty_points = 0


# =====================
# COMANDA (DIP)
# =====================
class Order:
    def __init__(self, client: Optional[Client] = None):
        self.client = client
        self._items: List[MenuItem] = []
        self._status = "pending"

    def add_item(self, item: MenuItem):  # DIP - depinde de abstractizare
        if item._available:
            self._items.append(item)

    def calculate_total(self) -> float:
        return sum(item.get_price() for item in self._items)

    def process_payment(self, payment_method: IPayment) -> str:  # DIP
        total = self.calculate_total()
        result = payment_method.pay(total)
        self._status = "paid"
        if self.client:
            self.client.loyalty_points += int(total // 10)
        return result


# =====================
# MENIU
# =====================
class Menu:
    def __init__(self):
        self._items: List[MenuItem] = []

    def add_item(self, item: MenuItem):
        self._items.append(item)

    def get_items(self) -> List[MenuItem]:
        return self._items.copy()

    def find_by_category(self, category: str) -> List[MenuItem]:
        return [item for item in self._items if item.__class__.__name__ == category]


# =====================
# RESTAURANT (clasa principală)
# =====================
class Restaurant:
    def __init__(self, name: str):
        self.name = name
        self.menu = Menu()
        self.orders: List[Order] = []
        self.clients: List[Client] = []
        self.revenue = 0.0

    def add_to_menu(self, item: MenuItem):
        self.menu.add_item(item)

    def register_client(self, client: Client):
        self.clients.append(client)

    def create_order(self, client: Optional[Client] = None) -> Order:
        order = Order(client)
        self.orders.append(order)
        return order

    def process_order(self, order: Order, payment: IPayment):
        result = order.process_payment(payment)
        self.revenue += order.calculate_total()
        return result

    def display_menu(self):
        print(f"\n=== {self.name} MENU ===")
        for item in self.menu.get_items():
            print(f"  • {item.get_description()}")


# =====================
# DEMONSTRAȚIE
# =====================
def main():
    # Creăm restaurantul
    restaurant = Restaurant("La OOP")

    # Adăugăm în meniu (OCP)
    restaurant.add_to_menu(Pizza("Margherita", 120, ["mozzarella", "busuioc"]))
    restaurant.add_to_menu(Pizza("Quattro Stagioni", 150, ["ciuperci", "măsline"]))
    restaurant.add_to_menu(Pasta("Carbonara", 110, "spaghete"))

    # Înregistrăm client
    client = Client("Ion Popescu", "069123456")
    restaurant.register_client(client)

    # Afișăm meniul
    restaurant.display_menu()

    # Creăm comandă
    order = restaurant.create_order(client)
    order.add_item(restaurant.menu.get_items()[0])
    order.add_item(restaurant.menu.get_items()[2])

    print(f"\nTotal comandă: {order.calculate_total()} MDL")

    # Procesăm plată (DIP)
    payment = CardPayment("1234567890123456")
    result = restaurant.process_order(order, payment)
    print(f"Rezultat plată: {result}")

    # Verificăm puncte loialitate
    print(f"Puncte loialitate {client.name}: {client.loyalty_points}")


if __name__ == "__main__":
    main()