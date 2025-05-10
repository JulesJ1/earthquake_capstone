from etl.load.load import create_connection
import sqlalchemy


def test_create_connection(mocker):
    mock_engine = mocker.patch('etl.load.load.create_engine')

    connection_details = {
        'dbname': 'test_target_db',
        'user': 'test_user',
        'password': 'test_password',
        'host': 'localhost',
        'port': '5432'
    }

    db_location = f'postgresql://{connection_details['user']}:'\
        f'{connection_details['password']}@{connection_details['host']}:'\
        f'{connection_details['port']}/{connection_details['dbname']}'
    create_connection(connection_details)

    mock_engine.assert_called_once_with(db_location)


def test_insert_data(mocker):
    pass
