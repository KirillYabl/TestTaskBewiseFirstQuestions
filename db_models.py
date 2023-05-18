import datetime
import functools

import sqlalchemy.orm

db_string = "sqlite+pysqlite:///db.sqlite3"

engine = sqlalchemy.create_engine(db_string)
SessionLocal = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = sqlalchemy.orm.declarative_base()


class Database:
    def __init__(self):
        self._session = SessionLocal()

    def get_session(self):
        return self._session


db = Database()


def get_session():
    try:
        db_session = db.get_session()
        yield db_session
    finally:
        db_session.close()


class Question(base):
    __tablename__ = "Question"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def get_unique_values_by_column(cls, session, column_name):
        return set(
            record.api_question_id
            for record
            in session.query(getattr(cls, column_name)).distinct()
        )

    @classmethod
    def get_previous_questions(cls, session):
        max_created_at_subquery = session.query(sqlalchemy.func.max(cls.created_at)).scalar_subquery()
        return [
            record.as_dict()
            for record
            in session.query(cls).filter(
                cls.created_at == max_created_at_subquery
            )
        ]

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
        index=True,
        nullable=False
    )


if __name__ == '__main__':
    base.metadata.create_all(engine, checkfirst=True)  # Explicit is better than implicit.
