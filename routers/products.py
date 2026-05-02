from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Product
from schemas import ProductRead

router = APIRouter(prefix="/products", tags=["Products"])


# отдаём все товары из базы
@router.get("", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
