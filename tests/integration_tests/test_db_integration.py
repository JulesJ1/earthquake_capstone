from utils.db_utils import create_connection, create_db_engine
from config.db_config import load_db_config
import sqlalchemy


def test_create_engine_and_connect():
    db_details = load_db_config()['target_database']
    engine = create_db_engine(db_details)
    connection = create_connection(engine)

    assert isinstance(connection, sqlalchemy.engine.base.Connection)