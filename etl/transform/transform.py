import pandas as pd


def clean_earthquake_data(earthquakes: pd.DataFrame) -> pd.DataFrame:
    columns = [
        'properties.updated', 'properties.tz', 'properties.url', 'properties.detail',
        'properties.felt', 'properties.cdi', 'properties.mmi', 'properties.alert',
        'properties.status', 'properties.tsunami', 'properties.sig', 'properties.net',
        'properties.code', 'properties.ids', 'properties.sources', 'properties.types',
        'properties.nst', 'properties.dmin', 'properties.rms', 'properties.gap',
        'properties.magType', 'properties.title', 'geometry.type', 'type'
    ]
    earthquakes = earthquakes.drop(columns=columns)
    earthquakes = earthquakes.dropna(subset=['properties.mag'])

    names = {
        'properties.type':'type',
        'properties.mag':'magnitude',
        'properties.place':'location',
        'properties.time':'time',
    }
    earthquakes = earthquakes.rename(columns = names)

    earthquakes['properties.time'] = pd.to_datetime(earthquakes['properties.time'],unit='ms').dt.floor('S')

    earthquake_coordinates = earthquakes['geometry.coordinates'].apply(pd.Series).round(2)
    earthquake_coordinates.columns = ['longitude','latitude','depth']

    earthquakes.drop(columns=['geometry.coordinates'], inplace=True)
    earthquakes = pd.merge(earthquakes,earthquake_coordinates,left_index=True,right_index=True)

    earthquakes['nearestCity'] = earthquakes['location'].apply(nearest_city)

    earthquakes['location'] = earthquakes['location'].apply(lambda x: x.split(',')[-1])


def nearest_city(location: str) -> str:
    if ',' in location:
        return location.split(',')[0]
    
    return 'None'
