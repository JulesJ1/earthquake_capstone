import logging
import pandas as pd
from utils.logging_utils import setup_logger
from .transform_functions import closest_location

logger = setup_logger(__name__, "database.log", level=logging.DEBUG)


def transform_esmc_data(earthquakes: pd.DataFrame) -> pd.DataFrame:
    columns = [
            "geometry.type", "properties.lastupdate",
            "properties.unid", "properties.auth",
            "properties.evtype", "geometry.coordinates",
            "properties.source_catalog", "properties.source_id",
            "type", "properties.magtype"
        ]
    earthquakes = earthquakes.drop(columns=columns)
    earthquakes = earthquakes.dropna(
        subset=['properties.mag']
        ).reset_index(drop=True)

    names = {
        'properties.mag': 'magnitude',
        'properties.flynn_region': 'location',
        'properties.time': 'time',
        'properties.lat': 'latitude',
        'properties.lon': 'longitude',
        'properties.depth': 'depth'
    }

    earthquakes = earthquakes.rename(columns=names)

    earthquakes['time'] = pd.to_datetime(
                            earthquakes['time'],
                        ).dt.floor('s').dt.strftime('%Y-%m-%d %H:%M:%S')

    earthquakes['location'] = earthquakes['location'].str.title()

    earthquakes['closestLocation'] = earthquakes[
        'location'
        ].apply(closest_location)

    earthquakes['location'] = earthquakes[
        'location'
        ].apply(lambda x: x.split(',')[-1])

    earthquakes["type"] = "earthquake"
    earthquakes["apisource"] = "esmc"

    logger.setLevel(logging.INFO)
    logger.info("Successfully transformed esmc data")

    return earthquakes
