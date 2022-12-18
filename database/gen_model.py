import os

from dotenv import load_dotenv

load_dotenv("../.env")

from sqlalchemy.pool import QueuePool

from sqlalchemy import (
    create_engine
)

from typing import List

from fastapi import Body
from sqlacodegen.codegen import CodeGenerator
from sqlalchemy import MetaData

from database.base import engine


def generate_model(file, tables: List[str] = Body("all")):
    metadata = MetaData(bind=engine, schema="prometheus")
    metadata.reflect(only=None if tables == "all" else tables)
    outfile = open(file, "w", encoding="utf-8")
    generator = CodeGenerator(metadata)
    generator.render(outfile)

#
if __name__ == "__main__":
    generate_model("model.py", "all")
