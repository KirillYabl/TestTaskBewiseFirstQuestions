import datetime
import logging
import typing
import uuid

import aiohttp
import fastapi
import sqlalchemy.orm
import sqlalchemy.exc
import uvicorn

import data_models
import db_models
import jservice_api
import exceptions

app = fastapi.FastAPI()
logger = logging.getLogger(__name__)


def query_logger(query_id: uuid.UUID, message: str, function: typing.Callable):
    """Add :query_id: to logger message for understanding, with which query there was a problem"""
    function(f"{query_id}| {message}")


@app.post("/")
async def index(
        questions_num: data_models.RandomQuestionsCount,
        db_session: sqlalchemy.orm.Session = fastapi.Depends(db_models.get_session)
) -> list[dict[str, typing.Any]]:
    unique_api_question_ids = db_models.Question.get_unique_values_by_column(
        session=db_session,
        column_name="api_question_id"
    )
    query_id = uuid.uuid4()

    query_logger(query_id, f"start to handle index, questions_num={questions_num.questions_num}", logger.info)
    questions_to_add = []
    made_queries = 0
    async with aiohttp.ClientSession() as aiohttp_session:
        while len(questions_to_add) < questions_num.questions_num:
            if made_queries == data_models.settings.search_questions_queries_limit:
                query_logger(query_id, "the limit of queries to find questions overflowed", logger.warning)
                raise exceptions.QueriesLimitException

            need_questions_num = questions_num.questions_num - len(questions_to_add)  # acts like greedy algorithm
            query_logger(
                query_id,
                f"api query number {made_queries + 1}, try to find {need_questions_num} questions",
                logger.debug
            )
            # no need to handle errors, because these is key functionality and errors in these functionality means 500
            questions = await jservice_api.get_random_questions(aiohttp_session, need_questions_num)
            not_in_db_questions = [question for question in questions if question["id"] not in unique_api_question_ids]
            questions_to_add += not_in_db_questions[:need_questions_num]
            made_queries += 1

    query_logger(query_id, "questions found, serialize to db", logger.debug)
    created_at = datetime.datetime.now(tz=datetime.timezone.utc)
    db_questions = [
        db_models.Question(
            api_question_id=question["id"],
            question=question["question"],
            answer=question["answer"],
            api_created_at=datetime.datetime.strptime(
                question["created_at"],
                data_models.settings.jservice_api_date_format
            ),
            created_at=created_at,
        )
        for question
        in questions_to_add
    ]

    query_logger(query_id, "questions serialized, searching previous question", logger.debug)
    previous_questions = db_models.Question.get_previous_questions(session=db_session)

    query_logger(
        query_id,
        f"found {len(previous_questions)} previous questions, try to save serialized questions",
        logger.debug
    )
    try:
        db_session.bulk_save_objects(db_questions)
        db_session.commit()
        query_logger(query_id, "successful: questions saved", logger.debug)
    except sqlalchemy.exc.IntegrityError:
        db_session.rollback()
        query_logger(query_id, "unsuccessful: can't save questions", logger.debug)
        raise exceptions.CannotSaveQuestionsError

    return previous_questions


def main():
    logging.basicConfig(level=data_models.settings.logging_level)
    uvicorn.run(app)


if __name__ == '__main__':
    main()
