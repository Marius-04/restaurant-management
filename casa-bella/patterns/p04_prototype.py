"""
04. PROTOTYPE  (Creational)
--------------------------------------------------------------
Clonăm produsele existente (cu mici modificări) fără să mai
trecem prin constructori sau prin DB. Util pentru "duplicat în Admin".

Folosit în: app/__init__.py → ruta /admin/clone/<id>.
"""
import copy
from .p01_factory_method import MenuProduct


class ProductPrototype:
    @staticmethod
    def clone(product: MenuProduct, **overrides) -> MenuProduct:
        new = copy.deepcopy(product)
        for k, v in overrides.items():
            setattr(new, k, v)
        return new
