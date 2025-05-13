from filters import fetch_data


def test_filter(mocker):
    # Arrange
    mock_connection = {
        'TARGET_DB_NAME': 'test_target_db',
        'TARGET_DB_USER': 'test_user',
        'TARGET_DB_PASSWORD': 'test_password',
        'TARGET_DB_HOST': 'localhost',
        'TARGET_DB_PORT': '5432',
        'TARGET_DB_TABLE': 'test_table',
        'TARGET_DB_SCHEMA': 'test_schema'
    }
    # Act
    mock_engine = mocker.patch('app.filters.retrieve_live_data')

    # Assert
    fetch_data()
    mock_engine.assert_called_once_with(mock_connection)
