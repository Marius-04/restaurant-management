"""
11. COMMAND  (Behavioral)
--------------------------------------------------------------
Acțiunile (schimbare status comandă) sunt obiecte cu execute()
și undo(). Permite istoric + Undo în Admin.

Folosit în: app/__init__.py → ruta /admin (Undo).
"""
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...


class ChangeOrderStatusCommand(Command):
    def __init__(self, order_id, new_status, apply_fn):
        self.order_id = order_id
        self.new_status = new_status
        self.apply_fn = apply_fn   # apply_fn(order_id, status) -> previous_status
        self.previous = None

    def execute(self):
        self.previous = self.apply_fn(self.order_id, self.new_status)

    def undo(self):
        if self.previous is not None:
            self.apply_fn(self.order_id, self.previous)


class CommandInvoker:
    def __init__(self):
        self._history: list[Command] = []

    def run(self, cmd: Command):
        cmd.execute()
        self._history.append(cmd)

    def undo_last(self):
        if self._history:
            self._history.pop().undo()

    def history_size(self):
        return len(self._history)
