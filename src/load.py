import psycopg2
import psycopg2.extras
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
    with open(filename, 'r') as sql_file:
        sql_commands = sql_file.read().split(';')

    # Execute every command from the input file
    for command in sql_commands[:-1]:
        try:
            connection.execute(command)
        except Exception as e:
            print(f"Error executing command: {e}")

def insert_into_database(values, table, cursor,unique_id):
    """
    Insert values into a database table.

    Parameters
    ----------
    values : list
        List of values to insert.
    table : str
        Table name.
    cursor : psycopg2 cursor object
        Cursor for database connection.

    Returns
    -------
    None
    """
    try:
        cursor.execute(f"INSERT INTO {table} VALUES ('{unique_id}',{values})")
    except Exception as e:
        print(f"Error inserting into {table}: {e}")


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
    # Create a random unique id to be used as dimension table primary id and fact tables foreign keys
    unique_id = uuid.uuid4()
    psycopg2.extras.register_uuid()

    try:
        # Connect to the database
        conn = psycopg2.connect(database=os.getenv('PG_DB'),
                                user=os.getenv('PG_USERNAME'),
                                password=os.getenv('PG_PASSWORD'),
                                host=os.getenv('DB_HOST'),
                                port="5432")
        cursor = conn.cursor()

        # Create tables if not exist
        execute_scripts_from_file('create_tables.sql', cursor)
        conn.commit()

        for table_value,table in zip(table_values,table_names):
            #ensure that only values are inserted and no keys are included
            if isinstance(table_value, dict):
                list_of_vals = iterate_nested_json_for_loop(table_value,[])
                values_to_enter = ','.join(f"{v}" for v in list_of_vals)
                insert_into_database(values_to_enter,table,cursor,unique_id)
            else:
                values_to_enter = ','.join(f"{v}" for v in table_value)
                insert_into_database(values_to_enter,table,cursor,unique_id)
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
    finally:
        if conn:
            conn.commit()
            conn.close()
