"""11. MEDIATOR
Bucataria, Livrarea, Comenzile comunica DOAR prin mediator.
"""
class RestaurantMediator:
    def __init__(self): self.handlers = {}; self.log = []
    def register(self, name: str, fn): self.handlers[name] = fn
    def notify(self, sender: str, target: str, msg: str):
        entry = f"{sender} -> {target}: {msg}"
        self.log.append(entry)
        if target in self.handlers: self.handlers[target](msg)
        return entry
