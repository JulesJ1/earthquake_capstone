import pandas as pd
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    VARCHAR,
    DateTime,
    NUMERIC
    )
from sqlalchemy.exc import (
    InvalidRequestError,
    OperationalError,
    IntegrityError,
    SQLAlchemyError,
    DataError,
    # DatabaseError
    )

from utils.logging_utils import setup_logger
import logging
from config.db_config import load_db_config
from utils.db_utils import create_db_engine


logger = setup_logger(__name__, "database_query.log", level=logging.DEBUG)


def load_data(data: pd.DataFrame):
    db_details = load_db_config()['target_database']
    table_details = [db_details['table'], db_details['schema']]

    meta = MetaData()

    engine = create_db_engine(db_details)

    if not table_exists(engine, meta, table_details):
        create_table(engine, meta, table_details)

    insert_data(data, engine, table_details)


def table_exists(engine, metadata, table_details) -> bool:
    metadata.reflect(bind=engine, schema=table_details[1])
    my_table = metadata.tables.keys()
    return table_details[1]+'.'+table_details[0] in my_table


def create_table(engine, metadata, table_details):
    try:
        Table(
            table_details[0],
            metadata,
            Column('id', VARCHAR(20), primary_key=True),
            Column('magnitude', NUMERIC),
            Column('location', VARCHAR(70)),
            Column('time', DateTime),
            Column('type', VARCHAR(30)),
            Column('longitude', NUMERIC),
            Column('latitude', NUMERIC),
            Column('depth', NUMERIC),
            Column('closestLocation', VARCHAR(70)),
            schema=table_details[1]
            )

        metadata.create_all(engine)
        logger.setLevel(logging.INFO)
        logger.info(f"Successfully created table: {table_details[0]}")

    except OperationalError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Operational error, table already exists: {e}")
        print(f'Operational error, table already exists: {e}')
    except InvalidRequestError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Invalid request: {e}")
        print(f'Invalid request: {e}')


def insert_data(data: pd.DataFrame, engine, table_details):
    try:
        # Read table from database
        current_table = pd.read_sql_table(
            table_details[0],
            con=engine,
            schema=table_details[1]
            )
        # Return the difference between the new data and data in table
        data = data[~data['id'].isin(current_table['id'])]
        number_of_records = data.shape[0]
        # Insert data into the table
        data.to_sql(
            table_details[0],
            engine,
            if_exists='append',
            index=False,
            schema=table_details[1]
            )
        logger.setLevel(logging.INFO)
        logger.info(f"Successfully inserted {number_of_records} "
                    f"row(s) of data into {table_details[0]} table")

    except IntegrityError as e:
        logger.setLevel(logging.ERROR)
        logger.error("Unique violation error, "
                     f"duplicate primary keys in data: {e}")
        print(f'Unique violation error, duplicate primary keys in data: {e}')

    except DataError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Data error: {e}")
        print(F'Data error: {e}')

    except SQLAlchemyError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"SQLAlchemy error: {e}")
        print(f'SQLAlchemy error: {e}')
