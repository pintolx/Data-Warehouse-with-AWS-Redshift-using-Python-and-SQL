import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

"""This function helps us to drop any tables that we would like to drop"""
def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

"""This function uses the queries from the create_tables file to create tables"""
def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """Loading the configuration file"""
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    
    print('Establishing the connection to redshift...')
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    
    print('Connection to redshift established....')

    cur = conn.cursor()
    print('Dropping any existing tables')
    drop_tables(cur, conn)
    
    create_tables(cur, conn)
    print('The tables have been successfully created')
    conn.close()


if __name__ == "__main__":
    main()