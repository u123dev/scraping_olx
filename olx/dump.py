from pathlib import Path

from celery import shared_task
from sqlalchemy import inspect, text
from datetime import datetime

from olx import db


def dump_table(engine, dump_fname=None, batch_size=10000, table_name="ads", ddl=True):
    """
    Dump table in database
    :param engine:
    :param dump_fname: dump file name
    :param batch_size: defaults to 100000
    :param table_name: defaults to "ads"
    :param ddl: write DDL, defaults to True
    :return:
    """
    if dump_fname is None:
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        dump_fname = f"dump_{current_time}.sql"

    # path:  root/dumps
    project_root = Path(__file__).parents[1] / "dumps"
    dump_fname = project_root / dump_fname

    inspector = inspect(engine)  # meta data
    columns = inspector.get_columns(table_name)  # table columns

    with open(dump_fname, "w", encoding="utf-8") as dump_file:
        if ddl:
            # DDL SQL table creation
            create_table_sql = f"CREATE TABLE {table_name} (\n"
            create_table_sql += ",\n".join([f"    {col['name']} {str(col['type'])}" for col in columns])
            create_table_sql += "\n);\n\n"
            dump_file.write(create_table_sql)

        offset = 0
        while True:
            query = text(f"SELECT * FROM {table_name} LIMIT {batch_size} OFFSET {offset}")

            with engine.connect() as connection:
                result = connection.execute(query)
                rows = result.fetchall()
                if not rows:
                    break

                #  SQL insert row
                for row in rows:
                    insert_sql = f"INSERT INTO {table_name} ({', '.join([col['name'] for col in columns])}) "
                    insert_sql += f"VALUES ({', '.join([repr(val) for val in row])});\n"
                    dump_file.write(insert_sql)

                offset += batch_size

    print(f"Dump table {table_name} saved into {dump_fname}")


@shared_task(queue="dumping_queue")
def dump_start():
    engine = db.db_connect()
    dump_table(engine)


if __name__ == "__main__":
    dump_start()
