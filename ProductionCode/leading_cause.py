"""
Written by Tin Nguyen, Lazuli Kleinhans & Kai R. Weiner
"""

def fits_search(datapoint,search):
    """ Take in datapoint, return booleans about whether datapoint matches search param or specifc search is not needed"""
    return is_equal_or_none(datapoint[0], search.get_state()) & is_equal_or_none(datapoint[1], search.get_age())\
        & is_equal_or_none(datapoint[2], search.get_gender())

def is_equal_or_none(compared, value):
    """Take in two varibles, returns True if the value match compared or None"""
    return (value == compared) | (value == None)

def return_data_entry(datapoint, data_dictionary):
    """ 
    Determine if a cause already exists in dictionary. If so, sum the number of   
    deaths. Otherwise, create new key with the new cause and num of deaths. 
    
    Args: 
        data_file: a two dimentional array with data.csv loaded into it
        data_dictionary: a dictionary with relevant causes as keys and deaths of said cause as the value. 
    Returns: 
        dictionary with updated cause of deaths keys or number of deaths per cause. 
    """
    if datapoint[3] in data_dictionary.keys():
        new_entry = {datapoint[3]: int(data_dictionary[datapoint[3]]) + int(datapoint[4])}
    else:
        new_entry = {datapoint[3]: int(datapoint[4])}
    return new_entry

def return_cause_of_death_dictionary(data_file, search_info):
    """
    Search database for the passed search info and returns a dictionary
    with all the matching causes and the number of deaths per each one.
    
    Args:
        data_file: a two dimentional array with data.csv loaded into it
        search_info: a SearchInfo object with all the search info loaded into it
    Returns:
        a dictionary where each entry is a cause of death that fit the search info
        and the number of deaths attributed to that cause.
    """
    data_dictionary = {}
    for datapoint in data_file:
        if fits_search(datapoint, search_info) and datapoint[3] != "Miscellaneous":
            new_entry = return_data_entry(datapoint, data_dictionary)
            data_dictionary.update(new_entry)
    return data_dictionary

def find_most_common_cause_of_death(data_dictionary):
    """take in dict of causes, return cause with most deaths"""
    max_number_of_deaths = 0
    leading_cause_of_death = ""
    for key in data_dictionary:
        if data_dictionary[key] > max_number_of_deaths:
            max_number_of_deaths = data_dictionary[key]
            leading_cause_of_death = key
    return [leading_cause_of_death, max_number_of_deaths]

def return_leading_cause(data_file, search_info):
    """takes in dataset & search param, returns cause w/ most deaths"""
    data_dictionary = return_cause_of_death_dictionary(data_file, search_info)
    leading_cause = find_most_common_cause_of_death(data_dictionary)
    return leading_cause
