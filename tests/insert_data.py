#!/usr/bin/env python

import asyncio
import random
import uuid
from datetime import datetime
from os import environ

import names
from google.cloud import spanner


INSTANCE_ID = environ.get("INSTANCE_ID")
DATABASE_ID = environ.get("DATABASE_ID")
user_id_list = []


def insert_users_data(instance_id, database_id):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.batch() as batch:
        batch.insert(
            table="users",
            columns=("user_id", "name", "created_at", "updated_at"),
            values=[(str(uuid.uuid4()),
                     names.get_full_name(),
                     datetime.now(),
                     datetime.fromtimestamp(0)) for i in range(0, 100)
                    ],
        )

    print("Inserted user data.")


def read_users(instance_id, database_id):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.snapshot(multi_use=True) as snapshot:
        # Read using SQL.
        results = snapshot.execute_sql(
            "SELECT user_id FROM users"
        )
        for row in results:
            user_id_list.append(*row)

    print("Read users")


async def insert_scores_data(instance_id, database_id):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.batch() as batch:
        batch.insert(
            table="scores",
            columns=("score_id", "user_id", "score", "created_at", "updated_at"),
            values=[(str(uuid.uuid4()),
                     random.choice(user_id_list),
                     random.randint(0, 10000),
                     datetime.now(),
                     datetime.fromtimestamp(0)) for x in range(0, 100)
                    ]
        )


async def parallel_insert_scores_data():
    tasks = [asyncio.create_task(insert_scores_data(INSTANCE_ID, DATABASE_ID)) for i in range(0, 100)]
    await asyncio.gather(*tasks)
    print("Inserted score data.")


if __name__ == "__main__":
    insert_users_data(INSTANCE_ID, DATABASE_ID)
    read_users(INSTANCE_ID, DATABASE_ID)
    asyncio.run(parallel_insert_scores_data())
