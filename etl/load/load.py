import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, VARCHAR, INT, DateTime
from sqlalchemy.exc import InvalidRequestError,OperationalError, IntegrityError, SQLAlchemyError, DataError, DatabaseError
from utils.logging_utils import setup_logger
import logging
from config.db_config import load_db_config
from psycopg2.errors import UniqueViolation

logger = setup_logger(__name__, "database_query.log", level=logging.DEBUG)
TABLE_NAME = 'earthquakes'


def load_data(data: pd.DataFrame):
    db_details = load_db_config()['target_database']
    meta = MetaData()

    engine = create_connection(db_details)

    if not table_exists(engine, meta):
        create_table(engine, meta)

    insert_data(data, engine)


def create_connection(connection_details: dict):
    try:
        engine = create_engine(f'postgresql://{connection_details['user']}:{connection_details['password']}@{connection_details['host']}:{connection_details['port']}/{connection_details['dbname']}')
        return engine
    except OperationalError as e:
        print(f'Cannot connect: {e}')
    except DatabaseError as e:
        print(f'DatabaseError: {e}')
    except SQLAlchemyError as e:
        print(f'Could not conncet: {e}')


def table_exists(engine, metadata) -> bool:
    metadata.reflect(bind=engine)
    my_table = metadata.tables
    return TABLE_NAME in my_table


def create_table(engine, metadata):
    try:
        print('creating new table')
        Table(
            TABLE_NAME,
            metadata,
            Column('id', VARCHAR(20), primary_key=True),
            Column('magnitude', INT),
            Column('location', VARCHAR(70)),
            Column('time', DateTime),
            Column('type', VARCHAR(30)),
            Column('longitude', INT),
            Column('latitude', INT),
            Column('depth', INT),
            Column('closestLocation', VARCHAR(70))
            )

        metadata.create_all(engine)
    except OperationalError as e:
        print(f'Table already exists: {e}')
    except InvalidRequestError as e:
        print(f'Table already exists: {e}')


def insert_data(data: pd.DataFrame, engine):
    try:
        current_table = pd.read_sql_table('earthquakes', con=engine)
        data = data[~data['id'].isin(current_table['id'])]
        print(data)
        data.to_sql(TABLE_NAME, engine, if_exists='append', index=False)

    except IntegrityError as e:
        print(f'Unique violation error, duplicate primary keys in data: {e}')

    except DataError as e:
        print(F'Data error: {e}')

    except SQLAlchemyError as e:
        print(f'{e}')

