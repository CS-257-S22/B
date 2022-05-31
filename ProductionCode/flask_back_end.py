import psycopg2
import psqlConfig as config
from SearchArgs import SearchArgs
from SearchResult import SearchResult
import random

class DeathsPerSearchResult:

    def __init__(self, search, deaths):
        self.state = search.get_state()
        self.age = search.get_age()
        self.gender = self.return_gender_as_string(search.get_gender())
        self.cause = search.get_cause()
        self.deaths = deaths
    
    def return_gender_as_string(self, gender):
        if gender == "M":
            return "males"
        else:
            return "females"
    
    def get_data_as_string(self):
        return "Number of deaths due to "+self.cause+" for "+self.gender+", age "+self.age+" in "+self.state+", is: \n"+self.deaths

class LeadingCauseSearchResult(DeathsPerSearchResult):

    def __init__(self, search, cause, deaths):
        super.__init__(search, deaths)
        self.cause = cause
    
    def get_data_as_string(self):
        if (self.deaths != 0):
            return "Leading cause of death for "+self.gender+", age "+self.age+" in "+self.state+", is: \n"
            +self.cause.lower()+", which was responsible for the deaths of "+self.deaths+" people in this category."
        else:
            return "There were no deaths found for "+self.gender+", age "+self.age+" in "+self.state+"."

connection = connect()
states = return_list_of_states()
causes = return_list_of_causes()
facts = ["The leading cause of death for infants younger than 1 is extreme immaturity with 13,660 deaths", 
    "For people 100 and up, the leading cause of death is dementia with 16,661 deaths.", "The most common cause of death for males is atherosclerotic heart disease, with 463,155 deaths.", 
    "The age group with the most deaths is 88 years old with 399,487 deaths.", "The most common cause of death for females is alzheimer's disease with 406,313 deaths"]
    
def connect():
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password, host="localhost")
    except Exception as e:
        print("Connection error: ", e)
        exit()
    return connection
    
def get_query_result(query, query_inputs):
    try:
        cursor = connection.cursor()
        cursor.execute(query, query_inputs)
        result = cursor.fetchall()
    except Exception as e:
        print("Internal error: ", e)
        exit()
    return result
    
def return_list_of_states():
    states = retrieve_states_from_database()
    states.sort()
    return states
    
def retrieve_states_from_database():
    states = get_query_result("SELECT DISTINCT state_name FROM death_data;", ())
    reformatted_states = reformat_list(states)
    return reformatted_states
    
def get_states():
    return states

def return_list_of_causes():
    causes = retrieve_causes_from_database()
    causes.sort()
    return causes
    
def retrieve_causes_from_database(search = SearchArgs(None, None, None, None)):
    query, query_inputs = return_query_with_search_arguments("SELECT DISTINCT cause FROM death_data WHERE TRUE", search)
    causes = get_query_result(query, query_inputs)
    causes = reformat_list(causes)
    return causes
    
def get_causes():
    return causes
    
def reformat_list(list):
    new_list = []
    for item in list:
        new_list.append(item[0])
    return new_list
    
def get_fact():
    """
    Retrieve fact from facts at given random int
        
    Returns:
        a string from facts 
    """
    index = random.randint(0,4)
    random_fact = facts[index]
    return random_fact  

def get_search_result_from_function(function_type, search_args):
    """
    Returns the search result for the passed arguments and function.

    Args:
        function_type: either 'dp' or 'lc', determines which function is used
        search_args: SearchArgs object with the search arguments
        
    Returns:
        the data for the search_args arguments using the passed function
    """

    if function_type == 'dp':
        return get_deaths_per_arguments(search_args)
    else:
        return get_leading_cause_per_arguments(search_args)

def return_arguments_as_search(search_arguments):
    search = SearchArgs(None, None, None, None)

    for key in search_arguments:
        value = search_arguments[key]
        if value != "None":
            search.set_term_from_string(key, value)
    return search

def return_search_as_query(search):
    query = ""
    query_inputs = ()
    for key in search.get_arguments():
        if (search.get_term_from_string(key) != None):
            query += " AND "+key+" = %s"
            query_inputs += (search.get_term_from_string(key),)
    return query, query_inputs
    
def return_query_with_search_arguments(query, search):
    search_query, query_inputs = return_search_as_query(search)
    query += search_query+";"
    return query, query_inputs
    
def get_deaths_per_arguments(search):
    query, query_inputs = return_query_with_search_arguments("SELECT SUM(deaths) FROM death_data WHERE TRUE", search)
    total_deaths = get_query_result(query, query_inputs)
    total_deaths = reformat_list(total_deaths)

    result = DeathsPerSearchResult(search, total_deaths[0])
    return result
    
def get_leading_cause_per_arguments(search):
    causes = retrieve_causes_from_database(search)
    causes.remove("Miscellaneous")
    leading_cause = ""
    leading_cause_deaths = 0

    for cause in causes:
        cause_deaths = get_deaths_per_cause(search, cause)
        leading_cause, leading_cause_deaths = return_greater_cause(cause, cause_deaths, leading_cause, leading_cause_deaths)
    
    result = LeadingCauseSearchResult(search, leading_cause, leading_cause_deaths)

    return (leading_cause, leading_cause_deaths)
    
def get_deaths_per_cause(search, cause):
    cause_search = search
    cause_search.set_cause(cause)
    cause_deaths = get_deaths_per_arguments(cause_search)
    return cause_deaths
    
def return_greater_cause(cause, cause_deaths, leading_cause, leading_cause_deaths):
    if (leading_cause_deaths < cause_deaths):
        leading_cause = cause
        leading_cause_deaths = cause_deaths
    return leading_cause, leading_cause_deaths

#referenced off of psycopg2 lab
#heavily referenced https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
