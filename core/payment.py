from abc import ABC, abstractmethod


class PaymentStrategy(ABC):

    @abstractmethod
    def pay(self, amount):
        pass


class CashPayment(PaymentStrategy):
    def pay(self, amount):
        print(f"Paid {amount}$ in cash.")
