"""
LABORATOR 6: Design Patterns Comportamentale
=============================================

Paternuri implementate:
1. Strategy
2. Observer
3. Command
4. Memento
5. Iterator
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any, Iterator as IteratorType
from datetime import datetime
import copy


# ============================================================================
# PATTERN 1: STRATEGY
# ============================================================================

class SortingStrategy(ABC):
    """Interfață pentru strategii de sortare"""
    
    @abstractmethod
    def sort(self, items: List[int]) -> List[int]:
        pass


class BubbleSort(SortingStrategy):
    """Strategie - Bubble Sort"""
    
    def sort(self, items: List[int]) -> List[int]:
        result = items.copy()
        n = len(result)
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result


class QuickSort(SortingStrategy):
    """Strategie - Quick Sort"""
    
    def sort(self, items: List[int]) -> List[int]:
        if len(items) <= 1:
            return items
        pivot = items[len(items) // 2]
        left = [x for x in items if x < pivot]
        middle = [x for x in items if x == pivot]
        right = [x for x in items if x > pivot]
        return self.sort(left) + middle + self.sort(right)


class MergeSort(SortingStrategy):
    """Strategie - Merge Sort"""
    
    def sort(self, items: List[int]) -> List[int]:
        if len(items) <= 1:
            return items
        mid = len(items) // 2
        left = self.sort(items[:mid])
        right = self.sort(items[mid:])
        return self._merge(left, right)
    
    @staticmethod
    def _merge(left: List[int], right: List[int]) -> List[int]:
        result = []
        while left and right:
            if left[0] <= right[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        return result + left + right


class DataSorter:
    """Context care folosește strategiile de sortare"""
    
    def __init__(self, strategy: SortingStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortingStrategy) -> None:
        self._strategy = strategy
    
    def sort(self, items: List[int]) -> List[int]:
        return self._strategy.sort(items)


# ============================================================================
# PATTERN 2: OBSERVER
# ============================================================================

class RestaurantEvent(ABC):
    """Interfață pentru observatori"""
    
    @abstractmethod
    def update(self, event_data: dict) -> None:
        pass


class OrderReadyNotifier(RestaurantEvent):
    """Observer - Notifică când comanda e gata"""
    
    def update(self, event_data: dict) -> None:
        if event_data.get("event_type") == "order_ready":
            print(f"📲 Customer {event_data['customer']} - "
                  f"Your order is ready! (ID: {event_data['order_id']})")


class KitchenDisplay(RestaurantEvent):
    """Observer - Display în bucătărie"""
    
    def update(self, event_data: dict) -> None:
        if event_data.get("event_type") == "order_ready":
            print(f"🖥️  Kitchen: Order {event_data['order_id']} "
                  f"is ready for pickup")


class RevenueTracker(RestaurantEvent):
    """Observer - Urmărire revenue"""
    
    def __init__(self):
        self.total_revenue = 0.0
    
    def update(self, event_data: dict) -> None:
        if event_data.get("event_type") == "payment_received":
            amount = event_data.get("amount", 0)
            self.total_revenue += amount
            print(f"💰 Revenue updated: ${self.total_revenue:.2f}")


class OrderSubject:
    """Subject - Observable"""
    
    def __init__(self):
        self._observers: List[RestaurantEvent] = []
    
    def attach(self, observer: RestaurantEvent) -> None:
        """Adaugă observer"""
        self._observers.append(observer)
    
    def detach(self, observer: RestaurantEvent) -> None:
        """Elimină observer"""
        self._observers.remove(observer)
    
    def notify(self, event_data: dict) -> None:
        """Notifică toți observerii"""
        for observer in self._observers:
            observer.update(event_data)
    
    def complete_order(self, order_id: str, customer: str, amount: float) -> None:
        """Completează comanda și notifică"""
        self.notify({
            "event_type": "order_ready",
            "order_id": order_id,
            "customer": customer
        })
        self.notify({
            "event_type": "payment_received",
            "amount": amount
        })


# ============================================================================
# PATTERN 3: COMMAND
# ============================================================================

class RestaurantCommand(ABC):
    """Interfață pentru comenzi"""
    
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @abstractmethod
    def undo(self) -> None:
        pass


class PlaceOrderCommand(RestaurantCommand):
    """Comandă - Plasare comandă"""
    
    def __init__(self, order_id: str, items: List[str]):
        self.order_id = order_id
        self.items = items
        self.executed = False
    
    def execute(self) -> None:
        print(f"✓ Order {self.order_id} placed with items: {', '.join(self.items)}")
        self.executed = True
    
    def undo(self) -> None:
        if self.executed:
            print(f"✗ Order {self.order_id} cancelled")
            self.executed = False


class CancelOrderCommand(RestaurantCommand):
    """Comandă - Anulare comandă"""
    
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.was_active = True
    
    def execute(self) -> None:
        print(f"✗ Order {self.order_id} cancelled")
        self.was_active = False
    
    def undo(self) -> None:
        print(f"↩️  Order {self.order_id} restoration requested")
        self.was_active = True


class ApplyDiscountCommand(RestaurantCommand):
    """Comandă - Aplicare discount"""
    
    def __init__(self, order_id: str, discount_percent: float):
        self.order_id = order_id
        self.discount_percent = discount_percent
    
    def execute(self) -> None:
        print(f"💳 Applied {self.discount_percent}% discount to order {self.order_id}")
    
    def undo(self) -> None:
        print(f"↩️  Discount removed from order {self.order_id}")


class CommandHistory:
    """Manager pentru comenzi (cu undo/redo)"""
    
    def __init__(self):
        self.history: List[RestaurantCommand] = []
        self.redo_stack: List[RestaurantCommand] = []
    
    def execute_command(self, command: RestaurantCommand) -> None:
        """Execută comandă"""
        command.execute()
        self.history.append(command)
        self.redo_stack.clear()
    
    def undo(self) -> None:
        """Undo ultima comandă"""
        if self.history:
            command = self.history.pop()
            command.undo()
            self.redo_stack.append(command)
    
    def redo(self) -> None:
        """Redo ultima anulare"""
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.history.append(command)


# ============================================================================
# PATTERN 4: MEMENTO
# ============================================================================

class OrderMemento:
    """Memento - Salvează starea comenzii"""
    
    def __init__(self, order_id: str, items: List[str], total: float):
        self.order_id = order_id
        self.items = items.copy()
        self.total = total
        self.timestamp = datetime.now()
    
    def get_state(self) -> dict:
        return {
            "order_id": self.order_id,
            "items": self.items,
            "total": self.total,
            "timestamp": self.timestamp
        }


class Order:
    """Originator - Poate salva/restaura starea"""
    
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.items: List[str] = []
        self.total: float = 0.0
    
    def add_item(self, item: str, price: float) -> None:
        self.items.append(item)
        self.total += price
    
    def save_state(self) -> OrderMemento:
        """Salvează starea (crează memento)"""
        return OrderMemento(self.order_id, self.items, self.total)
    
    def restore_state(self, memento: OrderMemento) -> None:
        """Restaurează starea din memento"""
        state = memento.get_state()
        self.order_id = state["order_id"]
        self.items = state["items"].copy()
        self.total = state["total"]
    
    def get_info(self) -> str:
        return f"Order {self.order_id}: {self.items} - Total: ${self.total:.2f}"


class OrderCaretaker:
    """Caretaker - Gestionează mementos"""
    
    def __init__(self):
        self.history: List[OrderMemento] = []
    
    def save(self, memento: OrderMemento) -> None:
        """Salvează memento în istoric"""
        self.history.append(memento)
    
    def restore(self, index: int) -> Optional[OrderMemento]:
        """Restaurează memento din istoric"""
        if 0 <= index < len(self.history):
            return self.history[index]
        return None
    
    def list_versions(self) -> None:
        """Listează toate versiunile"""
        for i, memento in enumerate(self.history):
            state = memento.get_state()
            print(f"Version {i}: {state['order_id']} - "
                  f"Items: {state['items']} - Total: ${state['total']:.2f}")


# ============================================================================
# PATTERN 5: ITERATOR
# ============================================================================

class MenuItem:
    """Element din meniu"""
    
    def __init__(self, name: str, price: float, category: str):
        self.name = name
        self.price = price
        self.category = category
    
    def __str__(self) -> str:
        return f"{self.name} (${self.price}) - {self.category}"


class MenuIterator(IteratorType[MenuItem]):
    """Iterator pentru meniu"""
    
    def __init__(self, items: List[MenuItem]):
        self.items = items
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self) -> MenuItem:
        if self.index < len(self.items):
            item = self.items[self.index]
            self.index += 1
            return item
        raise StopIteration
    
    def reset(self) -> None:
        """Resetează iteratorul"""
        self.index = 0
    
    def has_next(self) -> bool:
        """Verifică dacă mai sunt itemi"""
        return self.index < len(self.items)


class Menu:
    """Container cu iterator"""
    
    def __init__(self):
        self.items: List[MenuItem] = []
    
    def add_item(self, item: MenuItem) -> None:
        self.items.append(item)
    
    def create_iterator(self) -> MenuIterator:
        return MenuIterator(self.items)
    
    def __iter__(self) -> MenuIterator:
        return self.create_iterator()


if __name__ == "__main__":
    print("=" * 60)
    print("LABORATOR 6: Strategy, Observer, Command, Memento, Iterator")
    print("=" * 60)
    
    # ====== STRATEGY ======
    print("\n1. STRATEGY - Different Sorting Algorithms")
    print("-" * 60)
    
    data = [64, 34, 25, 12, 22, 11, 90]
    
    sorter = DataSorter(BubbleSort())
    print(f"Bubble Sort: {sorter.sort(data)}")
    
    sorter.set_strategy(QuickSort())
    print(f"Quick Sort: {sorter.sort(data)}")
    
    sorter.set_strategy(MergeSort())
    print(f"Merge Sort: {sorter.sort(data)}")
    
    # ====== OBSERVER ======
    print("\n\n2. OBSERVER - Order Notification System")
    print("-" * 60)
    
    order_subject = OrderSubject()
    
    # Adaugă observeri
    notifier = OrderReadyNotifier()
    kitchen = KitchenDisplay()
    revenue = RevenueTracker()
    
    order_subject.attach(notifier)
    order_subject.attach(kitchen)
    order_subject.attach(revenue)
    
    # Completează o comandă
    order_subject.complete_order("ORD001", "John", 45.99)
    
    # ====== COMMAND ======
    print("\n\n3. COMMAND - Order Commands with Undo/Redo")
    print("-" * 60)
    
    history = CommandHistory()
    
    # Execută comenzi
    history.execute_command(PlaceOrderCommand("ORD002", ["Pizza", "Salad"]))
    history.execute_command(ApplyDiscountCommand("ORD002", 10))
    
    print("\nUndo last command:")
    history.undo()
    
    print("Redo:")
    history.redo()
    
    # ====== MEMENTO ======
    print("\n\n4. MEMENTO - Order State History")
    print("-" * 60)
    
    order = Order("ORD003")
    caretaker = OrderCaretaker()
    
    # V1: Adaugă Pizza
    order.add_item("Pizza Margherita", 12.99)
    caretaker.save(order.save_state())
    print(f"V1: {order.get_info()}")
    
    # V2: Adaugă Salad
    order.add_item("Caesar Salad", 7.99)
    caretaker.save(order.save_state())
    print(f"V2: {order.get_info()}")
    
    # V3: Adaugă Drink
    order.add_item("Soda", 2.99)
    caretaker.save(order.save_state())
    print(f"V3: {order.get_info()}")
    
    print("\nAvailable versions:")
    caretaker.list_versions()
    
    print("\nRestore to version 1:")
    order.restore_state(caretaker.restore(0))
    print(f"Current: {order.get_info()}")
    
    # ====== ITERATOR ======
    print("\n\n5. ITERATOR - Menu Navigation")
    print("-" * 60)
    
    menu = Menu()
    menu.add_item(MenuItem("Pizza Margherita", 12.99, "Main"))
    menu.add_item(MenuItem("Caesar Salad", 7.99, "Appetizer"))
    menu.add_item(MenuItem("Tiramisu", 5.99, "Dessert"))
    menu.add_item(MenuItem("Soda", 2.99, "Beverage"))
    
    print("Using iterator:")
    iterator = menu.create_iterator()
    while iterator.has_next():
        print(f"  • {next(iterator)}")
    
    print("\nUsing for loop (implements Iterator):")
    for item in menu:
        print(f"  • {item}")
    
    print("\n" + "=" * 60)
