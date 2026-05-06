"""
06. DECORATOR  (Structural)
--------------------------------------------------------------
Adăugăm dinamic canale unei notificări de bază
(UI → +Email → +SMS). Fiecare decorator împachetează un Notifier
și extinde comportamentul fără să modifice clasa de bază.

Folosit în: app/services.py → confirmarea comenzii.
"""
from abc import ABC, abstractmethod
from typing import List


class Notifier(ABC):
    @abstractmethod
    def send(self, msg: str) -> List[str]: ...


class BaseNotifier(Notifier):
    def send(self, msg):
        return [f"[CONSOLE] {msg}"]


class _NotifierDecorator(Notifier):
    def __init__(self, wrapped: Notifier):
        self._wrapped = wrapped

    def send(self, msg):
        return self._wrapped.send(msg)


class UIDecorator(_NotifierDecorator):
    def send(self, msg):
        return super().send(msg) + [f"[UI] {msg}"]


class EmailDecorator(_NotifierDecorator):
    def send(self, msg):
        return super().send(msg) + [f"[EMAIL] {msg}"]


class SMSDecorator(_NotifierDecorator):
    def send(self, msg):
        return super().send(msg) + [f"[SMS] {msg}"]
