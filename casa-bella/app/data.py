"""Catalog produse — 35+ items, identice cu site-ul actual + extra.
Fiecare produs are un id stabil și un nume de imagine din /static/img/.
"""
from patterns import ProductFactory, MenuCategory, LeafProduct

# (id, kind, name, price, description, image_filename, category)
RAW = [
    # === ANTREURI ===
    (1, "food", "Bruschete cu roșii", 65, "Pâine prăjită, roșii cherry, busuioc, ulei de măsline", "bruschete.jpg", "Antreuri"),
    (2, "food", "Salată Caprese", 95, "Mozzarella di bufala, roșii, busuioc proaspăt", "caprese.jpg", "Antreuri"),
    (3, "food", "Carpaccio de vită", 130, "Felii fine de vită, rucola, parmezan, ulei de trufe", "carpaccio.jpg", "Antreuri"),
    (4, "food", "Platou de brânzeturi", 180, "Selecție de brânzeturi italiene cu miere și nuci", "platou-branzeturi.jpg", "Antreuri"),
    (5, "food", "Salată Caesar cu pui", 110, "Salată romaină, pui, crutoane, parmezan, sos Caesar", "caesar.jpg", "Antreuri"),

    # === PIZZA ===
    (6, "food", "Margherita", 120, "Mozzarella, roșii San Marzano, busuioc proaspăt", "margherita.jpg", "Pizza"),
    (7, "food", "Quattro Formaggi", 145, "Mozzarella, gorgonzola, parmezan, taleggio", "quattro-formaggi.jpg", "Pizza"),
    (8, "food", "Pizza Diavola", 140, "Salam picant, mozzarella, ardei iute", "diavola.jpg", "Pizza"),
    (9, "food", "Prosciutto e Funghi", 150, "Prosciutto crudo, ciuperci, mozzarella", "prosciutto-funghi.jpg", "Pizza"),

    # === PASTE ===
    (10, "food", "Carbonara", 135, "Spaghetti, guanciale, ou, pecorino romano, piper negru", "carbonara.jpg", "Paste"),
    (11, "food", "Pesto", 125, "Trofie, pesto genovese, cartofi, fasole verde", "pesto.jpg", "Paste"),
    (12, "food", "Lasagna Bolognese", 145, "Lasagna clasică cu ragù bolognese și béchamel", "lasagna.jpg", "Paste"),
    (13, "food", "Penne Arrabbiata", 115, "Penne, sos picant de roșii, usturoi, ardei iute", "arrabbiata.jpg", "Paste"),
    (14, "food", "Risotto ai Funghi Porcini", 155, "Risotto cremos cu hribi și parmezan", "risotto.jpg", "Paste"),

    # === FELURI PRINCIPALE ===
    (15, "food", "Mușchi de vită la grătar", 280, "Mușchi de vită, cartofi rumeniți, sos demi-glace", "muschi-vita.jpg", "Feluri principale"),
    (16, "food", "Somon la cuptor", 220, "File de somon, legume mediteraneene, lămâie", "somon.jpg", "Feluri principale"),
    (17, "food", "Piept de pui la grătar", 165, "Piept de pui, garnitură de cartofi, sos verde", "pui-gratar.jpg", "Feluri principale"),

    # === DESERTURI ===
    (18, "food", "Tiramisu", 75, "Mascarpone, cafea, savoiardi, cacao", "tiramisu.jpg", "Deserturi"),
    (19, "food", "Panna Cotta", 65, "Cremă fină de smântână cu coulis de fructe de pădure", "panna-cotta.jpg", "Deserturi"),
    (20, "food", "Gelato (3 cupe)", 70, "Trei cupe de înghețată artizanală la alegere", "gelato.jpg", "Deserturi"),

    # === BĂUTURI CALDE ===
    (21, "drink", "Espresso", 25, "Espresso single dintr-o cupă de origine italiană", "espresso.jpg", "Băuturi calde"),
    (22, "drink", "Cappuccino", 35, "Espresso, lapte spumat, pudră de cacao", "cappuccino.jpg", "Băuturi calde"),

    # === BĂUTURI RECI ===
    (23, "drink", "Limonadă de casă", 45, "Lămâie proaspătă, mentă, miere, apă plată", "limonada.jpg", "Băuturi reci"),
    (24, "drink", "Suc proaspăt de portocale", 40, "Suc 100% natural, stors la comandă", "suc-portocale.jpg", "Băuturi reci"),
    (25, "drink", "Apă minerală", 20, "Apă minerală 0.5L", "apa-minerala.jpg", "Băuturi reci"),

    # === VINURI ===
    (26, "drink", "Vin roșu (pahar)", 65, "Selecție de vin roșu sec italian, 175 ml", "vin-rosu.jpg", "Vinuri"),

    # === PRODUSE NOI (extra ca să arate mai bogat) ===
    (27, "food", "Antipasto Misto", 165, "Platou cu prosciutto, salam, măsline, brânzeturi", "platou-branzeturi.jpg", "Antreuri"),
    (28, "food", "Pizza Capricciosa", 155, "Mozzarella, șuncă, ciuperci, anghinare, măsline", "prosciutto-funghi.jpg", "Pizza"),
    (29, "food", "Pizza Quattro Stagioni", 160, "Patru anotimpuri: șuncă, ciuperci, anghinare, măsline", "diavola.jpg", "Pizza"),
    (30, "food", "Tagliatelle al Tartufo", 195, "Tagliatelle proaspete cu cremă de trufe negre", "carbonara.jpg", "Paste"),
    (31, "food", "Gnocchi al Pesto", 130, "Gnocchi de cartofi cu pesto genovese", "pesto.jpg", "Paste"),
    (32, "food", "Osso Buco", 295, "Rasol de vițel cu risotto alla milanese", "muschi-vita.jpg", "Feluri principale"),
    (33, "food", "Saltimbocca alla Romana", 210, "Vițel cu prosciutto și salvie, sos de vin alb", "muschi-vita.jpg", "Feluri principale"),
    (34, "food", "Cannoli Siciliani", 70, "Tuburi crocante umplute cu cremă de ricotta", "tiramisu.jpg", "Deserturi"),
    (35, "food", "Affogato al Caffè", 60, "Înghețată de vanilie înecată în espresso", "gelato.jpg", "Deserturi"),
    (36, "drink", "Latte Macchiato", 40, "Lapte spumat marcat cu espresso", "cappuccino.jpg", "Băuturi calde"),
    (37, "drink", "Aperol Spritz", 75, "Aperol, prosecco, apă minerală, felie de portocală", "vin-rosu.jpg", "Vinuri"),
    (38, "drink", "Vin alb (pahar)", 60, "Pinot Grigio, 175 ml", "vin-rosu.jpg", "Vinuri"),
]

CATEGORIES_ORDER = [
    "Antreuri", "Pizza", "Paste", "Feluri principale",
    "Deserturi", "Băuturi calde", "Băuturi reci", "Vinuri",
]


def all_products():
    """Returnează lista de MenuProduct (Factory Method la treabă)."""
    out = []
    for pid, kind, name, price, desc, img, cat in RAW:
        p = ProductFactory.create(kind, id=pid, name=name, price=price,
                                  description=desc, image=img)
        out.append((p, cat))
    return out


def menu_by_category():
    grouped = {c: [] for c in CATEGORIES_ORDER}
    for p, cat in all_products():
        grouped.setdefault(cat, []).append(p)
    return grouped


def find_product(pid: int):
    for p, _ in all_products():
        if p.id == pid:
            return p
    return None


def composite_menu():
    """Pattern 07: arborele meniului ca structură Composite."""
    root = MenuCategory("Casa Bella — Meniu complet")
    grouped = menu_by_category()
    for cat_name in CATEGORIES_ORDER:
        cat = MenuCategory(cat_name)
        for p in grouped.get(cat_name, []):
            cat.add(LeafProduct(p.name, p.price))
        root.add(cat)
    return root
