import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


"""This function runs queries that load data from the S3 files into redshift"""

def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

""" This function runs the INSERT statements, and selects the data from staging tables, and ingests it into the 
the fact and dimension tables
"""

def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

"""This main function access the config file, makes a connection to AWS and runs the 2 functions above"""
def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    
    print('Establishing the connection to redshift...')
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    print('Connection to redshift established....')
    cur = conn.cursor()
    
    print('Loading staging tables...')
    load_staging_tables(cur, conn)
    
    print('Transforming the data and loading it into dimension and fact tables...')
    insert_tables(cur, conn)

    conn.close()
    print('The ETL process is complete')


if __name__ == "__main__":
    main()