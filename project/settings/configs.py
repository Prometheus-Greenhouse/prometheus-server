import os
from typing import List

import cx_Oracle
from pydantic import BaseSettings, Field


class ApplicationSettings(BaseSettings):
    version: str = Field("1.0.0")
    project_name: str = Field("PROMETHEUS - Server", env="PROJECT_NAME")
    description: str = Field("Minerva description")
    secret_key: str = Field("", env="SECRET_KEY")
    debug: bool = Field(True, env="DEBUG")
    allowed_hosts: List = Field(["*"], env="ALLOWED_HOSTS")
    LANGUAGE_CODE: str = Field('en-us')
    TIME_ZONE: str = Field('UTC')
    USE_I18N: bool = Field(True)
    USE_TZ: bool = Field(True)


class DatabaseSettings(BaseSettings):
    class Oracle(BaseSettings):
        host: str = Field("localhost", env="ORACLE_HOST")
        port: str = Field("1521", env="ORACLE_PORT")
        username: str = Field("minerva", env="ORACLE_USER")
        password: str = Field("123456", env="ORACLE_PASSWORD")
        service_name: str = Field("xe", env="ORACLE_DATABASE")

        @property
        def url(self) -> str:
            return f"oracle+cx_oracle://{self.username}:{self.password}@{self.host}:{self.port}/?service_name={self.service_name}"

    class PostGreSQL(BaseSettings):
        host: str = Field("ec2-52-7-179-175.compute-1.amazonaws.com", env="PG_HOST")
        port: str = Field("5432", env="PG_PORT")
        username: str = Field("aktysraxvqsrmk", env="PG_USER")
        password: str = Field("9c0649b013fe86c45876f634e4018379e5792fd21029b8edb50ccdee8621be83", env="PG_PASSWORD")
        database: str = Field("dneo5evuqaq2e", env="PG_DATABASE")

        @property
        def url(self) -> str:
            return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}/{self.database}"

    oracle: Oracle = Oracle()
    postgres: PostGreSQL = PostGreSQL()


APPLICATION = ApplicationSettings()

DATABASES = DatabaseSettings()

# cx_Oracle.init_oracle_client(lib_dir=os.getenv("LD_LIBRARY_PATH"))
