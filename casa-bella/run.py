"""Punct de intrare — rulează cu: python run.py"""
from app import create_app

if __name__ == "__main__":
    app = create_app()
    print("\n  Casa Bella → http://127.0.0.1:5000")
    print("  Admin demo: admin@casabella.md / admin123\n")
    app.run(debug=True, host="127.0.0.1", port=5000)
