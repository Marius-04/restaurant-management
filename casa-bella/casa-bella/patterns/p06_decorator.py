"""6. DECORATOR
Adaugam dinamic canale de notificare (UI -> +Email -> +SMS).
"""
class Notifier:
    def send(self, msg: str): return [f"[UI] {msg}"]

class BaseUINotifier(Notifier): pass

class _Wrap(Notifier):
    def __init__(self, inner: Notifier): self.inner = inner
    def send(self, msg): return self.inner.send(msg)

class EmailDecorator(_Wrap):
    def send(self, msg): return super().send(msg) + [f"[Email] {msg}"]

class SMSDecorator(_Wrap):
    def send(self, msg): return super().send(msg) + [f"[SMS] {msg}"]
