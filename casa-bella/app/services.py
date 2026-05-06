"""Servicii — orchestrarea pattern-urilor în logica de business."""
from patterns import (
    OrderBuilder, PaymentContext, strategy_for,
    BaseNotifier, UIDecorator, EmailDecorator, SMSDecorator,
    EmailNotificationFactory, SMSNotificationFactory,
    RestaurantFacade, order_bus, OrderEvent,
    OrderStateMachine, app_config,
    CommandInvoker, ChangeOrderStatusCommand,
)
from . import db
from .data import find_product

facade = RestaurantFacade()
admin_invoker = CommandInvoker()    # Command pattern, instanță globală pentru Admin


def build_order_from_cart(cart: dict[str, int], payment: str, address: str, notes: str):
    """Pattern 03: Builder."""
    b = OrderBuilder().with_payment(payment).with_address(address).with_notes(notes)
    for pid_str, qty in cart.items():
        p = find_product(int(pid_str))
        if p:
            b.add_item(p, qty)
    return b.build()


def checkout(user_id: int, cart: dict, payment: str, address: str, notes: str):
    """Orchestrare completă: Builder → Strategy/Adapter → Facade →
    Decorator (notificări) → Abstract Factory (email/SMS) → Observer."""
    order = build_order_from_cart(cart, payment, address, notes)
    if not order.items:
        raise ValueError("Coșul este gol")

    # taxă + livrare din Singleton
    cfg = app_config
    total_with_fees = order.total * (1 + cfg.tax_rate) + cfg.delivery_fee

    # 1. salvăm în DB
    conn = db.get_conn()
    cur = conn.execute(
        "INSERT INTO orders(user_id,total,payment_method,delivery_address,notes,status) VALUES(?,?,?,?,?,?)",
        (user_id, total_with_fees, payment, address, notes, "pending"),
    )
    oid = cur.lastrowid
    for p, q in order.items:
        conn.execute(
            "INSERT INTO order_items(order_id,product_id,name,unit_price,quantity) VALUES(?,?,?,?,?)",
            (oid, p.id, p.name, p.price, q),
        )
    conn.commit()
    conn.close()

    # 2. Strategy + Adapter — procesăm "plata"
    pay_ctx = PaymentContext(strategy_for(payment))
    pay_result = pay_ctx.checkout(total_with_fees, f"order-{oid}")

    # 3. Facade — anunță subsistemele
    facade_log = facade.place_order(str(oid), order.items, address)

    # 4. Decorator — lanț de notificări
    notifier = SMSDecorator(EmailDecorator(UIDecorator(BaseNotifier())))
    notif_log = notifier.send(f"Comanda #{oid} confirmată — {total_with_fees:.2f} MDL")

    # 5. Abstract Factory — generăm conținutul email + SMS
    email_factory = EmailNotificationFactory()
    sms_factory = SMSNotificationFactory()
    extra_log = [
        email_factory.make_sender().send("client@example.com",
            email_factory.make_template().render(str(oid), total_with_fees)),
        sms_factory.make_sender().send("+373xxxxxxxx",
            sms_factory.make_template().render(str(oid), total_with_fees)),
    ]

    # 6. Observer — emit eveniment
    order_bus.publish(OrderEvent("created", str(oid), {"total": total_with_fees}))

    return {
        "order_id": oid,
        "total": total_with_fees,
        "payment": pay_result,
        "facade_log": facade_log,
        "notifications": notif_log + extra_log,
    }


# === Admin: State + Command ===
def change_order_status(order_id: int, new_status: str) -> str:
    """Folosit de Command. Întoarce statusul anterior pentru undo."""
    conn = db.get_conn()
    row = conn.execute("SELECT status FROM orders WHERE id=?", (order_id,)).fetchone()
    if not row:
        conn.close()
        raise ValueError("Comandă inexistentă")
    previous = row["status"]
    fsm = OrderStateMachine(previous)
    # Permitem și revenirea (pentru undo) — verificăm doar la "next"
    if new_status not in (previous, *fsm.next_options(),
                          *[s for opts in __import__("patterns").ORDER_TRANSITIONS.values() for s in opts]):
        conn.close()
        raise ValueError(f"Status invalid: {new_status}")
    conn.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order_id))
    conn.commit()
    conn.close()
    order_bus.publish(OrderEvent("status_changed", str(order_id),
                                 {"from": previous, "to": new_status}))
    return previous


def admin_transition(order_id: int, new_status: str):
    """Validează cu State Machine, execută cu Command (pentru undo)."""
    conn = db.get_conn()
    row = conn.execute("SELECT status FROM orders WHERE id=?", (order_id,)).fetchone()
    conn.close()
    if not row:
        raise ValueError("Comandă inexistentă")
    fsm = OrderStateMachine(row["status"])
    fsm.transition_to(new_status)   # ridică ValueError dacă e invalid
    cmd = ChangeOrderStatusCommand(order_id, new_status, change_order_status)
    admin_invoker.run(cmd)


def admin_undo():
    admin_invoker.undo_last()
