import os
import pytest
from config.db_config import load_db_config, DatabaseConfigError


def test_load_db_config(mocker):
    # Mock environment variables
    mocker.patch.dict(os.environ, {
        'TARGET_DB_NAME': 'test_target_db',
        'TARGET_DB_USER': 'test_user',
        'TARGET_DB_PASSWORD': 'test_password',
        'TARGET_DB_HOST': 'localhost',
        'TARGET_DB_PORT': '5432',
        'TARGET_DB_TABLE': 'test_table',
        'TARGET_DB_SCHEMA': 'test_schema'
    })

    config = load_db_config()

    assert config['target_database']['dbname'] == 'test_target_db'
    assert config['target_database']['user'] == 'test_user'
    assert config['target_database']['password'] == 'test_password'
    assert config['target_database']['host'] == 'localhost'
    assert config['target_database']['port'] == '5432'
    assert config['target_database']['table'] == 'test_table'
    assert config['target_database']['schema'] == 'test_schema'


def test_load_db_config_missing_env_var_port_defaults(mocker):
    # Mock environment variables with some missing
    mocker.patch.dict(os.environ, {
   
        'TARGET_DB_NAME': 'test_target_db',
        'TARGET_DB_USER': 'test_user',
        'TARGET_DB_PASSWORD': 'test_password',
        'TARGET_DB_HOST': 'localhost',
        #'TARGET_DB_PORT': '5432'
        'TARGET_DB_TABLE': 'test_table',
        'TARGET_DB_SCHEMA': 'test_schema'
    })

    config = load_db_config()

    assert config['target_database']['dbname'] == 'test_target_db'
    assert config['target_database']['user'] == 'test_user'
    assert config['target_database']['password'] == 'test_password'
    assert config['target_database']['host'] == 'localhost'
    assert config['target_database']['port'] == '5432'
    assert config['target_database']['table'] == 'test_table'
    assert config['target_database']['schema'] == 'test_schema'


# Mapping from environment variable names to configuration keys
env_var_to_config_key = {
    'TARGET_DB_NAME': 'dbname',
    'TARGET_DB_USER': 'user',
    'TARGET_DB_HOST': 'host'
}


@pytest.mark.parametrize("env_var", [
    'TARGET_DB_NAME',
    'TARGET_DB_USER',
    'TARGET_DB_HOST'
])
def test_load_db_config_missing_env_var_errors(mocker, env_var):
    # Mock environment variables with one set to 'error'
    mock_env = {
        'TARGET_DB_NAME': 'test_target_db',
        'TARGET_DB_USER': 'test_user',
        'TARGET_DB_PASSWORD': 'test_password',
        'TARGET_DB_HOST': 'localhost',
        'TARGET_DB_PORT': '5432'
    }
    mock_env[env_var] = 'error'  # Set the parameterized env_var to 'error'
    mocker.patch.dict(os.environ, mock_env)

    config_key = env_var_to_config_key[env_var]

    with pytest.raises(DatabaseConfigError, match=(
        f"Configuration error: target_database {config_key} is set to 'error'"
    )):
        load_db_config()
