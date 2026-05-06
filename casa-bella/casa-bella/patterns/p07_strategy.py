"""7. STRATEGY
Algoritmul de plata e selectat la runtime in functie de metoda aleasa.
"""
from .p04_adapter import StripeAdapter, PayPalAdapter, CashAdapter, PaymentGateway

class PaymentContext:
    def __init__(self, strategy: PaymentGateway): self.strategy = strategy
    def set(self, s: PaymentGateway): self.strategy = s
    def checkout(self, amount: float, ref: str): return self.strategy.pay(amount, ref)

def strategy_for(method: str) -> PaymentGateway:
    return {"card": StripeAdapter(), "online": PayPalAdapter()}.get(method, CashAdapter())
