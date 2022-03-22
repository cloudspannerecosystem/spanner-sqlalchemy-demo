FROM python:3.10-slim-buster as builder
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10-slim-buster as runner
WORKDIR /opt
COPY --from=builder /tmp/requirements.txt /opt/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /opt/requirements.txt
COPY ./app /opt/app
CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
