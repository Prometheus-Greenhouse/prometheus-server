import uvicorn
from fast_boot.exception import LOSException
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from apps.greenhouse.services import ClientService
from database.repositories.devices import DeviceRepository

app = FastAPI(
    docs_url="/",
    default_response_class=ORJSONResponse
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["POST", "GET"],
)


@app.exception_handler(LOSException)
async def los_http_exception_handler(request: Request, exc: LOSException):
    return JSONResponse(
        content={
            "errors": LOSException.arrow_error_pipeline(exc.get_detail()),
        },
        status_code=exc.status_code,
        headers=exc.headers
    )


@app.exception_handler(RequestValidationError)
async def except_custom(request: Request, exc: RequestValidationError):  # noqa
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"errors": jsonable_encoder(
            LOSException.arrow_error_pipeline(LOSException.errors_pipeline(exc.errors()))
        )}
    )


@app.get(
    path="/4/up"
)
async def publish():
    service = ClientService()
    repos = DeviceRepository()

    service.get_client().publish(
        repos.get_esp8266().topic,
        "1"
    )


@app.get(
    path="/4/down"
)
async def publish():
    service = ClientService()
    repos = DeviceRepository()

    service.get_client().publish(
        repos.get_esp8266().topic,
        "0"
    )


@app.get(
    path="/5/up"
)
async def publish():
    service = ClientService()
    repos = DeviceRepository()

    service.get_client().publish(
        "ESP8266/5",
        "1"
    )


@app.get(
    path="/5/down"
)
async def publish():
    service = ClientService()
    repos = DeviceRepository()

    service.get_client().publish(
        "ESP8266/5",
        "0"
    )


if __name__ == "__main__":
    uvicorn.run('app.main:app', host="127.0.0.1", port=8001, reload=True, env_file="../.env")
