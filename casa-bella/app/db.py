"""SQLite minimal pentru utilizatori, comenzi și itemi."""
import sqlite3, os, hashlib, secrets

DB_PATH = os.path.join(os.path.dirname(__file__), "casabella.db")


def _hash(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode()).hexdigest()


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT,
        salt TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        is_admin INTEGER NOT NULL DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        total REAL NOT NULL,
        payment_method TEXT NOT NULL,
        delivery_address TEXT,
        notes TEXT,
        status TEXT NOT NULL DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS order_items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        unit_price REAL NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY(order_id) REFERENCES orders(id)
    );
    """)
    # cont admin implicit
    c.execute("SELECT id FROM users WHERE email=?", ("admin@casabella.md",))
    if not c.fetchone():
        salt = secrets.token_hex(8)
        c.execute(
            "INSERT INTO users(email, full_name, salt, password_hash, is_admin) VALUES(?,?,?,?,1)",
            ("admin@casabella.md", "Administrator", salt, _hash("admin123", salt)),
        )
    conn.commit()
    conn.close()


def create_user(email: str, password: str, full_name: str) -> int | None:
    salt = secrets.token_hex(8)
    conn = get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO users(email, full_name, salt, password_hash) VALUES(?,?,?,?)",
            (email, full_name, salt, _hash(password, salt)),
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def authenticate(email: str, password: str):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    conn.close()
    if not row:
        return None
    if _hash(password, row["salt"]) != row["password_hash"]:
        return None
    return dict(row)


def get_user(uid: int):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()
    return dict(row) if row else None
