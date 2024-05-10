def prepare_data(json_api_retrun):
    """
    Prepare data values to insert into seperate tables

    create list of the data values which corresponds with each specified table
    Parameters
    ----------
    json_api_retrun: json object
        the json blob returned by the api
    Returns
    -------
    table_values: list
        list of values for specific table identified

    """
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


def iterate_nested_json_for_loop(json_obj,listed):
    """
    Unnest json object

    The json blob is drilled down and unnested to the value level to create a flat 
    falt structure of the values
    Parameters
    ----------
    json_obj: json object
        the json blob returned by the api
    listed: list
        an empty list which will contain the values
    Returns
    -------
    listed: list
        list of values

    """
    for _, value in json_obj.items():
        if isinstance(value, dict):
            iterate_nested_json_for_loop(value,listed)
        else:
            listed.append(value)
    return listed