"""9. COMMAND
Incapsulam actiuni (schimbare status) ca obiecte cu execute/undo.
"""
from abc import ABC, abstractmethod

class Command(ABC):
    label: str = ""
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...

class ChangeOrderStatusCommand(Command):
    def __init__(self, order, new_status: str):
        self.order = order; self.new_status = new_status; self.prev = order.status
        self.label = f"Status {order.status} -> {new_status}"
    def execute(self):
        self.prev = self.order.status
        self.order.status = self.new_status
    def undo(self):
        self.order.status = self.prev

class CommandInvoker:
    def __init__(self): self.history = []
    def run(self, cmd: Command):
        cmd.execute(); self.history.append(cmd); return cmd.label
    def undo_last(self):
        if not self.history: return None
        c = self.history.pop(); c.undo(); return c.label
