import requests
from random import randint
from time import sleep
from datetime import datetime 
import json
import pandas as pd
import psycopg2
import uuid

meta_tablename = "meta"
data_tablename = "cases"
listed = []
tables = ['Cases_Dimension','Cases_Fact','Testing_Fact','Hospitalization_Fact','Death_Fact']
current_date = '2021-01-02'#datetime.now().date() #current date to get the covid data for today
api_url = "https://api.covidtracking.com/v2/us/daily/"+str(current_date)+".json"

class api_data():
    def __init__(self,api_response):
        self.api_response = api_response
    def read_json(self):
        json_data = json.loads(self)
        return json_data

def call_api(api_url):
    #if error dont pull in data
    try:
        data = requests.get(api_url,timeout=10).json()
    #timeout exception
    except requests.Timeout:
        try:
            for _ in range(3):
                sleep(randint(10,1000))
                data = requests.get(api_url,timeout=10).json()
        except:
            print("Timed out error recieved")
    #redirect exception
    except requests.TooManyRedirects:
        print("URL location is bad")
    #reques exception
    except requests.RequestException as e:
        raise SystemExit(e)
    return json.dumps(data)

def iterate_nested_json_for_loop(json_obj,listed):
    #listed = []
    for _, value in json_obj.items():
        if isinstance(value, dict):
            iterate_nested_json_for_loop(value,listed)
        else:
            listed.append(value)
    return listed

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

    conn = psycopg2.connect(database = "postgres",
                            user = "postgres",
                            password = "12345",
                            host = "localhost",
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

def iterate_table_insert(table_names,table_values):
    unique_id = uuid.uuid4()
    for table_value,table in zip(table_values,tables):
        listed = []
        if isinstance(table_value, dict):
            lisofvals = iterate_nested_json_for_loop(table_value,listed)
            values_to_enter = ','.join(f"{v}" for v in lisofvals)
            put_into_database(values_to_enter,table,unique_id)
        else:
            values_to_enter = ','.join(f"{v}" for v in table_value)
            put_into_database(values_to_enter,table,unique_id)

def something(json_api_retrun):
    data_keys = ['cases','testing','outcomes']
    listedinch = []
    table_values = []  
    for eacch in data_keys:
        listedinch.append(json_api_retrun['data'][eacch])
    table_values.append([f"'{json_api_retrun['data']['date']}'",json_api_retrun['data']['states']])
    table_values.append(listedinch[0])
    table_values.append(listedinch[1])
    table_values.append(listedinch[2]['hospitalized'])
    table_values.append(listedinch[2]['death'])
    return table_values


def main():
        api_retrun = api_data.read_json(call_api(api_url))
        something_it = something(api_retrun)
        iterate_table_insert(tables,something_it)
        
        

if __name__ == "__main__": main()
