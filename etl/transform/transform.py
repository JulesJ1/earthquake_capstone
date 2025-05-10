import pandas as pd


def clean_earthquake_data(earthquakes: pd.DataFrame) -> pd.DataFrame:
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
    earthquakes = earthquakes.dropna(subset=['properties.mag'])

    names = {
        'properties.type': 'type',
        'properties.mag': 'magnitude',
        'properties.place': 'location',
        'properties.time': 'time',
    }
    earthquakes = earthquakes.rename(columns=names)

    earthquakes['time'] = pd.to_datetime(earthquakes['time'], unit='ms').dt.floor('s').dt.strftime('%Y-%m-%d %H:%M:%S')

    earthquake_coordinates = earthquakes['geometry.coordinates'].apply(pd.Series).round(2)
    earthquake_coordinates.columns = ['longitude', 'latitude', 'depth']
    

    earthquakes.drop(columns=['geometry.coordinates'], inplace=True)
    earthquakes = pd.merge(
                    earthquakes, 
                    earthquake_coordinates, 
                    left_index=True, 
                    right_index=True
                )
    
    earthquakes['depth'] = earthquakes['depth'].fillna(10)

    earthquakes['closestLocation'] = earthquakes['location'].apply(closest_location)

    earthquakes['location'] = earthquakes['location'].apply(lambda x: x.split(',')[-1])
    earthquakes['location'] = earthquakes['location'].str.strip().replace(standardised_locations)

    return earthquakes


def closest_location(location: str) -> str:
    if ',' in location:
        return location.split(',')[0]
    
    return 'None'
