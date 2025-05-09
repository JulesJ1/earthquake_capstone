import pandas as pd
import requests


class BadRequestError(Exception):
    pass


class RequestTimeoutError(Exception):
    pass


class GeneralException(Exception):
    pass

def extract_api(starttime, endttime):
    try:
        query = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={starttime}&endtime={endttime}'
        data = requests.get(query, timeout=5)
        data.raise_for_status()
        df = pd.json_normalize(data.json(), 'features')
        return df
    except requests.exceptions.HTTPError as e:
        raise BadRequestError(f'HTTP error: {e}')
    except requests.exceptions.ReadTimeout as e:
        raise RequestTimeoutError(f'Timed out: {e}')
    except Exception as e:
        raise GeneralException(f'unable to retrieve data: {e}')
