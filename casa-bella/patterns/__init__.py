"""
Casa Bella — 13 Design Patterns
================================
Distribuție conform cerinței academice:

CREATIONAL (4):
  01. Factory Method   — patterns/p01_factory_method.py
  02. Abstract Factory — patterns/p02_abstract_factory.py
  03. Builder          — patterns/p03_builder.py
  04. Prototype        — patterns/p04_prototype.py

STRUCTURAL (4):
  05. Adapter   — patterns/p05_adapter.py
  06. Decorator — patterns/p06_decorator.py
  07. Composite — patterns/p07_composite.py
  08. Facade    — patterns/p08_facade.py

BEHAVIORAL (4):
  09. Strategy — patterns/p09_strategy.py
  10. Observer — patterns/p10_observer.py
  11. Command  — patterns/p11_command.py
  12. State    — patterns/p12_state.py

OBLIGATORIU:
  13. Singleton — patterns/p13_singleton.py
"""
from .p01_factory_method import ProductFactory, FoodProduct, DrinkProduct, MenuProduct
from .p02_abstract_factory import (
    NotificationFactory, EmailNotificationFactory, SMSNotificationFactory,
)
from .p03_builder import OrderBuilder, Order
from .p04_prototype import ProductPrototype
from .p05_adapter import StripeAdapter, PayPalAdapter, CashAdapter, PaymentGateway
from .p06_decorator import (
    BaseNotifier, EmailDecorator, SMSDecorator, UIDecorator, Notifier,
)
from .p07_composite import MenuComponent, LeafProduct, MenuCategory
from .p08_facade import RestaurantFacade
from .p09_strategy import PaymentContext, strategy_for
from .p10_observer import order_bus, OrderEvent
from .p11_command import CommandInvoker, ChangeOrderStatusCommand
from .p12_state import OrderStateMachine, ORDER_TRANSITIONS
from .p13_singleton import AppConfig, app_config

__all__ = [
    "ProductFactory", "FoodProduct", "DrinkProduct", "MenuProduct",
    "NotificationFactory", "EmailNotificationFactory", "SMSNotificationFactory",
    "OrderBuilder", "Order", "ProductPrototype",
    "StripeAdapter", "PayPalAdapter", "CashAdapter", "PaymentGateway",
    "BaseNotifier", "EmailDecorator", "SMSDecorator", "UIDecorator", "Notifier",
    "MenuComponent", "LeafProduct", "MenuCategory", "RestaurantFacade",
    "PaymentContext", "strategy_for", "order_bus", "OrderEvent",
    "CommandInvoker", "ChangeOrderStatusCommand",
    "OrderStateMachine", "ORDER_TRANSITIONS",
    "AppConfig", "app_config",
]
