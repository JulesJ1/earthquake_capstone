import os
import sys
from config.env_config import setup_env
from etl.extract.extract import extract_api
from etl.transform.transform import clean_earthquake_data
from etl.transform.transform_esmc import transform_esmc_data
from etl.load.load import load_data
from datetime import datetime, timezone, timedelta
import schedule
import subprocess
import time

TIME_LENGTH = 30


def main():
    run_env_setup()

    print('Strarting pipeline')

    try:

        endtime = datetime.now(timezone.utc)
        starttime = (
            endtime - timedelta(hours=TIME_LENGTH/60)
            ).strftime('%Y-%m-%dT%H:%M:%S')
        endtime = endtime.strftime('%Y-%m-%dT%H:%M:%S')

        usgsquery = 'https://earthquake.usgs.gov/fdsnws/event/1/query'\
                    f'?format=geojson&starttime={starttime}&endtime={endtime}'
        esmcquery = 'http://www.seismicportal.eu/fdsnws/event/1/query'\
                    f'?start={starttime}&end={endtime}&format=json'
        run_pipeline(usgsquery, "usgs")
        run_pipeline(esmcquery, "esmc")

        print(f'Pipeline will run every {TIME_LENGTH} minutes')
        base_path = os.path.dirname(__file__)
        path = os.path.join(base_path, '../scripts/run_etl.py')
        subprocess.run([sys.executable, path, os.environ['ENV']], check=True)

    except subprocess.CalledProcessError as e:
        print(f'Failed to run pipeline: {e}')


def run_pipeline(query, source):

    data = extract_api(query)

    print('Extracted successfully')

    if source == "usgs":
        data = clean_earthquake_data(data)
    else:
        data = transform_esmc_data(data)
    print('Data cleaned successfully')

    load_data(data)
    print('Data loaded successfully into database')

    print(
        f"ETL pipeline run successfully in "
        f'{os.getenv("ENV", "error")} environment!'
    )


schedule.every(TIME_LENGTH).minutes.do(main)


def run_env_setup():
    print("Setting up environment...")
    setup_env(sys.argv)
    print("Environment setup complete.")


if __name__ == "__main__":

    while True:
        schedule.run_pending()
        time.sleep(1)
