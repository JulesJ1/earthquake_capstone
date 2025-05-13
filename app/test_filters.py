from filters import fetch_data


def test_filter(mocker):
    # Arrange
    mock_connection = {
        'TARGET_DB_NAME': 'test_target_db',
        'TARGET_DB_USER': 'test_user',
        'TARGET_DB_PASSWORD': 'test_password',
        'TARGET_DB_HOST': 'localhost',
        'TARGET_DB_PORT': '5432'
    }
    # Act
    mock_engine = mocker.patch('app.filters.fetch_data.retrieve_live_data')

    # Assert
    fetch_data()
    mock_engine.assert_called_once_with(mock_connection)
