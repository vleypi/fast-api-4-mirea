from fastapi import APIRouter, HTTPException, Response

from schemas import UserIn, UserOut

router = APIRouter(prefix="/users", tags=["Users"])

db: dict[int, dict] = {}
_next_id = 0


# генерация нового id
def next_user_id() -> int:
    global _next_id
    _next_id += 1
    return _next_id


# создание нового юзера в памяти
@router.post("", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    user_id = next_user_id()
    db[user_id] = user.model_dump()
    return {"id": user_id, **db[user_id]}


# получаем юзера по id
@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, **db[user_id]}


# удаляем юзера
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int):
    if db.pop(user_id, None) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)
