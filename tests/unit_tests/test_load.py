import pytest
import pandas as pd
from unittest.mock import MagicMock, patch
from etl.load.load import load_data, table_exists, insert_data


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'id': ['1', '2'],
        'magnitude': [2.5, 3.1],
        'location': ['A', 'B'],
        'time': [pd.Timestamp('2025-01-01'), pd.Timestamp('2025-01-02')],
        'type': ['earthquake', 'earthquake'],
        'longitude': [10.0, 20.0],
        'latitude': [50.0, 60.0],
        'depth': [5.0, 10.0],
        'closestLocation': ['A', 'B'],
        'apisource': ['usgs', 'esmc']
    })


def test_table_exists_true():
    # Arrange
    engine = MagicMock()
    metadata = MagicMock()

    # Assert
    metadata.tables.keys.return_value = ['schema.table']

    # Act
    assert table_exists(engine, metadata, ['table', 'schema']) is True


def test_table_exists_false():
    # Arrange
    engine = MagicMock()
    metadata = MagicMock()

    # Act
    metadata.tables.keys.return_value = []

    # Assert
    assert table_exists(engine, metadata, ['table', 'schema']) is False


@patch('etl.load.load.create_table')
@patch('etl.load.load.table_exists', return_value=False)
@patch('etl.load.load.insert_data')
@patch('etl.load.load.create_db_engine')
@patch('etl.load.load.load_db_config', return_value={
    'target_database': {'table': 'table', 'schema': 'schema'}})
def test_load_data_creates_table(mock_config,
                                 mock_engine,
                                 mock_insert,
                                 mock_exists,
                                 mock_create,
                                 sample_data):
    # Assert
    load_data(sample_data)

    # Act
    mock_create.assert_called()


@patch('etl.load.load.pd.read_sql_table')
@patch('etl.load.load.create_db_engine')
def test_insert_data_inserts_new_records(mock_engine,
                                         mock_read_sql,
                                         sample_data):
    # Arrange
    mock_read_sql.return_value = pd.DataFrame({'id': ['1']})
    engine = MagicMock()
    table_details = ['table', 'schema']

    # Assert
    with patch('etl.load.load.pd.DataFrame.to_sql') as mock_to_sql:
        insert_data(sample_data, engine, table_details)
        # Act
        mock_to_sql.assert_called_once()


@patch('etl.load.load.pd.read_sql_table', side_effect=Exception("DB error"))
def test_insert_data_handles_sqlalchemy_error(mock_read_sql, sample_data):
    # Arrange
    engine = MagicMock()
    table_details = ['table', 'schema']
    with pytest.raises(Exception):
        insert_data(sample_data, engine, table_details)
