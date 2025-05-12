from sqlalchemy import text
from utils.db_utils import get_time
import pandas as pd
from utils.logging_utils import setup_logger
import logging

logger = setup_logger(__name__, "database_query.log", level=logging.DEBUG)

def retrieve_live_data(connection):
    time = get_time(5)
    df = pd.read_sql(
        "SELECT id, time, magnitude, longitude, latitude, location, type, depth " 
            "FROM c12de.jj_capstone " 
            f"WHERE time BETWEEN '{time[0]}' AND '{time[1]}' "
            "ORDER BY time DESC;" ,
            con=connection

    )
    logger.setLevel(logging.INFO)
    logger.info("Queried database for live data")
    return df

def retrieve_historical_data(connection,start,end):
    df = pd.read_sql(
        "SELECT id, time, magnitude, longitude, latitude, location, type, depth " 
            "FROM c12de.jj_capstone " 
            f"WHERE time BETWEEN '{start}' AND '{end}' "
            "ORDER BY time DESC;" ,
            con=connection

    )
    logger.setLevel(logging.INFO)
    logger.info("Queried database for live data")
    return df

def retrieve_min_mag(connection):
    time = get_time(5)
    query = "SELECT id, time, magnitude, longitude, latitude " \
            "FROM c12de.jj_capstone " \
            f"WHERE time BETWEEN '{time[0]}' AND '{time[1]}';"
    output = connection.execute(text(query))
    print(output.fetchall())