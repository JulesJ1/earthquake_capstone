import pytest
from etl.load.load import create_connection


def test_create_connection(mocker):
    mock_engine = mocker.patch('etl.load.load.sqlalchemy.create_engine')

    test_details = {
        'TARGET_DB_NAME': 'test_target_db',
        'TARGET_DB_USER': 'test_user',
        'TARGET_DB_PASSWORD': 'test_password',
        'TARGET_DB_HOST': 'localhost',
        'TARGET_DB_PORT': '5432'
    }
    db_details = f'postgresql://{test_details['TARGET_DB_USER']}:{test_details['TARGET_DB_PASSWORD']}@{test_details['TARGET_DB_HOST']}:{test_details['TARGET_DB_PORT']}/{test_details['TARGET_DB_NAME']}'
    create_connection(test_details)

    mock_engine.assert_called_once_with(db_details)


def test_insert_data(mocker):
