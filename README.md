# Cloud Spanner + SQLAlchemy demo 
[![pytest & flake8](https://github.com/kazshinohara/spanner-sqlalchemy-demo/actions/workflows/pytest_flake8.yaml/badge.svg)](https://github.com/kazshinohara/spanner-sqlalchemy-demo/actions/workflows/pytest_flake8.yaml) 
[![docker_build](https://github.com/kazshinohara/spanner-sqlalchemy-demo/actions/workflows/docker_build.yaml/badge.svg)](https://github.com/kazshinohara/spanner-sqlalchemy-demo/actions/workflows/docker_build.yaml) 

This is a demo application for [Cloud Spanner SQLAlchemy ORM](https://github.com/googleapis/python-spanner-sqlalchemy).  
A simple ranking API for gaming use cases.

## Building blocks
* Language: [Python 3](https://docs.python.org/3/)
* Python package and virtualenv tool: [Poetry](https://github.com/python-poetry/poetry)
* Framework: [FastAPI](https://fastapi.tiangolo.com/)
* ORM: [SQLAlchemy](https://www.sqlalchemy.org/)
* Migration tool: [Alembic](https://alembic.sqlalchemy.org/en/latest/)
* Server: [Cloud Run](https://cloud.google.com/run/)
* DB: [Cloud Spanner](https://cloud.google.com/spanner/)
* Container registry: [Artifact Registry](https://cloud.google.com/artifact-registry/)
* CI/CD: [GitHub Actions](https://github.co.jp/features/actions) 

# For who want to play with this code
## 1. install dependencies to your local machine
```shell
git clone https://github.com/kazshinohara/spanner-sqlalchemy-demo
cd spanner-sqlalchemy-demo
poetry install
```

## 2. Setup Cloud Spanner and DB Migration
Set environment variables which are needed for the following steps.
```shell
export PROJECT_ID=""
export INSTANCE_ID=""
export DATABASE_ID=""
export SA_NAME=""
export SA_KEY_NAME=""
```

Create a service account for this demo.
```shell
gcloud iam service-accounts create ${SA_NAME}
```

Assign role to the service account. 
```shell
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/spanner.databaseAdmin"
```

Download the key file to your local machine.
```shell
gcloud iam service-accounts keys create ${SA_KEY_NAME} \
--iam-account=${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
```

Set your key file location as an environment variable.
```shell
export GOOGLE_APPLICATION_CREDENTIALS=""
```

Create Cloud Spanner instance and database.
```shell
gcloud spanner instances create ${INSTANCE_ID} --config=regional-asia-northeast1 --description="demo" --nodes=1
gcloud spanner databases create ${DATABASE_ID} --instance=${INSTANCE_ID}
```

DB migration, Alembic uses your service account's credential to access Cloud Spanner.
```shell
cd spanner-sqlalchemy-demo/app
poetry run alembic revision --autogenerate -m "Initial migration"
poetry run alembic upgrade head
```

## 3. Start API server at your local machine
*Note: The following steps need environment variables which are set at Section 2.*

```shell
cd spanner-sqlalchemy-demo
poetry run uvicorn app.main:app --reload
open http://127.0.0.1:8000/
```

## 4. Run unit test at your local machine
*Note: The following steps need environment variables which are set at Section 2.*

Run Cloud Spanner emulator.
```shell
docker run -p 9010:9010 -p 9020:9020 gcr.io/cloud-spanner-emulator/emulator
```

Set up Cloud Spanner emulator.
```shell
cd spanner-sqlalchemy-demo/tests
chmod u+x spanner_emulator_setup.sh
./spanner_emulator_setup.sh
```

Set environment variables which are needed for the following steps.
```shell
export SPANNER_EMULATOR_HOST=localhost:9010
export K_SERVICE=spanner-sqlalchemy-demo
export K_REVISION=spanner-sqlalchemy-demo-00001-thx
```

Run the unit test.
```shell
cd spanner-sqlalchemy-demo/tests
poetry run pytest
```

## 5. Create the container image and deploy to Cloud Run
*Note: The following steps need environment variables which are set at Section 2.*

Set an environment variable which are needed for the following steps.  
Please make sure that you have a docker image repo at Artifact Registry.
```shell
export REPOSITORY_NAME=""
```

Build a container image.
```shell
cd spanner-sqlalchemy-demo 
docker build -t asia-northeast1-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/spanner-sqlalchemy-demo:1.0.0 .
```

Push the image to Artifact Registry
```shell
cd spanner-sqlalchemy-demo 
docker push asia-northeast1-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/spanner-sqlalchemy-demo:1.0.0
```

Deploy the container image to Cloud Run.
```shell
gcloud run deploy spanner-sqlalchemy-demo \
--image asia-northeast1-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY_NAME}/spanner-sqlalchemy-demo:1.0.0 \
--allow-unauthenticated \
--set-env-vars=PROJECT_ID=${PROJECT_ID},INSTANCE_ID=${INSTANCE_ID},DATABASE_ID=${DATABASE_ID} \
--service-account=${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
--region=asia-northeast1
```