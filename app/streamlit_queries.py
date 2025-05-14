from utils.db_utils import get_time
import pandas as pd
from utils.logging_utils import setup_logger
import logging
import time

logger = setup_logger(__name__, "database_query.log", level=logging.DEBUG)


def time_query(starttime, endtime):
    return "SELECT id, time, magnitude, longitude,"\
        " latitude, location, type, depth "\
        "FROM c12de.jj_capstone "\
        f"WHERE time BETWEEN '{starttime}' AND '{endtime}' "\
        "ORDER BY time DESC;"


def retrieve_live_data(connection):
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


def retrieve_historical_data(connection, starttime, endtime):
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
