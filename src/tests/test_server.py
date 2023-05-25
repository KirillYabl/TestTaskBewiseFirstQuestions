import datetime
import random
import typing
import unittest.mock

import fastapi.testclient

import jservice_api
import data_models
import exceptions
import server


class AsyncMagicMock(unittest.mock.MagicMock):
    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


def return_any_question() -> dict[str, typing.Any]:
    question_id = random.randint(1, 2 ** 31)
    created_at = datetime.datetime.now(tz=datetime.timezone.utc).strftime(data_models.settings.jservice_api_date_format)
    return {
        "id": question_id,
        "question": f"Question {question_id}",
        "answer": f"Answer {question_id}",
        "created_at": created_at,
    }


def return_n_questions(n: int) -> list[dict[str, typing.Any]]:
    return [return_any_question() for _ in range(n)]


def test_index_successful():
    with fastapi.testclient.TestClient(server.app) as fastapi_client:
        first_query_questions_num = 3
        second_query_questions_num = 5

        first_return = return_n_questions(first_query_questions_num)
        jservice_api.get_random_questions = AsyncMagicMock(return_value=first_return)
        response = fastapi_client.post("/", json={"questions_num": first_query_questions_num})
        assert response.status_code == 200
        assert response.json() == []

        jservice_api.get_random_questions = AsyncMagicMock(return_value=return_n_questions(second_query_questions_num))
        response = fastapi_client.post("/", json={"questions_num": second_query_questions_num})
        assert response.status_code == 200
        assert len(response.json()) == first_query_questions_num


def test_index_error_api_return_exist_questions():
    with fastapi.testclient.TestClient(server.app) as fastapi_client:
        query_questions_num = 3
        query_return = return_n_questions(query_questions_num)

        jservice_api.get_random_questions = AsyncMagicMock(return_value=query_return)
        response = fastapi_client.post("/", json={"questions_num": query_questions_num})
        assert response.status_code == 200
        assert response.json() == []

        jservice_api.get_random_questions = AsyncMagicMock(return_value=query_return)
        response = fastapi_client.post("/", json={"questions_num": query_questions_num})
        assert response.status_code == 500
        assert response.json()["detail"] == exceptions.QueriesLimitException().detail
