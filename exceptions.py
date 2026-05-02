from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from schemas import ErrorResponse


class InsufficientStock(Exception):
    def __init__(self, requested, available):
        self.requested = requested
        self.available = available


class ItemNotFound(Exception):
    def __init__(self, item_id):
        self.item_id = item_id


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(InsufficientStock)
    async def insufficient_stock_handler(request: Request, exc: InsufficientStock):
        print(f"[InsufficientStock] requested={exc.requested}, available={exc.available}")
        body = ErrorResponse(
            error="insufficient_stock",
            detail=f"Requested {exc.requested}, available {exc.available}",
        )
        return JSONResponse(status_code=409, content=body.model_dump())

    @app.exception_handler(ItemNotFound)
    async def item_not_found_handler(request: Request, exc: ItemNotFound):
        print(f"[ItemNotFound] id={exc.item_id}")
        body = ErrorResponse(
            error="item_not_found",
            detail=f"Item with id {exc.item_id} does not exist",
        )
        return JSONResponse(status_code=404, content=body.model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        issues = []
        for err in exc.errors():
            field = ".".join(str(p) for p in err["loc"][1:])
            issues.append({"field": field, "message": err["msg"]})
        return JSONResponse(
            status_code=422,
            content={"error": "validation_failed", "issues": issues},
        )
