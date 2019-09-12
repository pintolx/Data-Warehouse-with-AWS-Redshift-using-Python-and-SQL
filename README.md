Project structure
1. The project contains 5 files which include create_tables.py, sql_queries.py, etl.py, dwh.cfg, Run File.ipynb. Here is the breakdown of what is happening in each of the project files.
a). Run File.ipynb.
This file has instructions about how to run the project. The project is run with the command %run -i 'etl.py'. If the process is successful, it will print 'The ETL process is complete'.
After the ETL process is complete and evaluation is done, the clusters can be deleted by running the last command in this file.
b). dwh.cfg
This is the configuration file it it contains connection details that help us connect to the AWS Redshift cluster.
c). sql_queries.py
This file contains the configuration setup which uses the dwh.cfg file to connect to the AWS Redshift cluster.
# DROP TABLES
This section contains queries that would help us drop tables if they already exist
# CREATE TABLES
This section contains queries that are used to create tables in the database. We structured the data warehouse in a star schema with one fact table and four dimension tables. The fact table was called songplays and the dimension tables are users, songs, artists, time
# STAGING TABLES
The data is initially stored in two staging tables that include staging_songs and staging_events, this is where the data is stored first before it is transfered into the tables.
# Insert Statements
We use these statements to select data from the staging tables and ingest it into the fact and dimension tables
d) etl.py
This file contains functions that import queries from the sql_queries files, connects to the redshift cluster, creates the tables, loads data into the staging tables and inserts data into the fact and dimension tables.