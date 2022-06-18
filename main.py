import subprocess

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

# init_logging()
from apps.client.services import ClientService
from project.config.settings import APPLICATION

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


@app.on_event("startup")
async def setup():
    subprocess.Popen(["rm", "-r", "apps/client/services."])


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True, env_file=".env")
