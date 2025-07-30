import logging
import pandas as pd
from utils.logging_utils import setup_logger
from .transform_functions import split_coordinates_column, closest_location

logger = setup_logger(__name__, "database.log", level=logging.DEBUG)


def clean_earthquake_data(earthquakes: pd.DataFrame) -> pd.DataFrame:

    # Dropping and renaming columns
    standardised_locations = {
        'CA': 'California',
        'NV': 'Nevada',
        'MX': 'Mexico'
    }

    columns = [
        'properties.updated', 'properties.tz', 'properties.url',
        'properties.detail', 'properties.felt', 'properties.status',
        'properties.cdi', 'properties.mmi', 'properties.alert',
        'properties.tsunami', 'properties.sig', 'properties.net',
        'properties.code', 'properties.ids', 'type',
        'properties.sources', 'properties.types', 'properties.nst',
        'properties.dmin', 'properties.rms', 'properties.gap',
        'properties.magType', 'properties.title', 'geometry.type'
    ]
    earthquakes = earthquakes.drop(columns=columns)
    earthquakes = earthquakes.dropna(
        subset=['properties.mag']
        ).reset_index(drop=True)

    names = {
        'properties.type': 'type',
        'properties.mag': 'magnitude',
        'properties.place': 'location',
        'properties.time': 'time',
    }
    earthquakes = earthquakes.rename(columns=names)

    # Reformating time
    earthquakes['time'] = pd.to_datetime(
                            earthquakes['time'],
                            unit='ms'
                        ).dt.floor('s').dt.strftime('%Y-%m-%d %H:%M:%S')

    earthquakes = split_coordinates_column(earthquakes)

    # Splits the location into country/region and closest location
    earthquakes['closestLocation'] = earthquakes[
        'location'
        ].apply(closest_location)

    earthquakes['location'] = earthquakes[
        'location'
        ].apply(lambda x: x.split(',')[-1])

    earthquakes['location'] = earthquakes[
        'location'
        ].str.strip().replace(standardised_locations)

    logger.setLevel(logging.INFO)
    logger.info("Successfully transformed data")

    return earthquakes
