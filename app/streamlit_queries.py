from utils.db_utils import get_time
import pandas as pd
from utils.logging_utils import setup_logger
import logging
import time
from sqlalchemy.exc import DatabaseError, TimeoutError


logger = setup_logger(__name__, "database_query.log", level=logging.DEBUG)


def time_query(starttime, endtime):
    return "SELECT id, time, magnitude, longitude,"\
        " latitude, location, type, depth, apisource "\
        "FROM c12de.jj_capstone "\
        f"WHERE time BETWEEN '{starttime}' AND '{endtime}' "\
        "ORDER BY time DESC;"


def retrieve_live_data(connection):
    try:
        timestamp = get_time(5)
        start = time.time()
        df = pd.read_sql(
            time_query(timestamp[0], timestamp[1]),
            con=connection
        )
        end = time.time()
        logger.setLevel(logging.INFO)
        logger.info("Queried database for live data,"
                    f" the query took {round(end-start, 3)}s to run!")
        return df

    except TimeoutError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Timeout error: {e}")
        print(f'Timeout error: {e}')

    except DatabaseError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Database error: {e}")
        print(f'Database error: {e}')


def retrieve_historical_data(connection, starttime, endtime):
    try:
        start = time.time()
        df = pd.read_sql(
            time_query(starttime, endtime),
            con=connection
        )
        end = time.time()
        logger.setLevel(logging.INFO)
        logger.info("Queried database for historical data,"
                    f" the query took {round(end-start, 3)}s to run!")
        return df

    except TimeoutError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Timeout error: {e}")
        print(f'Timeout error: {e}')

    except DatabaseError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Database error: {e}")
        print(f'Database error: {e}')
