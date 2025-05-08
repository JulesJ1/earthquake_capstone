import pandas as pd
from sqlalchemy import create_engine, text,insert, MetaData, Table, Column, VARCHAR, INT
from sqlalchemy.exc import InvalidRequestError,OperationalError, IntegrityError, SQLAlchemyError, DataError, DatabaseError
import sqlite3
import os
from dotenv import load_dotenv

from etl.extract.extract import extract_api
from etl.transform.transform import clean_earthquake_data
from config.db_config import load_db_config


def load_data(data: pd.DataFrame):

    db_details = load_db_config()['target_database']

    create_connection(db_details)

    insert_data(data)

def create_connection(connection_details: dict):
    try:
        engine = create_engine(f'postgresql://{connection_details['user']}\
            :{connection_details['password']}@{connection_details['host']}:\
            {connection_details['port']}/{connection_details['dbname']}')
        return engine
    except  OperationalError as e:
        print(f'Cannot connect: {e}')
    except DatabaseError as e:
        print(f'DatabaseError: {e}')
    except SQLAlchemyError as e:
        print(f'Could not conncet: {e}')


def create_table():
    pass

def insert_data(data: pd.DataFrame):
    try:
        pass

    except IntegrityError as e:
        print(f'{e}')

    except DataError as e:
        print(F'Data error: {e}')
    
    except SQLAlchemyError as e:
        print(f'{e}')

