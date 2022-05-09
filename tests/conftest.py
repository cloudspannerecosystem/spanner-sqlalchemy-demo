from os import environ

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm.session import close_all_sessions

from app.main import app, get_db
from app.models import Base

PROJECT_ID = environ["PROJECT_ID"]
INSTANCE_ID = environ["INSTANCE_ID"]
DATABASE_ID = environ["DATABASE_ID"]


class TestingSession(Session):
    def commit(self):
        # remove all data for next test
        self.flush()
        self.expire_all()


@pytest.fixture(scope="function")
def test_db():
    # 1. SetUp
    engine = create_engine("spanner:///projects/" + PROJECT_ID + "/instances/"
                           + INSTANCE_ID + "/databases/" + DATABASE_ID)
    Base.metadata.create_all(bind=engine)

    TestSessionLocal = sessionmaker(class_=TestingSession, autocommit=False, autoflush=False, bind=engine)

    db = TestSessionLocal()

    # Replace get_db() at app.main with the following func
    # https://fastapi.tiangolo.com/advanced/testing-dependencies/
    def get_db_for_testing():
        try:
            yield db
            db.commit()
        except SQLAlchemyError as e:
            assert e is not None
            db.rollback()

    app.dependency_overrides[get_db] = get_db_for_testing

    # 2. Execute test cases
    yield db

    # 3. TearDown
    db.rollback()
    close_all_sessions()
    engine.dispose()
