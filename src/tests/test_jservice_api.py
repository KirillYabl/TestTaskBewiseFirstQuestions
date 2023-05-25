import datetime

import aiohttp
import pytest

import jservice_api
import data_models


@pytest.mark.asyncio
async def test_get_random_questions():
    count = 5
    async with aiohttp.ClientSession() as session:
        questions = await jservice_api.get_random_questions(session, count)

    assert isinstance(questions, list)
    assert len(questions) == count

    for question in questions:
        assert isinstance(question, dict)
        assert "id" in question
        assert "question" in question
        assert "answer" in question
        assert "created_at" in question
        assert isinstance(question["id"], int)
        assert isinstance(question["question"], str)
        assert isinstance(question["answer"], str)
        assert isinstance(question["created_at"], str)
        datetime.datetime.strptime(
            question["created_at"],
            data_models.settings.jservice_api_date_format
        )
