import psycopg2
import uuid
import os
from transform import iterate_nested_json_for_loop

def execute_scripts_from_file(filename,connection):
    """
    Prepare data values to insert into seperate tables

    create list of the data values which corresponds with each specified table
    Parameters
    ----------
    filename: string
        SQL file with table creation commands
    Returns
    -------
    None

    """
    # Open and read the file as a single buffer
    file_sql = open(filename, 'r')
    sqlFile = file_sql.read()
    file_sql.close()

    # all SQL commands (split on ';')
    sql_commands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sql_commands[:-1]:
        try:
            connection.execute(command)
        except Exception as e:
            print(e)


def put_into_database(values,table,unique_id):
    """
    Insert values into database

    Insert transformed values into each table within the database
    ----------
    values: list
        list of values
    table: string
        table name
    unique_id: UUID
        unique id associated with each entry
    Returns
    -------
    None

    """
    #creates an connection to the databbase
    #TODO: Add error handeling and testing to connection
    conn = psycopg2.connect(database = os.getenv('PG_DB'),
                            user = os.getenv('PG_USERNAME'),
                            password = os.getenv('PG_PASSWORD'),
                            host = os.getenv('DB_HOST'),
                            port = "5432")
    
    cur = conn.cursor()  
    #create tables if not exist
    try:
        execute_scripts_from_file('create_tables.sql',cur)
        conn.commit()
    except:
        conn.rollback()
    #insert values into tables
    try:
        cur.execute(f"INSERT INTO {table} VALUES ('{unique_id}',{values})")
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    conn.close()


def iterate_table_insert(table_names,table_values):
    """
    Itterative value insert

    Itterating over tables and values to insert into tables
    ----------
    table_names: list
        list of table names in database
    table_values: list
        list of list of values
    Returns
    -------
    None

    """
    #create a random unique id to be used as dimension table primary id and fact tables
    #foreign keys
    unique_id = uuid.uuid4()
    for table_value,table in zip(table_values,table_names):
        listed = []
        #ensure that only values are inserted and no keys are included
        if isinstance(table_value, dict):
            lis_of_vals = iterate_nested_json_for_loop(table_value,listed)
            values_to_enter = ','.join(f"{v}" for v in lis_of_vals)
            put_into_database(values_to_enter,table,unique_id)
        else:
            values_to_enter = ','.join(f"{v}" for v in table_value)
            put_into_database(values_to_enter,table,unique_id)

