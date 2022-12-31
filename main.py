from dotenv import load_dotenv

load_dotenv(".env")

from apps.iot_service import IotService
from apps.decisiontree.services import DecisionTreeService

from fastapi import FastAPI, Depends
import uvicorn

from database.models import Greenhouse, DecisionTree
from project.utils.const import Constants

import argparse

from sqlalchemy.orm import Session

from database.base import Session_
from project.settings.logger import init_logging

__version__ = "0.0.1"
init_logging()

app = FastAPI(
    docs_url="/",
    redoc_url="/redoc"
)
iot_service = IotService()


@app.on_event("startup")
async def startup():
    s: Session = Session_()
    gh = s.query(Greenhouse).filter(Greenhouse.is_default == True).first()
    Constants.greenhouse_id = gh.id
    s.close()
    iot_service.run()


@app.on_event("shutdown")
async def shutdown():
    iot_service.stop()


@app.post("/decision/tree")
async def post_decision_tree(
        decision_tree_service: DecisionTreeService = Depends(DecisionTreeService)
):
    z = decision_tree_service.create_tree()
    decision_tree_service.session.add(
        DecisionTree(tree=z.print_tree())
    )


@app.post("/decision")
async def make_decision(
        sensor_data: float,
        decision_tree_service: DecisionTreeService = Depends(DecisionTreeService)
):
    return {"data": decision_tree_service.make_decision(sensor_data)}


if __name__ == "__main__":
    version = "0.0.1"
    banner = f"""
         _     ___  ____
        | |   / _ \\/ ___|
        | |  | | | \\___ \\
        | |__| |_| |___) |
        |_____\\___/|____/
         =========|_|==============
          :: Prometheus ::                (v{version})
        """
    parser = argparse.ArgumentParser(usage=banner)
    parser.add_argument("-e", "--env-file", help="Set env file, default=all")
    # parser.add_argument("-v", "--version", action="store_true", help="print the version number and exit")
    parser.add_argument("-v", "--version", action="store_true", help="print the version number and exit")
    args = parser.parse_args()
    if args.version:
        print(__version__)
    uvicorn.run("main:app", host="127.0.0.1", port=8009, env_file=".env")
