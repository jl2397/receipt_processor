from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from receipts.views import router as receipt_router

app = FastAPI()
app.include_router(router=receipt_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [f"{err['type']} at {' -> '.join(map(str, err['loc']))}: {err['msg']}" for err in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": errors}
    )

@app.get("/health")
def get_health():
    return {"status": "ok"}