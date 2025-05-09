import pandas as pd
from etl.transform.transform import clean_earthquake_data


def test_clean_data():
    # Arrange
    unclean_data = pd.read_csv('../testdata/unclean_test_data.csv')
    clean_data = pd.read_csv('../testdata/clean_test_data.csv')
    # Act
    transformed_dataframe = clean_earthquake_data(unclean_data)
    # Assert
    assert clean_data == transformed_dataframe
