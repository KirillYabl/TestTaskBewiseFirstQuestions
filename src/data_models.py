import logging
import typing

import pydantic


class RandomQuestionsCount(pydantic.BaseModel):
    questions_num: pydantic.conint(ge=1, le=100)


class Settings(pydantic.BaseSettings):
    search_questions_queries_limit: pydantic.conint(gt=0) = 10
    jservice_api_date_format: str = "%Y-%m-%dT%H:%M:%S.%f%z"
    logging_level: pydantic.conint(ge=0, le=5) = 2
    postgres_password: str = "DB_PASSWORD"
    postgres_user: str = "USER_NAME"
    postgres_host: str = "db"
    postgres_port: int = 5432
    db_string: typing.Optional[str] = None

    @pydantic.validator("logging_level", always=True)
    def transform_int_to_level(cls, v: int) -> int:
        int_to_level = {
            0: logging.NOTSET,
            1: logging.DEBUG,
            2: logging.INFO,
            3: logging.WARNING,
            4: logging.ERROR,
            5: logging.CRITICAL,
        }
        return int_to_level[v]

    @pydantic.validator("db_string", always=True)
    def build_db_string(cls, v: typing.Optional[str], values: dict[str, typing.Any]) -> str:
        if v is not None:
            return v

        postgres_password = values["postgres_password"]
        postgres_user = values["postgres_user"]
        postgres_host = values["postgres_host"]
        postgres_port = values["postgres_port"]
        v = f"postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/postgres"
        return v

    class Config:
        env_file = '.env'


settings = Settings()
