import datetime
import functools

import sqlalchemy.orm

db_string = "sqlite+pysqlite:///db.sqlite3"

db = sqlalchemy.create_engine(db_string)
base = sqlalchemy.orm.declarative_base()


class Question(base):
    __tablename__ = "Question"

    question_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.Sequence("question_id_seq", start=1),
        primary_key=True
    )  # it's better to have self primary key for the case if something happened with API
    api_question_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, index=True, nullable=False)
    # limit based on few thousands requests to API with some extra space
    question = sqlalchemy.Column(sqlalchemy.String(1000), nullable=False)
    answer = sqlalchemy.Column(sqlalchemy.String(500), nullable=False)
    api_created_at = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=False)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime(timezone=True),
        default=functools.partial(datetime.datetime.now, tz=datetime.timezone.utc),
        index=True, nullable=False
    )


if __name__ == '__main__':
    base.metadata.create_all(db, checkfirst=True)  # Explicit is better than implicit.
