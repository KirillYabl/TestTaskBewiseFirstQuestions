import typing

import fastapi


class QueriesLimitException(fastapi.HTTPException):
    def __init__(
            self,
            status_code: int = 500,
            detail: typing.Any = "Couldn't find so many new questions",
            headers: typing.Optional[dict[str, typing.Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class CannotSaveQuestionsError(fastapi.HTTPException):
    def __init__(
            self,
            status_code: int = 500,
            detail: typing.Any = "Unable to save as many new questions, please try reducing the number of questions or check back later",
            headers: typing.Optional[dict[str, typing.Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
