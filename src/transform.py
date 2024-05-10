def prepare_data(json_api_retrun):
    """
    Prepare data values to insert into seperate tables

    create list of the data values which corresponds with each specified table
    Parameters
    ----------
    json_api_retrun: dictionary
        the json blob returned by the api
    Returns
    -------
    table_values: list
        list of values for specific table identified

    """
    #key values of top level json objects
    data_keys = ['cases','testing','outcomes']
    list_of_json_objects = []
    table_values = [] 
    #extract the json objects for each key in the data key; value object. 
    try:
        for each in data_keys:
            list_of_json_objects.append(json_api_retrun['data'][each])
        #append the seperate blobs corresponding to the table name convention
        #Field_Definitions_Dimension
        #TODO: Implement ingestion of meta data for schema changes
        #      Check if schema changed and insert only if changed and alert
        #Cases_Dimension
        table_values.append([f"'{json_api_retrun['data']['date']}'",json_api_retrun['data']['states']])
        #Cases_Fact
        table_values.append(list_of_json_objects[0])
        #Testing_Fact
        table_values.append(list_of_json_objects[1])
        #Hospitalization_Fact
        table_values.append(list_of_json_objects[2]['hospitalized'])
        #Death_Fact
        table_values.append(list_of_json_objects[2]['death'])
    except Exception as e:
        raise SystemExit(f"Key {e} does not exist - check if correct data is returned from the api")
    return table_values


def iterate_nested_json_for_loop(json_obj,listed):
    """
    Unnest json object

    The json object is drilled down and unnested to the value level to create a flat 
    falt structure of the values
    Parameters
    ----------
    json_obj: dictionary
        the json blob returned by the api
    listed: list
        an empty list which will contain the values
    Returns
    -------
    listed: list
        list of values

    """
    #drill down to value level
    for _, value in json_obj.items():
        if isinstance(value, dict):
            iterate_nested_json_for_loop(value,listed)
        else:
            listed.append(value)
    return listed