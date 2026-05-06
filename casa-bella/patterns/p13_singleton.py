"""
13. SINGLETON  (OBLIGATORIU)
--------------------------------------------------------------
O singură instanță globală pentru configurația aplicației
(nume restaurant, monedă, comision livrare, taxă, email suport).
Garantează că oriunde în cod accesăm același obiect.
"""
import threading


class _SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kw):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kw)
        return cls._instances[cls]


class AppConfig(metaclass=_SingletonMeta):
    def __init__(self):
        self.restaurant_name = "Casa Bella"
        self.currency = "MDL"
        self.delivery_fee = 30.0
        self.tax_rate = 0.09
        self.support_email = "contact@casabella.md"

    def update(self, **kw):
        for k, v in kw.items():
            if hasattr(self, k):
                setattr(self, k, v)


# instanță globală exportată
app_config = AppConfig()
