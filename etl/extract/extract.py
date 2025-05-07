import pandas as pd
import requests


def extract_api(starttime, endttime):
    try:
        query = f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={starttime}&endtime={endttime}'
        data = requests.get(query)
        df = pd.json_normalize(data.json(), 'features')
        return df

    except Exception as e:
        print(f'unable to retrieve data: {e}')
