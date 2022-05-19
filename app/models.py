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

from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects import registry
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
registry.register("spanner", "google.cloud.sqlalchemy_spanner", "SpannerDialect")


class Users(Base):
    __tablename__ = "users"

    user_id = Column("user_id", String(36), primary_key=True, nullable=False)
    name = Column("name", String(256), nullable=False)
    created_at = Column("created_at", DateTime, default=datetime.now(), nullable=False)
    # Because Cloud Spanner emulator does not infer null of Datatime, needs to set dummy value even if just creation
    updated_at = Column("updated_at", DateTime, default=datetime.fromtimestamp(0), onupdate=datetime.now(),
                        nullable=False)


class Scores(Base):
    __tablename__ = "scores"
    __table_args__ = {
        'spanner_interleave_in': 'users',
        'spanner_interleave_on_delete_cascade': True
    }

    user_id = Column("user_id", String(36), primary_key=True, nullable=False)
    score_id = Column("score_id", String(36), primary_key=True, nullable=False)
    score = Column("score", Integer, nullable=False, index=True)
    created_at = Column("created_at", DateTime, default=datetime.now(), nullable=False)
    # Because Cloud Spanner emulator does not infer null of Datatime, needs to set dummy value even if just creation
    updated_at = Column("updated_at", DateTime, default=datetime.fromtimestamp(0), onupdate=datetime.now(),
                        nullable=False)


Scores.__table__.add_is_dependent_on(Users.__table__)
