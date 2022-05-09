from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PROJECT_ID = environ.get("PROJECT_ID")
INSTANCE_ID = environ.get("INSTANCE_ID")
DATABASE_ID = environ.get("DATABASE_ID")
SQL_LOG = environ.get("SQL_LOG")

if SQL_LOG:
    import logging

    logging.basicConfig()
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

DATABASE_URL = "spanner:///projects/" + PROJECT_ID + "/instances/" + INSTANCE_ID + "/databases/" + DATABASE_ID
engine = create_engine(DATABASE_URL)

# TODO: resolve an error | `staleness` option can't be changed while a transaction is in progress.
# https://github.com/googleapis/python-spanner-sqlalchemy/issues/192
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
