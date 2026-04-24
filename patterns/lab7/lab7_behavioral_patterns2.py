"""
LABORATORUL 7 - Chain of Responsibility, State, Mediator, Template Method, Visitor
Restaurant Management System - Paternuri Comportamentale Avansate
"""

from abc import ABC, abstractmethod
from typing import List, Optional

# ============================================================================
# CHAIN OF RESPONSIBILITY - Aprobări Comenzi pe Niveluri
# ============================================================================

class OrderApprovalHandler(ABC):
    """Handler abstract pentru aprobări comenzi"""
    def __init__(self):
        self.next_handler: Optional[OrderApprovalHandler] = None

    def set_next(self, handler: 'OrderApprovalHandler') -> 'OrderApprovalHandler':
        self.next_handler = handler
        return handler

    @abstractmethod
    def handle(self, amount: float) -> str: pass

class ManagerApproval(OrderApprovalHandler):
    """Aprobare manager pentru comenzi < 100 MDL"""
    def handle(self, amount: float) -> str:
        if amount < 100:
            return f"✅ Manager: Aprobă comanda de {amount:.2f} MDL"
        return self.next_handler.handle(amount) if self.next_handler else "❌ Nu poate aproba"

class DirectorApproval(OrderApprovalHandler):
    """Aprobare director pentru comenzi < 500 MDL"""
    def handle(self, amount: float) -> str:
        if amount < 500:
            return f"✅ Director: Aprobă comanda de {amount:.2f} MDL"
        return self.next_handler.handle(amount) if self.next_handler else "❌ Nu poate aproba"

class OwnerApproval(OrderApprovalHandler):
    """Aprobare proprietar pentru orice comandă"""
    def handle(self, amount: float) -> str:
        return f"✅ Proprietar: Aprobă comanda de {amount:.2f} MDL"

# ============================================================================
# STATE - Stări Comandă
# ============================================================================

class OrderState(ABC):
    """Interfață pentru stări comandă"""
    @abstractmethod
    def process(self) -> str: pass
    @abstractmethod
    def next_state(self) -> 'OrderState': pass

class PendingState(OrderState):
    """Stare: În Așteptare"""
    def process(self) -> str:
        return "⏳ Comanda este în așteptare"

    def next_state(self) -> OrderState:
        return ConfirmedState()

class ConfirmedState(OrderState):
    """Stare: Confirmată"""
    def process(self) -> str:
        return "✅ Comanda a fost confirmată"

    def next_state(self) -> OrderState:
        return PreparingState()

class PreparingState(OrderState):
    """Stare: În Preparare"""
    def process(self) -> str:
        return "👨‍🍳 Comanda este în preparare"

    def next_state(self) -> OrderState:
        return ReadyState()

class ReadyState(OrderState):
    """Stare: Gata"""
    def process(self) -> str:
        return "🎉 Comanda este gata de servit!"

    def next_state(self) -> OrderState:
        return DeliveredState()

class DeliveredState(OrderState):
    """Stare: Livrată"""
    def process(self) -> str:
        return "✨ Comanda a fost servită"

    def next_state(self) -> OrderState:
        return self

class OrderStateMachine:
    """Mașină de stări pentru comandă"""
    def __init__(self):
        self.state: OrderState = PendingState()

    def transition(self):
        self.state = self.state.next_state()

    def get_status(self) -> str:
        return self.state.process()

# ============================================================================
# MEDIATOR - Coordonare Kitchen
# ============================================================================

class KitchenMediator(ABC):
    """Mediator pentru coordonare bucătărie"""
    @abstractmethod
    def order_placed(self, dish: str) -> str: pass
    @abstractmethod
    def notify_ready(self, dish: str) -> str: pass

class RestaurantKitchenMediator(KitchenMediator):
    """Mediator restaurant - coordonează bucătăria"""
    def __init__(self):
        self.dishes_in_prep = []

    def order_placed(self, dish: str) -> str:
        self.dishes_in_prep.append(dish)
        return f"👨‍🍳 Bucătăria: {dish} a fost adăugat în coadă ({len(self.dishes_in_prep)} plăci în preparare)"

    def notify_ready(self, dish: str) -> str:
        if dish in self.dishes_in_prep:
            self.dishes_in_prep.remove(dish)
        return f"✅ Bucătăria: {dish} este gata! ({len(self.dishes_in_prep)} rămase)"

class Cook:
    """Bucătar"""
    def __init__(self, name: str, mediator: KitchenMediator):
        self.name = name
        self.mediator = mediator

    def prepare_dish(self, dish: str) -> str:
        return self.mediator.order_placed(dish)

    def dish_ready(self, dish: str) -> str:
        return self.mediator.notify_ready(dish)

# ============================================================================
# TEMPLATE METHOD - Generare Rapoarte
# ============================================================================

class ReportGenerator(ABC):
    """Template pentru generare rapoarte"""
    def generate_report(self) -> str:
        header = self.generate_header()
        body = self.generate_body()
        footer = self.generate_footer()
        return f"{header}\n{body}\n{footer}"

    @abstractmethod
    def generate_header(self) -> str: pass

    @abstractmethod
    def generate_body(self) -> str: pass

    @abstractmethod
    def generate_footer(self) -> str: pass

class DailyRevenueReport(ReportGenerator):
    """Raport venituri zilei"""
    def generate_header(self) -> str:
        return "="*50 + "\n📊 RAPORT VENITURI ZILEI\n" + "="*50

    def generate_body(self) -> str:
        return "Venituri: 5000 MDL\nBenevola: 1200 MDL\nNet: 3800 MDL"

    def generate_footer(self) -> str:
        return "="*50 + "\nGenerat: 2024-03-13"

class WeeklyAnalysisReport(ReportGenerator):
    """Raport analiză săptămână"""
    def generate_header(self) -> str:
        return "="*50 + "\n📈 RAPORT SĂPTĂMÂNAL\n" + "="*50

    def generate_body(self) -> str:
        return "Comenzi: 250\nClient mediu: 85 MDL\nZiua top: Sâmbătă"

    def generate_footer(self) -> str:
        return "="*50 + "\nPerioadă: 2024-03-07 la 2024-03-13"

# ============================================================================
# VISITOR - Export Date
# ============================================================================

class DataElement(ABC):
    """Element de date"""
    @abstractmethod
    def accept(self, visitor: 'DataVisitor') -> str: pass

class MenuItem(DataElement):
    """Element meniu"""
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def accept(self, visitor: 'DataVisitor') -> str:
        return visitor.visit_menu_item(self)

class OrderData(DataElement):
    """Date comandă"""
    def __init__(self, order_id: str, total: float):
        self.order_id = order_id
        self.total = total

    def accept(self, visitor: 'DataVisitor') -> str:
        return visitor.visit_order_data(self)

class DataVisitor(ABC):
    """Visitor pentru export date"""
    @abstractmethod
    def visit_menu_item(self, item: MenuItem) -> str: pass
    @abstractmethod
    def visit_order_data(self, order: OrderData) -> str: pass

class JSONExporter(DataVisitor):
    """Export JSON"""
    def visit_menu_item(self, item: MenuItem) -> str:
        return f'{{"menu": "{item.name}", "price": {item.price}}}'

    def visit_order_data(self, order: OrderData) -> str:
        return f'{{"order_id": "{order.order_id}", "total": {order.total}}}'

class XMLExporter(DataVisitor):
    """Export XML"""
    def visit_menu_item(self, item: MenuItem) -> str:
        return f'<menu name="{item.name}" price="{item.price}"/>'

    def visit_order_data(self, order: OrderData) -> str:
        return f'<order id="{order.order_id}" total="{order.total}"/>'

class CSVExporter(DataVisitor):
    """Export CSV"""
    def visit_menu_item(self, item: MenuItem) -> str:
        return f'{item.name},{item.price}'

    def visit_order_data(self, order: OrderData) -> str:
        return f'{order.order_id},{order.total}'

# ============================================================================
# DEMONSTRAȚIE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("LABORATORUL 7 - CHAIN, STATE, MEDIATOR, TEMPLATE, VISITOR")
    print("RESTAURANT MANAGEMENT SYSTEM")
    print("="*80)

    # CHAIN OF RESPONSIBILITY
    print("\n✅ CHAIN OF RESPONSIBILITY - Aprobări:\n")

    manager = ManagerApproval()
    director = DirectorApproval()
    owner = OwnerApproval()

    manager.set_next(director).set_next(owner)

    print("  Comanda 50 MDL:")
    print(f"    {manager.handle(50)}")

    print("\n  Comanda 250 MDL:")
    print(f"    {manager.handle(250)}")

    print("\n  Comanda 1000 MDL:")
    print(f"    {manager.handle(1000)}\n")

    # STATE
    print("✅ STATE - Stări Comandă:\n")

    order_machine = OrderStateMachine()

    print("  Progres comandă:")
    print(f"    1. {order_machine.get_status()}")

    order_machine.transition()
    print(f"    2. {order_machine.get_status()}")

    order_machine.transition()
    print(f"    3. {order_machine.get_status()}")

    order_machine.transition()
    print(f"    4. {order_machine.get_status()}")

    order_machine.transition()
    print(f"    5. {order_machine.get_status()}\n")

    # MEDIATOR
    print("✅ MEDIATOR - Coordonare Kitchen:\n")

    kitchen = RestaurantKitchenMediator()
    cook = Cook("Chef Ion", kitchen)

    print("  Comenzi:")
    print(f"    {cook.prepare_dish('Spaghetti')}")
    print(f"    {cook.prepare_dish('Pizza')}")
    print(f"    {cook.prepare_dish('Salată')}")

    print("\n  Plăci gata:")
    print(f"    {cook.dish_ready('Spaghetti')}")
    print(f"    {cook.dish_ready('Pizza')}\n")

    # TEMPLATE METHOD
    print("✅ TEMPLATE METHOD - Rapoarte:\n")

    daily_report = DailyRevenueReport()
    print("  Raport Zilei:")
    for line in daily_report.generate_report().split('\n'):
        print(f"    {line}")

    print("\n  Raport Săptămânal:")
    weekly_report = WeeklyAnalysisReport()
    for line in weekly_report.generate_report().split('\n'):
        print(f"    {line}")
    print()

    # VISITOR
    print("✅ VISITOR - Export Date:\n")

    menu_item = MenuItem("Spaghetti Carbonara", 24.99)
    order = OrderData("CMD-001", 125.50)

    json_exporter = JSONExporter()
    xml_exporter = XMLExporter()
    csv_exporter = CSVExporter()

    print("  JSON Export:")
    print(f"    Menu: {menu_item.accept(json_exporter)}")
    print(f"    Order: {order.accept(json_exporter)}")

    print("\n  XML Export:")
    print(f"    Menu: {menu_item.accept(xml_exporter)}")
    print(f"    Order: {order.accept(xml_exporter)}")

    print("\n  CSV Export:")
    print(f"    Menu: {menu_item.accept(csv_exporter)}")
    print(f"    Order: {order.accept(csv_exporter)}\n")

    print("="*80)
    print("✅ LAB 7 - COMPLET")
    print("="*80 + "\n")