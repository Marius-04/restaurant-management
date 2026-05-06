"""Aplicația Flask — rute, sesiuni, autentificare cu rol admin."""
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, abort,
)
from functools import wraps

from . import db
from .data import (
    menu_by_category, CATEGORIES_ORDER, find_product, composite_menu,
)
from .services import checkout, admin_transition, admin_undo
from patterns import app_config, ORDER_TRANSITIONS, order_bus


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.secret_key = "casa-bella-secret-key-change-me"
    db.init_db()

    # ----- helpers -----
    def current_user():
        uid = session.get("user_id")
        return db.get_user(uid) if uid else None

    def login_required(fn):
        @wraps(fn)
        def w(*a, **k):
            if not current_user():
                flash("Trebuie să te loghezi mai întâi.", "warn")
                return redirect(url_for("login", next=request.path))
            return fn(*a, **k)
        return w

    def admin_required(fn):
        @wraps(fn)
        def w(*a, **k):
            u = current_user()
            if not u or not u["is_admin"]:
                abort(403)
            return fn(*a, **k)
        return w

    @app.context_processor
    def inject_globals():
        cart = session.get("cart", {})
        return {
            "user": current_user(),
            "cart_count": sum(cart.values()),
            "cfg": app_config,
        }

    # ============ PAGINI PUBLICE ============
    @app.route("/")
    def index():
        # primele 6 produse ca "featured"
        featured = []
        for cat in CATEGORIES_ORDER:
            items = menu_by_category().get(cat, [])
            if items:
                featured.append(items[0])
        return render_template("index.html", featured=featured[:6])

    @app.route("/meniu")
    def menu():
        return render_template("menu.html",
                               grouped=menu_by_category(),
                               categories=CATEGORIES_ORDER)

    # ============ AUTENTIFICARE ============
    @app.route("/auth", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            mode = request.form.get("mode", "login")
            email = request.form["email"].strip().lower()
            pwd = request.form["password"]
            if mode == "register":
                name = request.form.get("full_name", "").strip()
                uid = db.create_user(email, pwd, name)
                if not uid:
                    flash("Email deja înregistrat.", "error")
                    return redirect(url_for("login"))
                session["user_id"] = uid
                flash("Cont creat cu succes!", "ok")
                return redirect(url_for("index"))
            else:
                u = db.authenticate(email, pwd)
                if not u:
                    flash("Email sau parolă greșite.", "error")
                    return redirect(url_for("login"))
                session["user_id"] = u["id"]
                flash(f"Bun venit, {u['full_name'] or u['email']}!", "ok")
                return redirect(url_for("admin") if u["is_admin"] else url_for("index"))
        return render_template("auth.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Te-ai delogat.", "ok")
        return redirect(url_for("index"))

    # ============ COȘ ============
    @app.route("/adauga/<int:pid>", methods=["POST"])
    def add_to_cart(pid):
        p = find_product(pid)
        if not p:
            abort(404)
        cart = session.get("cart", {})
        cart[str(pid)] = cart.get(str(pid), 0) + 1
        session["cart"] = cart
        flash(f"„{p.name}” adăugat în coș.", "ok")
        return redirect(request.referrer or url_for("menu"))

    @app.route("/cos")
    def cart():
        cart = session.get("cart", {})
        items = []
        subtotal = 0
        for pid_str, qty in cart.items():
            p = find_product(int(pid_str))
            if p:
                items.append({"p": p, "qty": qty, "line": p.price * qty})
                subtotal += p.price * qty
        tax = subtotal * app_config.tax_rate
        delivery = app_config.delivery_fee if items else 0
        total = subtotal + tax + delivery
        return render_template("cart.html", items=items,
                               subtotal=subtotal, tax=tax,
                               delivery=delivery, total=total)

    @app.route("/cos/sterge/<int:pid>", methods=["POST"])
    def cart_remove(pid):
        cart = session.get("cart", {})
        cart.pop(str(pid), None)
        session["cart"] = cart
        return redirect(url_for("cart"))

    @app.route("/cos/goleste", methods=["POST"])
    def cart_clear():
        session["cart"] = {}
        return redirect(url_for("cart"))

    # ============ CHECKOUT ============
    @app.route("/checkout", methods=["GET", "POST"])
    @login_required
    def checkout_view():
        cart = session.get("cart", {})
        if not cart:
            flash("Coșul este gol.", "warn")
            return redirect(url_for("menu"))
        if request.method == "POST":
            try:
                result = checkout(
                    user_id=current_user()["id"],
                    cart=cart,
                    payment=request.form.get("payment", "cash"),
                    address=request.form.get("address", "").strip(),
                    notes=request.form.get("notes", "").strip(),
                )
                session["cart"] = {}
                return render_template("checkout_done.html", r=result)
            except Exception as e:
                flash(f"Eroare la checkout: {e}", "error")
        return render_template("checkout.html")

    # ============ COMENZILE MELE ============
    @app.route("/comenzile-mele")
    @login_required
    def my_orders():
        conn = db.get_conn()
        orders = conn.execute(
            "SELECT * FROM orders WHERE user_id=? ORDER BY id DESC",
            (current_user()["id"],),
        ).fetchall()
        result = []
        for o in orders:
            items = conn.execute(
                "SELECT * FROM order_items WHERE order_id=?", (o["id"],)
            ).fetchall()
            result.append({"o": dict(o), "items": [dict(i) for i in items]})
        conn.close()
        return render_template("my_orders.html", orders=result)

    # ============ ADMIN ============
    @app.route("/admin")
    @admin_required
    def admin():
        conn = db.get_conn()
        orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
        conn.close()
        return render_template("admin.html",
                               orders=[dict(o) for o in orders],
                               transitions=ORDER_TRANSITIONS)

    @app.route("/admin/status/<int:oid>", methods=["POST"])
    @admin_required
    def admin_status(oid):
        try:
            admin_transition(oid, request.form["status"])
            flash(f"Comanda #{oid} → {request.form['status']}", "ok")
        except Exception as e:
            flash(str(e), "error")
        return redirect(url_for("admin"))

    @app.route("/admin/undo", methods=["POST"])
    @admin_required
    def admin_undo_route():
        admin_undo()
        flash("Ultima acțiune a fost anulată (Command pattern).", "ok")
        return redirect(url_for("admin"))

    # ============ PATTERNS DEMO ============
    @app.route("/patterns")
    def patterns_page():
        tree = composite_menu().print()
        return render_template("patterns.html",
                               tree=tree,
                               events=order_bus.history[-10:])

    return app
