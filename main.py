from fastapi import FastAPI

from exceptions import register_exception_handlers
from routers import errors, products, users, validation

app = FastAPI(title="kr4")

register_exception_handlers(app)

app.include_router(products.router)
app.include_router(errors.router)
app.include_router(validation.router)
app.include_router(users.router)
