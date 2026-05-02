from fastapi import APIRouter

from schemas import User

router = APIRouter(prefix="/validation", tags=["Validation"])


# валидация полей пользователя
@router.post("/users")
def create_validated_user(user: User):
    return {"message": "User accepted", "user": user.model_dump()}
