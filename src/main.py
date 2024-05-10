


from datetime import datetime 
import pandas as pd
from extract import call_api,api_data,prepare_data
from load import iterate_table_insert


def main():

        meta_tablename = "meta"
        data_tablename = "cases"
        listed = []
        tables = ['Cases_Dimension','Cases_Fact','Testing_Fact','Hospitalization_Fact','Death_Fact']
        current_date = '2021-01-02'#datetime.now().date() #current date to get the covid data for today
        api_url = "https://api.covidtracking.com/v2/us/daily/"+str(current_date)+".json"

        api_retrun = api_data.read_json(call_api(api_url))
        something_it = prepare_data(api_retrun)
        iterate_table_insert(tables,something_it)
        
        

if __name__ == "__main__": main()
