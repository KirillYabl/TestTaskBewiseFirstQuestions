import enum
import logging

import pydantic


class RandomQuestionsCount(pydantic.BaseModel):
    questions_num: pydantic.conint(ge=1, le=100)


class Settings(pydantic.BaseSettings):
    search_questions_queries_limit: pydantic.conint(gt=0) = 10
    jservice_api_date_format: str = "%Y-%m-%dT%H:%M:%S.%f%z"
    logging_level: pydantic.conint(ge=0, le=5) = 2

    @pydantic.validator("logging_level", always=True)
    def transform_int_to_level(cls, v):
        int_to_level = {
            0: logging.NOTSET,
            1: logging.DEBUG,
            2: logging.INFO,
            3: logging.WARNING,
            4: logging.ERROR,
            5: logging.CRITICAL,
        }
        return int_to_level[v]

    class Config:
        env_file = '.env'


settings = Settings()
