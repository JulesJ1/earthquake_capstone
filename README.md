# Earthquake Visualiser

## Project Aim:

The goal of this project is to explore how earthquakes can be visualised using a map. As well as uncovering insights such what times earthquakes more frequently occur at and the relationship between an earthquakes depth and magnitude.
The dashboard can be used to view different types of quakes such as earthquakes, ice quakes and explosions. Users can select data from different dates and set a minimum magnitude for data displayed.

## USGS Earthquake API

USGS provides a free API for information about recent and historical earthquake information

## Questions

### Optimising query execution

Indexing the 'time' column in the database would help to increase query performance. Querying the database for the entire time range (~13,000 records) takes around \*\*\* seconds without indexing the time column.

### Error handling and Logging

The etl pipeline includes error handling when extracting and loading the data.
During extraction, request error handling is implemented to catch errors from requests that are invalid, timeout, return a 400 status or return an no data.
During loading

### Security and privacy issues

### Deploying the application to cloud

The project can be containerised using docker

## How to run the project

### Venv Setup

#### Linux/Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-setup.txt
pip install -e .
```

#### Windows

```bash
py -m venv .venv
source .venv/scripts/activate
pip install -r requirements-setup.txt
pip install -e .
```

### Running the etl pipeline

1. create a file named .env in the root directory.
2. Set the following environment variables for the pipeline's database destination:
   TARGET_DB_NAME=< DATABASE NAME>
   TARGET_DB_USER=< DATABASE USERNAME>
   TARGET_DB_PASSWORD=< DATABASE PASSWORD>
   TARGET_DB_HOST=< DATABASE HOST ADDRESS>
   TARGET_DB_PORT=< DATABASE PORT NUMBER>
   TARGET_DB_TABLE=< DATABASE TABLE NAME>
   TARGET_DB_SCHEMA=< DATABASE SCHEMA NAME>
3. Run the script:

```bash
run_etl prod
```

### Locally starting the streamlit application

Run the following script:

```bash
streamlit run app/main.py
```
