import datetime
import typing

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


@app.post("/")
async def index(
        questions_num: data_models.RandomQuestionsCount,
        db_session: sqlalchemy.orm.Session = fastapi.Depends(db_models.get_session)
) -> list[dict[str, typing.Any]]:
    unique_api_question_ids = db_models.Question.get_unique_values_by_column(
        session=db_session,
        column_name="api_question_id"
    )

    questions_to_add = []
    made_queries = 0
    async with aiohttp.ClientSession() as aiohttp_session:
        while len(questions_to_add) < questions_num.questions_num:
            if made_queries == data_models.settings.search_questions_queries_limit:
                raise exceptions.QueriesLimitException

            need_questions_num = questions_num.questions_num - len(questions_to_add)  # acts like greedy algorithm
            # no need to handle errors, because these is key functionality and errors in these functionality means 500
            questions = await jservice_api.get_random_questions(aiohttp_session, need_questions_num)
            not_in_db_questions = [question for question in questions if question["id"] not in unique_api_question_ids]
            questions_to_add += not_in_db_questions[:need_questions_num]
            made_queries += 1

    db_questions = [
        db_models.Question(
            api_question_id=question["id"],
            question=question["question"],
            answer=question["answer"],
            api_created_at=datetime.datetime.strptime(
                question["created_at"],
                data_models.settings.jservice_api_date_format
            ),
        )
        for question
        in questions_to_add
    ]

    previous_questions = db_models.Question.get_previous_questions(session=db_session)

    try:
        db_session.bulk_save_objects(db_questions)
        db_session.commit()
    except sqlalchemy.exc.IntegrityError:
        db_session.rollback()
        raise exceptions.CannotSaveQuestionsError

    return previous_questions


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
