import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from starlette.middleware.authentication import AuthenticationMiddleware

from apps.security.authentication.services import AuthenticationFilter
from project import router as main_router
from project.settings.configs import APPLICATION
from project.settings.logger import init_logging

init_logging()
app = FastAPI(
    title=APPLICATION.project_name,
    description=APPLICATION.description,
    debug=APPLICATION.debug,
    version=APPLICATION.version,
    docs_url="/",
    redoc_url="/redoc",
    default_response_class=ORJSONResponse
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=APPLICATION.allowed_hosts or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["POST", "GET"],
)

app.add_middleware(AuthenticationMiddleware, backend=AuthenticationFilter())


@app.on_event("startup")
async def setup():
    ...
    # subprocess.Popen(["rm", "-r", "apps/client/services."])


app.include_router(main_router.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True, env_file=".env")
