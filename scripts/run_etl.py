import os
import sys
from config.env_config import setup_env
from etl.extract.extract import extract_api
from etl.transform.transform import clean_earthquake_data
from etl.load.load import load_data
from datetime import datetime, timezone, timedelta
import schedule
import subprocess


def main():
    run_env_setup()

    endtime = datetime.now(timezone.utc)
    starttime = (endtime - timedelta(hours=8)).strftime('%Y-%m-%dT%H:%M:%S')
    endtime = endtime.strftime('%Y-%m-%dT%H:%M:%S')

    data = extract_api(starttime, endtime)
    print('Extracted successfully')

    data = clean_earthquake_data(data)
    print('Data cleaned successfully')

    load_data(data)
    print('Data loaded successfully into database')

    print(
        f"ETL pipeline run successfully in "
        f'{os.getenv("ENV", "error")} environment!'
    )


def run_env_setup():
    print("Setting up environment...")
    setup_env(sys.argv)
    print("Environment setup complete.")


if __name__ == "__main__":
    user = input()
    print('here')
    main()
