import pandas as pd
import requests
import logging
from utils.logging_utils import setup_logger


class BadRequestError(Exception):
    pass


class RequestTimeoutError(Exception):
    pass


class GeneralException(Exception):
    pass


logger = setup_logger(__name__, "database.log", level=logging.DEBUG)


def extract_api(starttime, endttime):
    try:
        query = 'https://earthquake.usgs.gov/fdsnws/event/1/query'\
            f'?format=geojson&starttime={starttime}&endtime={endttime}'

        data = requests.get(query, timeout=60)
        data.raise_for_status()
        df = pd.json_normalize(data.json(), 'features')
        logger.setLevel(logging.INFO)
        logger.info("Successfully extracted data")
        return df
    except requests.exceptions.HTTPError as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"HTTP error when extracting data: {e}")
        raise BadRequestError(f'HTTP error: {e}')
    except requests.exceptions.ReadTimeout as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Timeout error when extracting data: {e}")
        raise RequestTimeoutError(f'Timed out: {e}')
    except Exception as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"unable to retrieve data: {e}")
        raise GeneralException(f'unable to retrieve data: {e}')
