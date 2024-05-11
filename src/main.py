


from datetime import datetime 
import pandas as pd
from extract import call_api,apiData
from transform import prepare_data
from load import iterate_table_insert


def main():
        """
        Main function of ETL process

        The function contains the steps required to perform the extract, transform
        and loading of the daily COVID-19 data into a postgres databse

        Parameters
        ----------
        None
        Returns
        -------
        None

        """

        tables = ['Cases_Dimension','Cases_Fact','Testing_Fact','Hospitalization_Fact','Death_Fact']
        current_date = '2021-01-02'#datetime.now().date() current date to get the covid data for today
        api_url = f"https://api.covidtracking.com/v2/us/daily/{current_date}.json"

        #step to extract the daiky json blob from the api        
        api_return = apiData.read_json(call_api(api_url))
        if not api_return:
                return
        #step to prepare the data to be ingested
        prepared_values = prepare_data(api_return)
        #step to create the tables if not created and insert the daily data
        iterate_table_insert(tables,prepared_values)
        
        

if __name__ == "__main__": 
        main()
