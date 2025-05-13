from utils.db_utils import create_db_engine, get_time, create_connection
from datetime import datetime


def test_create_engine(mocker):
    mock_engine = mocker.patch('utils.db_utils.create_engine')

    connection_details = {'dbname': 'test_target_db',
                          'user': 'test_user',
                          'password': 'test_password',
                          'host': 'localhost',
                          'port': '5432'
                          }
    db_location = f'postgresql://{connection_details['user']}:'\
        f'{connection_details['password']}@{connection_details['host']}:'\
        f'{connection_details['port']}/{connection_details['dbname']}'
    create_db_engine(connection_details)

    mock_engine.assert_called_once_with(db_location)


def test_create_connection(mocker):
    mock_engine = mocker.patch('utils.db_utils.create_engine')
    mock_engine_value = 'test_engine'
    mock_engine.connect.return_value = mock_engine_value
    create_connection(mock_engine)
    mock_engine.connect.assert_called_once_with()


def test_get_time(mocker):
    timenow = datetime.strptime('2025-04-05T06:00:00', '%Y-%m-%dT%H:%M:%S')
    mock_datetime = mocker.patch('utils.db_utils.datetime')
    mock_datetime.now.return_value = timenow
    assert get_time(5) == ['2025-04-05T01:00:00', '2025-04-05T06:00:00']
