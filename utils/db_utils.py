import logging
from sqlalchemy import create_engine
from utils.logging_utils import setup_logger
from sqlalchemy.exc import (
                            OperationalError,
                            SQLAlchemyError,
                            DatabaseError
                            )
from datetime import datetime, timezone, timedelta

logger = setup_logger(__name__, "database_query.log", level=logging.DEBUG)


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


def create_connection(engine):
    try:
        conn = engine.connect()
        return conn
    except OperationalError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Operational error: {e}")
        print(f'Operational error: {e}')


def get_time(delta: int) -> list[str, str]:
    endtime = datetime.now(timezone.utc)
    starttime = (
            endtime - timedelta(hours=delta)
        ).strftime('%Y-%m-%dT%H:%M:%S')
    endtime = endtime.strftime('%Y-%m-%dT%H:%M:%S')
    return [starttime, endtime]
