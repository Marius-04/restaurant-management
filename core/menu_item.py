from abc import ABC, abstractmethod


class MenuItem(ABC):
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @abstractmethod
    def get_details(self):
        pass
