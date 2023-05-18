import pydantic


class RandomQuestionsCount(pydantic.BaseModel):
    questions_num: pydantic.conint(ge=1, le=100)


class Settings(pydantic.BaseSettings):
    search_questions_queries_limit: pydantic.conint(gt=0) = 10
    jservice_api_date_format: str = "%Y-%m-%dT%H:%M:%S.%f%z"

    class Config:
        env_file = '.env'


settings = Settings()
