"""
09. STRATEGY  (Behavioral)
--------------------------------------------------------------
Selectează la runtime algoritmul de plată în funcție de alegerea
utilizatorului. Fiecare strategie respectă aceeași interfață.

Folosit în: app/services.py → checkout (cash / card / online).
"""
from .p05_adapter import PaymentGateway, StripeAdapter, PayPalAdapter, CashAdapter


class PaymentContext:
    def __init__(self, strategy: PaymentGateway):
        self._strategy = strategy

    def set_strategy(self, s: PaymentGateway):
        self._strategy = s

    def checkout(self, amount: float, ref: str):
        return self._strategy.pay(amount, ref)


def strategy_for(method: str) -> PaymentGateway:
    return {
        "card":   StripeAdapter(),
        "online": PayPalAdapter(),
        "cash":   CashAdapter(),
    }.get(method, CashAdapter())
