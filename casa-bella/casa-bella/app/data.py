"""Meniu bogat - 35+ produse organizate cu pattern COMPOSITE."""
from patterns import ProductFactory, MenuCategory, MenuLeaf

# (id, name, price, type, description, emoji)
RAW = [
    # Antreuri
    ("a1", "Bruschete cu rosii", 22.0, "food", "Paine prajita, rosii cherry, busuioc, ulei de masline.", "🍅"),
    ("a2", "Carpaccio de vita", 38.0, "food", "Felii fine de vita, parmezan, rucola, lamaie.", "🥩"),
    ("a3", "Salata Caprese", 28.0, "food", "Mozzarella di bufala, rosii coapte, busuioc proaspat.", "🧀"),
    ("a4", "Platou de branzeturi", 65.0, "food", "Selectie de 5 branzeturi italiene cu miere si nuci.", "🧀"),
    ("a5", "Calamari fritti", 42.0, "food", "Inele de calamar in crusta crocanta, sos aioli.", "🦑"),
    ("a6", "Supa minestrone", 24.0, "food", "Supa traditionala cu legume si paste mici.", "🍲"),

    # Salate
    ("s1", "Salata Caesar cu pui", 36.0, "food", "Salata romana, pui la gratar, crutoane, parmezan.", "🥗"),
    ("s2", "Salata greceasca", 32.0, "food", "Rosii, castraveti, masline, feta, oregano.", "🥗"),
    ("s3", "Salata cu somon afumat", 44.0, "food", "Mix verdeturi, somon afumat, avocado, citrice.", "🥗"),

    # Pizza
    ("p1", "Margherita", 32.0, "food", "Sos rosii San Marzano, mozzarella fior di latte, busuioc.", "🍕"),
    ("p2", "Quattro Formaggi", 42.0, "food", "Mozzarella, gorgonzola, parmezan, taleggio.", "🍕"),
    ("p3", "Pizza Diavola", 38.0, "food", "Salam picant, mozzarella, ardei iuti.", "🍕"),
    ("p4", "Prosciutto e Funghi", 40.0, "food", "Sunca de Parma, ciuperci proaspete, mozzarella.", "🍕"),
    ("p5", "Capricciosa", 41.0, "food", "Sunca, ciuperci, anghinare, masline negre.", "🍕"),
    ("p6", "Pizza Tartufo", 52.0, "food", "Crema de trufe, mozzarella, rucola, parmezan.", "🍕"),

    # Paste
    ("pa1", "Carbonara", 36.0, "food", "Spaghetti, guanciale, oua, pecorino, piper.", "🍝"),
    ("pa2", "Pesto Genovese", 32.0, "food", "Trofie, pesto de busuioc, pin, parmezan.", "🍝"),
    ("pa3", "Lasagna Bolognese", 38.0, "food", "Strat dupa strat: ragu, bechamel, parmezan.", "🍝"),
    ("pa4", "Penne Arrabbiata", 30.0, "food", "Sos picant de rosii, usturoi, ardei iute.", "🍝"),
    ("pa5", "Tagliatelle al Tartufo", 58.0, "food", "Paste proaspete cu unt si trufe negre.", "🍝"),
    ("pa6", "Risotto ai Funghi Porcini", 46.0, "food", "Orez Carnaroli, ciuperci porcini, parmezan.", "🍚"),

    # Feluri principale
    ("f1", "Muschi de vita la gratar", 89.0, "food", "300g cu sos demi-glace si cartofi rustici.", "🥩"),
    ("f2", "Somon la cuptor", 64.0, "food", "Somon norvegian, lamaie, ierburi, legume.", "🐟"),
    ("f3", "Piept de pui la gratar", 42.0, "food", "Marinat in ierburi, garnitura de legume.", "🍗"),
    ("f4", "Osso Buco", 78.0, "food", "Specialitate milaneza cu gremolata si polenta.", "🍖"),
    ("f5", "Saltimbocca alla Romana", 56.0, "food", "Vitel cu prosciutto si salvie, sos de vin.", "🍖"),

    # Deserturi
    ("d1", "Tiramisu", 24.0, "food", "Reteta clasica: mascarpone, cafea, savoiardi, cacao.", "🍰"),
    ("d2", "Panna Cotta", 22.0, "food", "Crema fina de smantana cu coulis de fructe de padure.", "🍮"),
    ("d3", "Gelato (3 cupe)", 26.0, "food", "Inghetata artizanala - 3 sortimente la alegere.", "🍨"),
    ("d4", "Cannoli Siciliani", 28.0, "food", "Tuburi crocante umplute cu crema de ricotta.", "🥐"),
    ("d5", "Profiterol", 26.0, "food", "Choux umplute cu crema, ciocolata calda.", "🍫"),

    # Bauturi
    ("b1", "Espresso", 10.0, "drink", "Boabe 100% Arabica, prajite artizanal.", "☕"),
    ("b2", "Cappuccino", 14.0, "drink", "Espresso cu lapte spumat catifelat.", "☕"),
    ("b3", "Vin rosu (pahar)", 22.0, "drink", "Selectie din podgorii italiene si romanesti.", "🍷"),
    ("b4", "Vin alb (pahar)", 22.0, "drink", "Pinot Grigio sau Sauvignon Blanc.", "🥂"),
    ("b5", "Aperol Spritz", 26.0, "drink", "Aperol, Prosecco, sifon, felie de portocala.", "🍹"),
    ("b6", "Limonada de casa", 16.0, "drink", "Lamaie proaspata, menta, miere.", "🍋"),
    ("b7", "Suc proaspat de portocale", 14.0, "drink", "100% storcit pe loc.", "🍊"),
    ("b8", "Apa minerala", 8.0, "drink", "Plata sau minerala, 0.5L.", "💧"),
]

PRODUCTS = {pid: ProductFactory.create(t, id=pid, name=n, price=pr, description=d, image=emo)
            for (pid, n, pr, t, d, emo) in RAW}

CATEGORIES = [
    ("Antreuri",       ["a1","a2","a3","a4","a5","a6"]),
    ("Salate",         ["s1","s2","s3"]),
    ("Pizza",          ["p1","p2","p3","p4","p5","p6"]),
    ("Paste & Risotto",["pa1","pa2","pa3","pa4","pa5","pa6"]),
    ("Feluri principale",["f1","f2","f3","f4","f5"]),
    ("Deserturi",      ["d1","d2","d3","d4","d5"]),
    ("Bauturi",        ["b1","b2","b3","b4","b5","b6","b7","b8"]),
]

def build_composite_menu():
    """COMPOSITE: meniul ca arbore."""
    root = MenuCategory("Casa Bella - Meniu Complet")
    for cname, ids in CATEGORIES:
        cat = MenuCategory(cname)
        for pid in ids: cat.add(MenuLeaf(PRODUCTS[pid]))
        root.add(cat)
    return root
