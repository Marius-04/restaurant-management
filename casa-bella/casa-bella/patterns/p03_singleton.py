"""3. SINGLETON
O singura instanta de configurare in toata aplicatia.
"""
import threading

class _Singleton(type):
    _inst = {}; _lock = threading.Lock()
    def __call__(cls, *a, **kw):
        with cls._lock:
            if cls not in cls._inst:
                cls._inst[cls] = super().__call__(*a, **kw)
        return cls._inst[cls]

class AppConfig(metaclass=_Singleton):
    def __init__(self):
        self.restaurant_name = "Casa Bella"
        self.currency = "Lei"
        self.delivery_fee = 15.0
        self.tax_rate = 0.09
