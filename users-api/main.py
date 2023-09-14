from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn

from users import users_router
from employees import employees_router
from s3 import s3_router

from config import PRODUCTION

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.options("/{url}")
async def handle_options(url):
    return JSONResponse({"ok": True}, headers={"Access-Control-Allow-Headers": "*"})


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, err) -> JSONResponse:
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(
        status_code=500,
        content={"message": f"{base_error_message}. Detail: {str(err)}"},
    )


app.include_router(users_router, tags=["Users"])
app.include_router(employees_router, tags=["Employees"])
app.include_router(s3_router, tags=["Storage"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=not PRODUCTION)
