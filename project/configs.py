import os
from typing import List, Any

import requests
from loguru import logger
from pydantic import Field, BaseModel


class BaseConfig(BaseModel):
    __metadata__ = {}

    def __init__(self, **data: Any):
        super().__init__(**data)
        for name, info in self.__fields__.items():
            conf_key = info.field_info.extra.get("conf")
            if not conf_key:
                continue
            conf_value = self.__metadata__.get(conf_key)
            if conf_value is None:
                raise ValueError(f"Config not found: {conf_key}")
            self.__setattr__(name, self.parse_type(info.type_, conf_value))

    @staticmethod
    def parse_type(type_, value):
        return type_(value)


def init_config():
    config_uri = os.getenv("CONFIG_SOURCE", None)
    if not config_uri:
        raise ValueError("CONFIG_SOURCE is required")
    logger.info("Configs uri" + config_uri)
    res = requests.get(config_uri)
    if not res.ok:
        raise ValueError("Cannot load CONFIG_SOURCE" + res.text)
    source = res.json()["propertySources"][0]["source"]
    BaseConfig.__metadata__ = source
    logger.info(BaseConfig.__metadata__)


class ApplicationConfigs(BaseConfig):
    version: str = Field("1.0.0")
    project_name: str = Field("PROMETHEUS - Server")
    description: str = Field("Minerva description")
    secret_key: str = Field("", )
    debug: bool = Field(True, conf="debug")
    allowed_hosts: List = Field(["*"])
    LANGUAGE_CODE: str = Field('en-us')
    TIME_ZONE: str = Field('UTC')
    USE_I18N: bool = Field(True)
    USE_TZ: bool = Field(True)


class DatabaseConfigs(BaseConfig):
    class Oracle(BaseConfig):
        host: str = Field("127.0.0.1", conf="database.host")
        port: str = Field("1521", conf="database.port")
        username: str = Field("prometheus", conf="database.username")
        password: str = Field("123456", conf="database.password")
        service_name: str = Field("xe", conf="database.service")

        @property
        def url(self) -> str:
            return f"oracle+cx_oracle://{self.username}:{self.password}@{self.host}:{self.port}/?service_name={self.service_name}"

    # class PostGreSQL(BaseConfig):
    #     host: str = Field("ec2-52-7-179-175.compute-1.amazonaws.com", conf="PG_HOST")
    #     port: str = Field("5432", conf="PG_PORT")
    #     username: str = Field("aktysraxvqsrmk", conf="PG_USER")
    #     password: str = Field("9c0649b013fe86c45876f634e4018379e5792fd21029b8edb50ccdee8621be83", conf="PG_PASSWORD")
    #     database: str = Field("dneo5evuqaq2e", conf="PG_DATABASE")
    #
    #     @property
    #     def url(self) -> str:
    #         return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}/{self.database}"

    oracle: Oracle = Field(default_factory=Oracle)
    # postgres: PostGreSQL = PostGreSQL()


class BrokerConfigs(BaseConfig):
    host: str = Field("192.168.1.4", conf="broker.host")
    port: int = Field(1883, conf="broker.port")


init_config()
APPLICATION = ApplicationConfigs()
DATABASE = DatabaseConfigs()
BROKER = BrokerConfigs()

# cx_Oracle.init_oracle_client(lib_dir=os.getenv("LD_LIBRARY_PATH"))
