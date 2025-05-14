from filters import fetch_data


def test_filter(mocker):
    # Arrange

    # Act
    mock_engine = mocker.patch('app.filters.retrieve_live_data')

    # Assert
    mock_engine2 = mocker.patch('app.filters.create_connection')
    mock_engine2.return_value = 'test'
    fetch_data()
    mock_engine.assert_called_once_with(mock_engine2)
