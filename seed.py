from database import SessionLocal
from models import Product


def seed():
    session = SessionLocal()
    try:
        if session.query(Product).count() > 0:
            print("products already seeded, skipping")
            return
        session.add_all([
            Product(title="Headphones", price=99.99, count=10, description="Over-ear wireless"),
            Product(title="Keyboard", price=149.50, count=5, description="Mechanical RGB"),
        ])
        session.commit()
        print("seeded 2 products")
    finally:
        session.close()

seed()
