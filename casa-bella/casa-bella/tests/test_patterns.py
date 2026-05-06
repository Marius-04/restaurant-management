"""Teste pentru cele 13 patterns."""
import unittest
from patterns import (ProductFactory, OrderBuilder, AppConfig, StripeAdapter, PayPalAdapter,
    CashAdapter, MenuCategory, MenuLeaf, BaseUINotifier, EmailDecorator, SMSDecorator,
    PaymentContext, strategy_for, order_bus, OrderEvent, CommandInvoker,
    ChangeOrderStatusCommand, OrderStateMachine, RestaurantMediator,
    JSONExportVisitor, CSVExportVisitor, XMLExportVisitor, OrderOriginator, OrderCaretaker)

class T(unittest.TestCase):
    def test_01_factory(self):
        p = ProductFactory.create("food", id="x", name="Pizza", price=30)
        self.assertEqual(p.type, "food")
    def test_02_builder(self):
        p = ProductFactory.create("drink", id="b", name="Apa", price=8)
        o = OrderBuilder().add(p, 2).address("Str").payment("cash").build()
        self.assertEqual(o.total, 16)
    def test_03_singleton(self):
        self.assertIs(AppConfig(), AppConfig())
    def test_04_adapter(self):
        for a in (StripeAdapter(), PayPalAdapter(), CashAdapter()):
            self.assertTrue(a.pay(10, "r")["ok"])
    def test_05_composite(self):
        c = MenuCategory("X").add(MenuLeaf(ProductFactory.create("food", id="i", name="N", price=1)))
        self.assertEqual(c.count(), 1)
    def test_06_decorator(self):
        n = SMSDecorator(EmailDecorator(BaseUINotifier()))
        self.assertEqual(len(n.send("hi")), 3)
    def test_07_strategy(self):
        self.assertEqual(PaymentContext(strategy_for("card")).checkout(5,"r")["provider"], "stripe")
    def test_08_observer(self):
        got = []
        unsub = order_bus.subscribe(lambda e: got.append(e))
        order_bus.publish(OrderEvent("created", "x"))
        unsub(); self.assertEqual(len(got), 1)
    def test_09_command(self):
        class O: status="pending"
        o=O(); inv=CommandInvoker()
        inv.run(ChangeOrderStatusCommand(o, "confirmed"))
        self.assertEqual(o.status, "confirmed"); inv.undo_last()
        self.assertEqual(o.status, "pending")
    def test_10_state(self):
        s = OrderStateMachine("pending")
        self.assertTrue(s.can("confirmed")); self.assertFalse(s.can("delivered"))
    def test_11_mediator(self):
        m = RestaurantMediator(); seen=[]
        m.register("k", lambda x: seen.append(x))
        m.notify("o","k","go"); self.assertEqual(seen, ["go"])
    def test_12_visitor(self):
        d = {"id":"x","total":10,"status":"pending","payment_method":"cash","delivery_address":"a"}
        for v in (JSONExportVisitor(), CSVExportVisitor(), XMLExportVisitor()):
            self.assertTrue(len(v.visit(d)) > 0)
    def test_13_memento(self):
        o = OrderOriginator({"a":1}); c = OrderCaretaker()
        c.push(o.save()); o.set({"a":2}); o.restore(c.pop())
        self.assertEqual(o.get(), {"a":1})

if __name__ == "__main__":
    unittest.main()
