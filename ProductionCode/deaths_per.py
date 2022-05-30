"""
Written By Kai R. Weiner, Lazuli Kleinhans
"""

from SearchArgs import SearchArgs

def get_deaths_per_arguments(data, search):
    """" 
    Search through entire database to return the total number of deaths that matches all of the search parameters.
    
    Args: 
      search: a SearchInfo object with all the search info loaded into it
      data: a two dimentional array with data.csv loaded into it
    Return: 
       total_deaths: an integer total specifying the number of deaths for people who fall under the search
    """
    total_deaths = 0
    for datapoint in data:
        total_deaths += get_relevant_deaths(datapoint, search)
    return total_deaths

def get_relevant_deaths(datapoint, search):
    """ 
    Take in a point of data and search, return number of deaths if datapoint matches search param
    
    Args:
        search : the search containing factors that the user wants the number of deaths for
    Return:
        deaths: the number of deaths for the subset of people or 0 if the subset is not relevant to the search
    """
    deaths = 0
    if is_match(datapoint, search) and datapoint[4] != 5:
        deaths = int(datapoint[4])
    return deaths

def is_match(datapoint, search):
    """ 
    Determines if a subset of people is relevant to a user's search.
    
    Args:
        datapoint : the subset of people being examined
        search : the search containing factors that the user wants the number of deaths for
    Return:
        True if the subset of people fits the user's search, false if not
    """
    return is_equal_or_none(datapoint[0], search.get_state()) & is_equal_or_none(datapoint[1], search.get_age())\
        & is_equal_or_none(datapoint[2], search.get_gender()) & is_equal_or_none(datapoint[3], search.get_cause())

def is_equal_or_none(compared, value):
    """
    Determines whether or not a value is equal to either the compared value or None.
    
    Args:
        compared : the variable value is being compared with
        value : the variable being determined to be compared or None
    Return:
        True if the value is equal to compared or equal to None, False otherwise
    """
    return (value == compared) | (value == None)

# referenced this article to work with csv's:
# https://www.analyticsvidhya.com/blog/2021/08/python-tutorial-working-with-csv-file-for-data-science/
