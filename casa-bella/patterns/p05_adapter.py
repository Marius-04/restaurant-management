"""
05. ADAPTER  (Structural)
--------------------------------------------------------------
SDK-uri de plată diferite (Stripe-like, PayPal-like, Cash) sunt
unificate sub o interfață comună `PaymentGateway`.

Folosit în: Strategy (p09) la finalizarea comenzii.
"""
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PaymentResult:
    success: bool
    transaction_id: str
    provider: str


class PaymentGateway(ABC):
    @abstractmethod
    def pay(self, amount: float, ref: str) -> PaymentResult: ...


# === SDK-uri "externe" cu API-uri incompatibile ===
class _StripeSDK:
    def charge(self, cents: int, reference: str):
        return {"ok": True, "id": "stripe_" + uuid.uuid4().hex[:8]}


class _PayPalSDK:
    def make_payment(self, dollars: float, note: str):
        return {"status": "COMPLETED", "txn": "pp_" + uuid.uuid4().hex[:8]}


# === Adapters ===
class StripeAdapter(PaymentGateway):
    def __init__(self): self._sdk = _StripeSDK()

    def pay(self, amount, ref):
        r = self._sdk.charge(int(amount * 100), ref)
        return PaymentResult(r["ok"], r["id"], "Stripe")


class PayPalAdapter(PaymentGateway):
    def __init__(self): self._sdk = _PayPalSDK()

    def pay(self, amount, ref):
        r = self._sdk.make_payment(amount, ref)
        return PaymentResult(r["status"] == "COMPLETED", r["txn"], "PayPal")


class CashAdapter(PaymentGateway):
    def pay(self, amount, ref):
        return PaymentResult(True, "cash_" + uuid.uuid4().hex[:8], "Cash")
