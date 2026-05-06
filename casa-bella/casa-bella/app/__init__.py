"""Aplicatia Flask Casa Bella - integreaza toate cele 13 patterns."""
from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
from .data import PRODUCTS, CATEGORIES, build_composite_menu
from . import services as svc
from patterns import AppConfig

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.secret_key = "casa-bella-secret-demo"
    cfg = AppConfig()

    @app.context_processor
    def inject():
        cart = session.get("cart", {})
        cart_count = sum(cart.values())
        return {"cfg": cfg, "cart_count": cart_count}

    # --- Public ---
    @app.route("/")
    def index():
        featured = ["p1","pa1","f1","d1","p6","pa5"]
        return render_template("index.html", featured=[PRODUCTS[i] for i in featured])

    @app.route("/menu")
    def menu():
        cats = [(name, [PRODUCTS[i] for i in ids]) for name, ids in CATEGORIES]
        return render_template("menu.html", categories=cats)

    @app.route("/cart/add/<pid>", methods=["POST"])
    def cart_add(pid):
        cart = session.get("cart", {})
        svc.save_cart_snapshot(cart)  # MEMENTO
        cart[pid] = cart.get(pid, 0) + 1
        session["cart"] = cart
        flash(f"{PRODUCTS[pid].name} adaugat in cos", "success")
        return redirect(request.referrer or url_for("menu"))

    @app.route("/cart")
    def cart_view():
        cart = session.get("cart", {})
        lines = [{"product": PRODUCTS[pid], "qty": q, "subtotal": round(PRODUCTS[pid].price*q,2)}
                 for pid, q in cart.items() if pid in PRODUCTS]
        total = round(sum(l["subtotal"] for l in lines), 2)
        return render_template("cart.html", lines=lines, total=total,
                               can_undo=svc.caretaker.size() > 0)

    @app.route("/cart/remove/<pid>", methods=["POST"])
    def cart_remove(pid):
        cart = session.get("cart", {})
        svc.save_cart_snapshot(cart)
        cart.pop(pid, None)
        session["cart"] = cart
        return redirect(url_for("cart_view"))

    @app.route("/cart/undo", methods=["POST"])
    def cart_undo():
        cart = session.get("cart", {})
        cart = svc.undo_cart(cart)
        session["cart"] = cart
        flash("Ultima modificare a cosului anulata (Memento)", "info")
        return redirect(url_for("cart_view"))

    @app.route("/checkout", methods=["GET","POST"])
    def checkout():
        cart = session.get("cart", {})
        if not cart:
            flash("Cos gol", "warning"); return redirect(url_for("menu"))
        if request.method == "POST":
            method = request.form["payment_method"]
            address = request.form["address"]
            notes = request.form.get("notes","")
            order = svc.checkout(cart, method, address, notes)
            session["cart"] = {}
            return render_template("order_confirmation.html", order=order)
        lines = [{"product": PRODUCTS[pid], "qty": q} for pid, q in cart.items()]
        total = round(sum(PRODUCTS[pid].price*q for pid,q in cart.items()), 2)
        return render_template("checkout.html", lines=lines, total=total)

    # --- Admin ---
    @app.route("/admin")
    def admin():
        return render_template("admin.html",
                               orders=list(svc.ORDERS.values())[::-1],
                               notif_log=svc.notif_log[-15:][::-1],
                               mediator_log=svc.mediator.log[-15:][::-1])

    @app.route("/admin/status/<oid>/<new>", methods=["POST"])
    def admin_status(oid, new):
        ok, msg = svc.change_status(oid, new)
        flash(msg, "success" if ok else "danger")
        return redirect(url_for("admin"))

    @app.route("/admin/undo", methods=["POST"])
    def admin_undo():
        flash(f"Undo: {svc.admin_undo()}", "info")
        return redirect(url_for("admin"))

    @app.route("/admin/export/<fmt>")
    def admin_export(fmt):
        out, mime = svc.export_orders(fmt)
        return Response(out, mimetype=mime,
                        headers={"Content-Disposition": f'attachment; filename="orders.{fmt}"'})

    # --- Patterns showcase ---
    @app.route("/patterns")
    def patterns_page():
        tree = build_composite_menu().display()
        return render_template("patterns.html", composite_tree=tree,
                               total_products=build_composite_menu().count())

    return app
