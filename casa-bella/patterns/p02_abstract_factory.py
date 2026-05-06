"""
02. ABSTRACT FACTORY  (Creational)
--------------------------------------------------------------
Familie de obiecte înrudite (canale de notificare): un Email
are un sender + un template, un SMS are alt sender + alt template.

Folosit în: app/services.py → la confirmarea comenzii.
"""
from abc import ABC, abstractmethod


# === produse abstracte ===
class Sender(ABC):
    @abstractmethod
    def send(self, to: str, body: str) -> str: ...


class Template(ABC):
    @abstractmethod
    def render(self, order_id: str, total: float) -> str: ...


# === produse concrete – familia EMAIL ===
class EmailSender(Sender):
    def send(self, to, body):
        return f"[EMAIL → {to}] {body}"


class EmailTemplate(Template):
    def render(self, order_id, total):
        return f"Bună! Comanda #{order_id} a fost confirmată. Total: {total:.2f} MDL."


# === produse concrete – familia SMS ===
class SMSSender(Sender):
    def send(self, to, body):
        return f"[SMS → {to}] {body}"


class SMSTemplate(Template):
    def render(self, order_id, total):
        return f"Casa Bella: cmd #{order_id} confirmată ({total:.2f} MDL)"


# === fabrică abstractă + fabrici concrete ===
class NotificationFactory(ABC):
    @abstractmethod
    def make_sender(self) -> Sender: ...
    @abstractmethod
    def make_template(self) -> Template: ...


class EmailNotificationFactory(NotificationFactory):
    def make_sender(self):  return EmailSender()
    def make_template(self): return EmailTemplate()


class SMSNotificationFactory(NotificationFactory):
    def make_sender(self):  return SMSSender()
    def make_template(self): return SMSTemplate()
