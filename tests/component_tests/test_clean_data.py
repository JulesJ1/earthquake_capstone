import pandas as pd
from etl.transform.transform import clean_earthquake_data
from pathlib import Path

coordinates = [[-122.609169006348, 38.4456672668457, 3.46000003814697],
               [-69.9926, -19.6387, 60.403],
               [-152.235, 61.2755, 3.76],
               [-176.31, 51.5375, 32.7],
               [-121.758, 46.855333333333334, 1.62],
               [-135.0243, 55.5028, 10],
               [-153.1314, 59.5105, 106.2],
               [-117.1221667, 33.6783333, 2.31],
               [-104.428, 31.66, 5.5872],
               [-122.80899810791, 38.7508316040039, 14.7799997329712]
               ]


def test_clean_data(mocker):
    # Arrange
    base_path = Path(__file__).parent
    unclean_data = pd.read_csv(base_path / '../testdata/unclean_test_data.csv')
    clean_data = pd.read_csv(base_path / '../testdata/clean_test_data.csv')
    unclean_data = pd.DataFrame(unclean_data).iloc[:, 1:-1]
    coord_df = pd.Series(coordinates, name='geometry.coordinates')
    unclean_data = pd.merge(
        unclean_data,
        coord_df,
        right_index=True,
        left_index=True
        )
    # Act
    transformed_dataframe = clean_earthquake_data(unclean_data)

    clean_dataframe = pd.DataFrame(clean_data).iloc[:, 1:]

    # Assert
    pd.testing.assert_frame_equal(clean_dataframe, transformed_dataframe)
