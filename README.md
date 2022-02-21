# Cloud Spanner + SQLAlchemy demo 
This is a demo application for [Cloud Spanner SQLAlchemy ORM](https://github.com/googleapis/python-spanner-sqlalchemy).  
A simple ranking API for gaming use cases.

## Building blocks
* Language: Python3 
* Framework: FastAPI
* ORM: SQLAlchemy
* Migration tool: Alembic
* Server: Cloud Run
* DB: Cloud Spanner
* CI/CD: Cloud Build


## TODO
- Implement PUT/DELETE [DONE]
- Resolve "stalenesss error" [Waiting for v1.1.0 available from PyPI]
- Adapt Alembic [DONE]
- Implement unit tests w/ Cloud Spanner emulator [DONE]
- Containerization
- Deploy to Cloud Run
- Set up Cloud Build


# For who want to play with this code
## 1. How to install dependencies 
```shell
$ git clone https://github.com/kazshinohara/spanner-sqlalchemy-demo
$ cd spanner-sqlalchemy-demo
$ poetry install
```

## 2. How to do DB Migration to Cloud Spanner
Create Cloud Spanner instance and database
```shell
$ gcloud spanner instances create demo --config=regional-asia-northeast1 --description="demo" --nodes=1
$ gcloud spanner databases create ranking --instance=demo
```

DB Migration
```shell
$ export GOOGLE_APPLICATION_CREDENTIALS=""
$ export PROJECT_ID=""
$ export INSTANCE_ID=""
$ export DATABASE_ID=""
$ cd spanner-sqlalchemy-demo/app
$ export PYTHONPATH=.
$ poetry run alembic revision --autogenerate -m "Initial migration"
$ poetry run alembic upgrade head
```

## 3. How to start API server
```shell
$ export GOOGLE_APPLICATION_CREDENTIALS=""
$ export PROJECT_ID=""
$ export INSTANCE_ID=""
$ export DATABASE_ID=""
$ cd spanner-sqlalchemy-demo
$ poetry run uvicorn app.main:app --reload
$ open http://127.0.0.1:8000/docs
```

## 3. How to run unit test at your local machine
Run Cloud Spanner emulator
```shell
$ docker run -p 9010:9010 -p 9020:9020 gcr.io/cloud-spanner-emulator/emulator
```

Set up Cloud Spanner emulator
```shell
$ gcloud config configurations create emulator
$ gcloud config set auth/disable_credentials true
$ gcloud config set project your-project-id
$ gcloud config set api_endpoint_overrides/spanner http://localhost:9020/
$ gcloud spanner instances create demo --config=emulator-config --description="demo" --nodes=1
$ gcloud spanner databases create ranking --instance=demo
```

Set up environment variables which are needed for the unit test
```shell
$ export PROJECT_ID=""
$ export INSTANCE_ID=""
$ export DATABASE_ID=""
$ export SPANNER_EMULATOR_HOST=localhost:9010
```

Run the unit test
```shell
$ cd spanner-sqlalchemy-demo/tests
$ pytest
```