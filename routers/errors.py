from fastapi import APIRouter

from exceptions import InsufficientStock, ItemNotFound

router = APIRouter(prefix="/errors")

# словарь товаров и остатков на складе
stock = {1: 5, 2: 0}


# покупаем товар или кидаем ошибку
@router.post("/buy/{item_id}")
def buy_item(item_id: int, quantity: int = 1):
    if item_id not in stock:
        raise ItemNotFound(item_id)
    if stock[item_id] < quantity:
        raise InsufficientStock(quantity, stock[item_id])
    stock[item_id] -= quantity
    return {"message": f"Bought {quantity} of item {item_id}", "remaining": stock[item_id]}


# получаем товар по id
@router.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in stock:
        raise ItemNotFound(item_id)
    return {"id": item_id, "stock": stock[item_id]}
