# Earthquake Visualiser

## Project Description:

This project explores how earthquake data can be extracted from a source, transformed and then loaded into a database. Analysis is then conducted on the clean data to gain insights from the location, magnitude and depth. This information is displayed in a streamlit app with visualisations.

The initial earthquake data is provided by the USGS Earthquake API. This data is ingested into python, where it is cleaned and transformed using pandas. Finally, the clean data is loaded into a postgres database. This ETL (Extract Transform Load) pipeline runs using python's schedule library which allows it to perform the ETL process every 30 minutes.

The clean data in the Postgres database is visualised in a dashboard using streamlit. The dashboard map displays different eartquake events over a timespan. Each event on the map can be selected to view information such as its magnitude, depth and location.

The data in the dashboard can be filtered by date, which will query the database for data if the selected date is outside of the currently displayed date. There are also filters for minimum magnitude and type of event which can include earthquakes, ice quakes and explosions. The 'Data Analyser' tab displays the dataframe, a barchart showing the number of occurences for each hour and a lineplot of Depth vs. Magnitude.

The United States Geological Survey (USGS) provides a free API for [recent and historical earthquake information](https://earthquake.usgs.gov/fdsnws/event/1/)

## Project Considerations

### Optimising Query Execution

- Normalising the data would increase performance as there are many repeating locations in the database. The database can be normalised by creating a seperate table for locations with a primary key that is used as a foreign key in the main earthquake table. When making a query which includes location, these two tables can then be joined.
- Indexing the 'time' column in the database would help to increase query performance as the dataset increases. Querying the database for the entire time range (~13,000 records) takes around 1 second without indexing the time column.

### Error Handling And Logging

#### Error Handling

- The ETL pipeline includes error handling when extracting and loading the data.
- During extraction, request error handling is implemented to catch errors from requests that are invalid, timeout, return a 400 status or return an no data.
- During the loading phase, there is error handling for creating the database engine, connecting to the database, creating tables and inserting data into a table.
- Error handling allows the pipeline to continue running on a schedule even if an error occurs, errors will simply be logged and execution will continue.

#### Logging

- Logging is used in the pipeline and when querying the database.
- When an error occurs in the pipeline, the error is logged in a .log file. Additionally, information such as the number of rows inserted into the databse after successfully loading is also logged.
- When a query is made to the database, logs are made if the query fails. If the query is successful the speed of the query is logged.
- These logs can be leveraged to help with debugging and keep track of the pipeline and query performance.

### Security and privacy issues

While the database does not contain any confidential information, the transfer of data between the application and database should always be secure. The security of the database can be maintained by considering:

- The principle of least priveledge so that users only have access to the resources that they need at their level.
- Use of firewall and monitoring for protection against malicious attacks.
- Encrypting any sensitive data during transfer with the streamlit app.

### Deploying The Application To AWS

#### ETL Pipeline:

- The ETL pipeline can be adapted to run on AWS lambda's serverless architecture. Lambda would be more suitable than AWS Glue due to the pipelines quick runtime.
- AWS EventBridge can be used to trigger the lambda function on a schedule.
- AWS CloudTrail can be used to store logs during the ETL process.
- The Postgres database can be migrated to Postgres for RDS as its new destination.

#### Streamlit App:

- The streamlit dashboard can be containerised using docker and then deployed to an ec2 instance (or multiple instances to increase availability).
- An EC2 autoscaling group can be setup to ensure the application is scalable, and a load balancer can be used to route traffic between the instances.
- A security group for the EC2 instances will address security, allowing communication between the application, internet (through an internet gateway) and rds.
- The database credentials and table location variables can be stored using parameter store.

## Run The Project Locally

### Virtual Environment Setup

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

```
   TARGET_DB_NAME=< DATABASE NAME>
   TARGET_DB_USER=< DATABASE USERNAME>
   TARGET_DB_PASSWORD=< DATABASE PASSWORD>
   TARGET_DB_HOST=< DATABASE HOST ADDRESS>
   TARGET_DB_PORT=< DATABASE PORT NUMBER>
   TARGET_DB_TABLE=< DATABASE TABLE NAME>
   TARGET_DB_SCHEMA=< DATABASE SCHEMA NAME>
```

3. Run the following script:

```bash
run_etl prod
```

### Running tests

1. create a file named .env.test in the root directory.
2. Set the test database environment variables the same way as step 2 in Running the etl pipeline.
3. Run the following script, providing the type of test as an argument:

```bash
run_tests <unit|integration|component|all|streamlit>
```

### Locally starting the streamlit application

Run the following script:

```bash
streamlit run app/main.py
```
