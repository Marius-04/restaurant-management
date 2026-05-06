# Casa Bella — Flask + 13 Design Patterns

Aplicație web pentru un restaurant italian, cu autentificare, coș, checkout,
panou de admin și **13 design patterns** integrate în logica reală.

## Distribuție patterns (cerință academică)

| Categorie       | # | Pattern           | Fișier                                  |
|-----------------|---|-------------------|------------------------------------------|
| **Creational**  | 1 | Factory Method    | `patterns/p01_factory_method.py`         |
|                 | 2 | Abstract Factory  | `patterns/p02_abstract_factory.py`       |
|                 | 3 | Builder           | `patterns/p03_builder.py`                |
|                 | 4 | Prototype         | `patterns/p04_prototype.py`              |
| **Structural**  | 5 | Adapter           | `patterns/p05_adapter.py`                |
|                 | 6 | Decorator         | `patterns/p06_decorator.py`              |
|                 | 7 | Composite         | `patterns/p07_composite.py`              |
|                 | 8 | Facade            | `patterns/p08_facade.py`                 |
| **Behavioral**  | 9 | Strategy          | `patterns/p09_strategy.py`               |
|                 |10 | Observer          | `patterns/p10_observer.py`               |
|                 |11 | Command           | `patterns/p11_command.py`                |
|                 |12 | State             | `patterns/p12_state.py`                  |
| **Obligatoriu** |13 | **Singleton**     | `patterns/p13_singleton.py`              |

## Rulare locală

```bash
unzip casa-bella.zip
cd casa-bella
pip install -r requirements.txt
python run.py
```

Apoi deschide http://127.0.0.1:5000

**Cont admin demo:** `admin@casabella.md` / `admin123`

## Funcționalități

- Pagină principală cu recomandări
- Meniu cu 38 de produse organizate în 8 categorii (cu poze)
- Înregistrare / login (parolă SHA-256 + salt)
- Coș de cumpărături în sesiune
- Checkout cu 3 metode de plată (Strategy + Adapter)
- "Comenzile mele" pentru utilizatori
- Panou Admin cu schimbare status (State + Command + Undo)
- Pagina /patterns cu explicații + arborele Composite live

## Teste

```bash
python tests/test_patterns.py
```
