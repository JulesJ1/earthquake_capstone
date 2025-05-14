from filters import filter_magnitude, filter_type

"""
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
    mock_engine2 = mocker.patch('app.filters.create_connection')
    mock_engine2.return_value = 'test'
    fetch_data()
    mock_engine.assert_called_once_with(mock_engine2)



def test_display_live_data(mocker):
    mock_button = mocker.patch(
        'app.filters.st.sidebar.button',
        return_value=True
        )
    mocker.patch('app.filters.fetch_data', return_value='dummy')

    display_live_data()
    mock_button.assert_called_once_with(label='Show live data')
"""


def test_filter_magnitude(mocker):
    mock_slider = mocker.patch('app.filters.st.sidebar.slider')
    filter_magnitude()
    mock_slider.assert_called_once_with(
        label='filter minimum magnitude',
        min_value=0.0,
        max_value=9.5,
        key='mag_filter'
    )


def test_filter_type(mocker):
    test_options = ['typeA', 'typeB']
    mock_pills = mocker.patch('app.filters.st.sidebar.pills')
    filter_type(test_options)
    mock_pills.assert_called_once_with(
        'Type',
        test_options,
        selection_mode='single',
        default=test_options[0],
        key='type_filter'
        )


"""
def test_filter_date(mocker):
    start_value = datetime.now() - timedelta(hours=6)
    mock_date = mocker.patch('app.filters.st.sidebar.date_input')
    mock_time = mocker.patch('app.filters.st.sidebar.time_input')

    filter_date()
    mock_date.assert_called_once_with('start date',start_value)
    mock_time.assert_called_once_with('start time',start_value)

"""
