def prepare_data(json_api_return):
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
    data_keys = ['cases', 'testing', 'outcomes']
    table_values = []

    try:
        # Append separate blobs corresponding to the table name convention
        # Cases_Dimension
        table_values.append([f"'{json_api_return['data']['date']}'", json_api_return['data']['states']])

        # Cases_Fact, Testing_Fact
        for key in data_keys[:-1]:
            table_values.append(json_api_return['data'][key])

        # Hospitalization_Fact, Death_Fact
        for key in ['hospitalized', 'death']:
            table_values.append(json_api_return['data']['outcomes'][key])
    except KeyError as e:
        raise KeyError(f"Key '{e}' does not exist. Check if correct data is returned from the API")

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