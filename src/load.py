import psycopg2
import uuid
import os

def execute_scripts_from_file(filename,curnection):
    # Open and read the file as a single buffer
    file_sql = open(filename, 'r')
    sqlFile = file_sql.read()
    file_sql.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        try:
            curnection.execute(command)
        except Exception as e:

            print(e)


def put_into_database(values,table,unique_id):

    conn = psycopg2.connect(database = os.getenv('PG_DB'),
                            user = os.getenv('PG_USERNAME'),
                            password = os.getenv('PG_PASSWORD'),
                            host = os.getenv('DB_HOST'),
                            port = "5432")
    
    cur = conn.cursor()  
    
    try:
        execute_scripts_from_file('create_tables.sql',cur)
        conn.commit()
    except:
        conn.rollback()
    try:
        cur.execute(f"INSERT INTO {table} VALUES ('{unique_id}',{values})")
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    conn.close()

def iterate_nested_json_for_loop(json_obj,listed):
    for _, value in json_obj.items():
        if isinstance(value, dict):
            iterate_nested_json_for_loop(value,listed)
        else:
            listed.append(value)
    return listed

def iterate_table_insert(table_names,table_values):
    unique_id = uuid.uuid4()
    for table_value,table in zip(table_values,table_names):
        listed = []
        if isinstance(table_value, dict):
            lisofvals = iterate_nested_json_for_loop(table_value,listed)
            values_to_enter = ','.join(f"{v}" for v in lisofvals)
            put_into_database(values_to_enter,table,unique_id)
        else:
            values_to_enter = ','.join(f"{v}" for v in table_value)
            put_into_database(values_to_enter,table,unique_id)

