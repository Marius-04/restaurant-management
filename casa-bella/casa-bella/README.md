# Casa Bella - Aplicatie Web cu 13 Design Patterns

Aplicatie web Flask in Python care implementeaza un restaurant online cu **toate cele 13 design patterns** integrate functional.

## Cerinte
- Python 3.10+

## Instalare si rulare

```bash
pip install -r requirements.txt
python run.py
```

Apoi deschide in browser: **http://127.0.0.1:5000**

## Structura

```
casa-bella-flask/
├── run.py                  # Punct de intrare
├── requirements.txt
├── app/
│   ├── __init__.py         # Aplicatia Flask + rute
│   ├── data.py             # 35+ produse + meniu Composite
│   └── services.py         # Logica de business (foloseste patterns)
├── patterns/               # CELE 13 PATTERNS
│   ├── p01_factory.py
│   ├── p02_builder.py
│   ├── p03_singleton.py
│   ├── p04_adapter.py
│   ├── p05_composite.py
│   ├── p06_decorator.py
│   ├── p07_strategy.py
│   ├── p08_observer.py
│   ├── p09_command.py
│   ├── p10_state.py
│   ├── p11_mediator.py
│   ├── p12_visitor.py
│   └── p13_memento.py
├── templates/              # HTML (Jinja2)
├── static/css/style.css
└── tests/test_patterns.py
```

## Pagini web

| Ruta            | Descriere                                                |
|-----------------|----------------------------------------------------------|
| `/`             | Acasa - hero + recomandari (Factory)                     |
| `/menu`         | Meniu complet - 35+ produse, 7 categorii (Composite)     |
| `/cart`         | Cos cu Undo (Memento)                                    |
| `/checkout`     | Plaseaza comanda (Builder + Strategy + Adapter + Decorator + Observer + Mediator) |
| `/admin`        | Comenzi, schimbare status (State + Command), export (Visitor) |
| `/patterns`     | Documentatie + arborele Composite live                   |

## Cele 13 patterns - unde sunt folosite

| # | Pattern        | Fisier                  | Folosit in                       |
|---|----------------|-------------------------|----------------------------------|
| 1 | Factory Method | p01_factory.py          | data.py - creeaza produsele     |
| 2 | Builder        | p02_builder.py          | services.checkout                |
| 3 | Singleton      | p03_singleton.py        | AppConfig (configurare globala)  |
| 4 | Adapter        | p04_adapter.py          | Stripe/PayPal/Cash               |
| 5 | Composite      | p05_composite.py        | Arborele meniului                |
| 6 | Decorator      | p06_decorator.py        | Notificari (UI+Email+SMS)        |
| 7 | Strategy       | p07_strategy.py         | Selectare gateway plata          |
| 8 | Observer       | p08_observer.py         | order_bus - log evenimente       |
| 9 | Command        | p09_command.py          | Undo in admin                    |
| 10| State          | p10_state.py            | Tranzitii status comanda         |
| 11| Mediator       | p11_mediator.py         | Bucatarie ↔ Livrare              |
| 12| Visitor        | p12_visitor.py          | Export JSON/CSV/XML              |
| 13| Memento        | p13_memento.py          | Undo cos                         |

## Teste

```bash
python -m unittest tests.test_patterns -v
```
