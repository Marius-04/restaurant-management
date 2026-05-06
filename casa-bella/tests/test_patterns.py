"""Teste unit pentru toate cele 13 patterns."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from patterns import (
    ProductFactory, EmailNotificationFactory, SMSNotificationFactory,
    OrderBuilder, ProductPrototype,
    StripeAdapter, PayPalAdapter, CashAdapter,
    BaseNotifier, UIDecorator, EmailDecorator, SMSDecorator,
    MenuCategory, LeafProduct,
    RestaurantFacade,
    PaymentContext, strategy_for,
    order_bus, OrderEvent,
    CommandInvoker, ChangeOrderStatusCommand,
    OrderStateMachine,
    AppConfig, app_config,
)


def test_01_factory_method():
    p = ProductFactory.create("food", id=1, name="Margherita", price=120)
    assert p.type == "food" and p.name == "Margherita"

def test_02_abstract_factory():
    f = EmailNotificationFactory()
    msg = f.make_template().render("42", 99.5)
    out = f.make_sender().send("a@b.c", msg)
    assert "EMAIL" in out and "42" in out

def test_03_builder():
    p = ProductFactory.create("drink", id=2, name="Espresso", price=25)
    o = OrderBuilder().add_item(p, 2).with_payment("card").with_address("X").build()
    assert o.total == 50 and o.payment_method == "card"

def test_04_prototype():
    p = ProductFactory.create("food", id=1, name="Margherita", price=120)
    clone = ProductPrototype.clone(p, name="Margherita XL", price=150)
    assert clone.name == "Margherita XL" and p.name == "Margherita"

def test_05_adapter():
    for a in [StripeAdapter(), PayPalAdapter(), CashAdapter()]:
        r = a.pay(50, "ref")
        assert r.success and r.transaction_id

def test_06_decorator():
    n = SMSDecorator(EmailDecorator(UIDecorator(BaseNotifier())))
    log = n.send("hi")
    assert any("CONSOLE" in l for l in log) and any("SMS" in l for l in log)

def test_07_composite():
    root = MenuCategory("All").add(LeafProduct("A", 10)).add(LeafProduct("B", 20))
    assert root.get_price() == 30 and "▸" in root.print()

def test_08_facade():
    log = RestaurantFacade().place_order("1", [], "Str. X")
    assert len(log) == 3

def test_09_strategy():
    ctx = PaymentContext(strategy_for("card"))
    r = ctx.checkout(100, "x")
    assert r.provider == "Stripe"

def test_10_observer():
    seen = []
    off = order_bus.subscribe(lambda e: seen.append(e))
    order_bus.publish(OrderEvent("created", "1", {"total": 50}))
    off()
    assert seen and seen[-1].order_id == "1"

def test_11_command():
    state = {"v": "pending"}
    def apply(_oid, ns):
        prev = state["v"]; state["v"] = ns; return prev
    inv = CommandInvoker()
    inv.run(ChangeOrderStatusCommand(1, "confirmed", apply))
    assert state["v"] == "confirmed"
    inv.undo_last()
    assert state["v"] == "pending"

def test_12_state():
    fsm = OrderStateMachine("pending")
    assert fsm.can_transition_to("confirmed")
    assert not fsm.can_transition_to("delivered")
    fsm.transition_to("confirmed")
    assert fsm.state == "confirmed"

def test_13_singleton():
    a, b = AppConfig(), AppConfig()
    assert a is b is app_config

if __name__ == "__main__":
    import inspect
    tests = [(n, f) for n, f in globals().items() if n.startswith("test_") and inspect.isfunction(f)]
    ok = 0
    for n, f in tests:
        try:
            f(); print(f"✓ {n}"); ok += 1
        except Exception as e:
            print(f"✗ {n} → {e}")
    print(f"\n{ok}/{len(tests)} passed")
