"""
08. FACADE  (Structural)
--------------------------------------------------------------
O față simplă peste subsistemele complexe ale restaurantului:
stoc, bucătărie, livrare. Clientul (ruta Flask) apelează un
singur `place_order` în loc să orchestreze totul.

Folosit în: app/services.py → checkout.
"""
class _StockSystem:
    def reserve(self, items): return True


class _KitchenSystem:
    def queue_order(self, order_id): return f"Comanda {order_id} în bucătărie"


class _DeliverySystem:
    def schedule(self, address): return f"Livrare programată la {address or 'ridicare'}"


class RestaurantFacade:
    def __init__(self):
        self.stock = _StockSystem()
        self.kitchen = _KitchenSystem()
        self.delivery = _DeliverySystem()

    def place_order(self, order_id: str, items, address: str) -> list[str]:
        log = []
        if not self.stock.reserve(items):
            raise RuntimeError("Stoc insuficient")
        log.append("Stoc rezervat")
        log.append(self.kitchen.queue_order(order_id))
        log.append(self.delivery.schedule(address))
        return log
