def prepare_data(json_api_retrun):
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
    for _, value in json_obj.items():
        if isinstance(value, dict):
            iterate_nested_json_for_loop(value,listed)
        else:
            listed.append(value)
    return listed