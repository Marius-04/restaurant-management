"""13. MEMENTO
Salvam snapshot-uri ale comenzii pentru undo (caretaker tine istoricul).
"""
import copy

class OrderMemento:
    def __init__(self, state): self.state = copy.deepcopy(state)

class OrderOriginator:
    def __init__(self, state=None): self.state = state or {}
    def set(self, s): self.state = s
    def get(self): return self.state
    def save(self): return OrderMemento(self.state)
    def restore(self, m: OrderMemento): self.state = copy.deepcopy(m.state)

class OrderCaretaker:
    def __init__(self): self.stack = []
    def push(self, m): self.stack.append(m)
    def pop(self): return self.stack.pop() if self.stack else None
    def size(self): return len(self.stack)
