import pandas as pd


def split_coordinates_column(data: pd.DataFrame) -> pd.DataFrame:
    # Splits the geometry.coordinates column into 3 seperate columns
    coordinates = data['geometry.coordinates'].apply(pd.Series).round(2)
    coordinates.columns = ['longitude', 'latitude', 'depth']

    data.drop(columns=['geometry.coordinates'], inplace=True)
    data = pd.merge(
                    data,
                    coordinates,
                    left_index=True,
                    right_index=True
                )

    data['depth'] = data['depth'].fillna(10)
    data['magnitude'] = data['magnitude'].round(2)
    data['depth'] = data['depth'].round(2)

    return data


def closest_location(location: str) -> str:
    if ',' in location:
        return location.split(',')[0]

    return 'None'
