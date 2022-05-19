# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import environ

from sqlalchemy import create_engine
from sqlalchemy.dialects import registry
from sqlalchemy.orm import sessionmaker

PROJECT_ID = environ.get("PROJECT_ID")
INSTANCE_ID = environ.get("INSTANCE_ID")
DATABASE_ID = environ.get("DATABASE_ID")
SQL_LOG = environ.get("SQL_LOG")

if SQL_LOG:
    import logging

    logging.basicConfig()
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

registry.register("spanner", "google.cloud.sqlalchemy_spanner", "SpannerDialect")
DATABASE_URL = "spanner:///projects/" + PROJECT_ID + "/instances/" + INSTANCE_ID + "/databases/" + DATABASE_ID
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
