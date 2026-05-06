"""Servicii: aici converg patterns peste logica de business."""
from typing import Dict
from patterns import (
    AppConfig, OrderBuilder, PaymentContext, strategy_for,
    BaseUINotifier, EmailDecorator, SMSDecorator,
    order_bus, OrderEvent, CommandInvoker, ChangeOrderStatusCommand,
    OrderStateMachine, RestaurantMediator,
    JSONExportVisitor, CSVExportVisitor, XMLExportVisitor,
    OrderOriginator, OrderCaretaker,
)
from .data import PRODUCTS
import uuid

# SINGLETON
config = AppConfig()
# MEDIATOR
mediator = RestaurantMediator()
mediator.register("kitchen",  lambda m: print(f"[KITCHEN] {m}"))
mediator.register("delivery", lambda m: print(f"[DELIVERY] {m}"))
# COMMAND invoker (pt admin undo)
invoker = CommandInvoker()
# MEMENTO caretaker (pt cos undo)
caretaker = OrderCaretaker()

# OBSERVER subscribers
notif_log = []
def _on_event(e: OrderEvent): notif_log.append(f"{e.type}: #{e.order_id[:8]} {e.detail}")
order_bus.subscribe(_on_event)

# Stocare in memorie
ORDERS: Dict[str, dict] = {}

def cart_to_builder(cart_items: dict) -> OrderBuilder:
    """BUILDER: construieste comanda din cosul din sesiune."""
    b = OrderBuilder()
    for pid, qty in cart_items.items():
        if pid in PRODUCTS: b.add(PRODUCTS[pid], qty)
    return b

def save_cart_snapshot(cart: dict):
    """MEMENTO: snapshot inainte de modificare (pentru undo cos)."""
    o = OrderOriginator(dict(cart))
    caretaker.push(o.save())

def undo_cart(cart: dict) -> dict:
    m = caretaker.pop()
    if not m: return cart
    cart.clear(); cart.update(m.state); return cart

def checkout(cart: dict, payment_method: str, address: str, notes: str = "") -> dict:
    """STRATEGY + ADAPTER + DECORATOR + OBSERVER + MEDIATOR + STATE."""
    b = cart_to_builder(cart).payment(payment_method).address(address).note(notes)
    order = b.build()
    order_id = uuid.uuid4().hex
    # STRATEGY (alege adapter)
    pay = PaymentContext(strategy_for(payment_method)).checkout(order.total, order_id)
    # DECORATOR (notificari multiple)
    notifier = SMSDecorator(EmailDecorator(BaseUINotifier()))
    channels = notifier.send(f"Comanda confirmata: {order.total} {config.currency}")
    # MEDIATOR
    mediator.notify("orders", "kitchen", f"Comanda noua #{order_id[:6]}")
    # OBSERVER
    order_bus.publish(OrderEvent("created", order_id, f"total={order.total}"))
    record = {
        "id": order_id,
        "items": [{"name": l.product.name, "qty": l.quantity, "price": l.product.price} for l in order.items],
        "total": order.total, "payment_method": payment_method,
        "delivery_address": address, "notes": notes,
        "status": "pending", "payment": pay, "channels": channels,
    }
    ORDERS[order_id] = record
    return record

def change_status(order_id: str, new_status: str) -> tuple[bool, str]:
    """STATE + COMMAND."""
    o = ORDERS.get(order_id)
    if not o: return False, "Comanda inexistenta"
    fsm = OrderStateMachine(o["status"])
    if not fsm.can(new_status):
        return False, f"Tranzitie invalida {o['status']} -> {new_status}"

    class _Wrap:
        def __init__(s): s.label=f"{o['status']}->{new_status}"; s.prev=o["status"]
        def execute(s): s.prev=o["status"]; o["status"]=new_status
        def undo(s): o["status"]=s.prev
    invoker.run(_Wrap())
    if new_status == "preparing": mediator.notify("orders","kitchen", f"Pregateste #{order_id[:6]}")
    if new_status == "delivering": mediator.notify("orders","delivery", f"Livreaza #{order_id[:6]}")
    order_bus.publish(OrderEvent("status_changed", order_id, f"-> {new_status}"))
    return True, f"Status -> {new_status}"

def admin_undo() -> str:
    return invoker.undo_last() or "Nimic de anulat"

def export_orders(fmt: str) -> tuple[str, str]:
    """VISITOR."""
    visitor = {"json": JSONExportVisitor(), "csv": CSVExportVisitor(), "xml": XMLExportVisitor()}[fmt]
    if fmt == "csv":
        rows = [visitor.visit(o) for o in ORDERS.values()]
        out = (rows[0] if rows else "id,total,status,payment,address")
        for r in rows[1:]: out += "\n" + r.split("\n")[1]
    else:
        out = "\n\n".join(visitor.visit(o) for o in ORDERS.values())
    mime = {"json":"application/json","csv":"text/csv","xml":"application/xml"}[fmt]
    return out, mime
