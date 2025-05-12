import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, VARCHAR, DateTime, NUMERIC, schema
from sqlalchemy.exc import InvalidRequestError, OperationalError, IntegrityError, SQLAlchemyError, DataError, DatabaseError
from utils.logging_utils import setup_logger
import logging
from config.db_config import load_db_config


logger = setup_logger(__name__, "database_query.log", level=logging.DEBUG)
TABLE_NAME = 'jj_capstone'
SCHEMA_NAME = 'c12de'
#TABLE_NAME = 'test_types_3'
#SCHEMA_NAME = 'test'

def load_data(data: pd.DataFrame):
    db_details = load_db_config()['target_database']
    meta = MetaData()
    
    engine = create_db_engine(db_details)

    if not table_exists(engine, meta):
        create_table(engine, meta)

    insert_data(data, engine)


def create_db_engine(connection_details: dict):
    try:
        engine = create_engine(
                f'postgresql://{connection_details['user']}:'
                f'{connection_details['password']}@'
                f'{connection_details['host']}:'
                f'{connection_details['port']}/'
                f'{connection_details['dbname']}'
            )
        logger.setLevel(logging.INFO)
        logger.info("Successfully connected to the database")
        return engine
    except OperationalError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Operational error: {e}")
        print(f'Operational error: {e}')
    except DatabaseError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"DatabaseError: {e}")
        print(f'Database error: {e}')
    except SQLAlchemyError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Could not conncet to the database: {e}")
        print(f'Could not conncet to the database: {e}')


def table_exists(engine, metadata) -> bool:
    # metadata.clear()
    metadata.reflect(bind=engine, schema=SCHEMA_NAME)
    my_table = metadata.tables.keys()
    return SCHEMA_NAME+'.'+TABLE_NAME in my_table


def create_table(engine, metadata):
    try:
        Table(
            TABLE_NAME,
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
            schema=SCHEMA_NAME
            )

        metadata.create_all(engine)
        logger.setLevel(logging.INFO)
        logger.info(f"Successfully created table: {TABLE_NAME}")

    except OperationalError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Operational error, table already exists: {e}")
        print(f'Operational error, table already exists: {e}')
    except InvalidRequestError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Invalid request: {e}")
        print(f'Invalid request: {e}')


def insert_data(data: pd.DataFrame, engine):
    try:
        current_table = pd.read_sql_table(TABLE_NAME, con=engine, schema=SCHEMA_NAME)
        data = data[~data['id'].isin(current_table['id'])]
        number_of_records = data.shape[0]
        data.to_sql(TABLE_NAME, engine, if_exists='append', index=False, schema=SCHEMA_NAME)
        logger.setLevel(logging.INFO)
        logger.info(f"Successfully inserted {number_of_records} row(s) of data into {TABLE_NAME} table")

    except IntegrityError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Unique violation error, duplicate primary keys in data: {e}")
        print(f'Unique violation error, duplicate primary keys in data: {e}')

    except DataError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Data error: {e}")
        print(F'Data error: {e}')

    except SQLAlchemyError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"SQLAlchemy error: {e}")
        print(f'SQLAlchemy error: {e}')
