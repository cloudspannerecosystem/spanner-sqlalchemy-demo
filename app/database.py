from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PROJECT_ID = environ["PROJECT_ID"]
INSTANCE_NAME = environ["INSTANCE_NAME"]
DATABASE_NAME = environ["DATABASE_NAME"]

# DATABASE_URL = "spanner:///projects/" + PROJECT_ID + "/instances/" + INSTANCE_NAME + "/databases/" + DATABASE_NAME
DATABASE_URL = "spanner:///projects/your-project-id/instances/demo/databases/ranking"

engine = create_engine(DATABASE_URL)

# TODO: resolve an error | `staleness` option can't be changed while a transaction is in progress.
# https://github.com/googleapis/python-spanner-sqlalchemy/issues/192
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


