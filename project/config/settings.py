import os
from typing import List

import cx_Oracle
from pydantic import BaseSettings, Field


class ApplicationSettings(BaseSettings):
    version: str = Field("1.0.0")
    project_name: str = Field("MINERVA - Server", env="PROJECT_NAME")
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

    oracle: Oracle = Oracle()


APPLICATION = ApplicationSettings()

DATABASES = DatabaseSettings()

cx_Oracle.init_oracle_client(lib_dir=os.getenv("LD_LIBRARY_PATH"))
