"""4. ADAPTER
Adaptam SDK-uri externe (Stripe, PayPal) la o interfata unica PaymentGateway.
"""
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def pay(self, amount: float, ref: str) -> dict: ...

# SDK-uri "externe" simulate
class _StripeSDK:
    def charge(self, cents: int, ref: str): return {"ok": True, "id": f"st_{ref}", "cents": cents}
class _PayPalSDK:
    def send_payment(self, usd: float, ref: str): return {"status": "COMPLETED", "txn": f"pp_{ref}", "usd": usd}

class StripeAdapter(PaymentGateway):
    def __init__(self): self.sdk = _StripeSDK()
    def pay(self, amount, ref):
        r = self.sdk.charge(int(amount*100), ref)
        return {"provider": "stripe", "ok": r["ok"], "id": r["id"]}

class PayPalAdapter(PaymentGateway):
    def __init__(self): self.sdk = _PayPalSDK()
    def pay(self, amount, ref):
        r = self.sdk.send_payment(amount, ref)
        return {"provider": "paypal", "ok": r["status"] == "COMPLETED", "id": r["txn"]}

class CashAdapter(PaymentGateway):
    def pay(self, amount, ref):
        return {"provider": "cash", "ok": True, "id": f"cash_{ref}"}
