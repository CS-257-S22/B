import psycopg2
import psqlConfig as config
from SearchArgs import SearchArgs
from deaths_per import *
from leading_cause import *
import random

class DataSource:

    def __init__(self):
        self.connection = self.connect()
    
    def connect(self):
        try:
            connection = psycopg2.connect(database=config.database, user=config.user, password=config.password, host="localhost")
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection
    
    def get_query_result(self, query, query_inputs):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, query_inputs)
            result = cursor.fetchall()
        except Exception as e:
            print("Internal error: ", e)
            exit()
        return result

class SiteData:

    def __init__(self):
        self.source = DataSource()
        self.states = self.return_list_of_states()
        self.causes = self.return_list_of_causes()
        self.facts = ["The leading cause of death for infants younger than 1 is extreme immaturity with 13,660 deaths", 
        "For people 100 and up, the leading cause of death is dementia with 16,661 deaths.", "The most common cause of death for males is atherosclerotic heart disease, with 463,155 deaths.", 
        "The age group with the most deaths is 88 years old with 399,487 deaths.", "The most common cause of death for females is alzheimer's disease with 406,313 deaths"]
    
    def return_list_of_states(self):
        states = self.retrieve_states_from_database()
        states.sort()
        return states
    
    def retrieve_states_from_database(self):
        states = self.source.get_query_result("SELECT DISTINCT state_name FROM death_data;", ())
        reformatted_states = self.reformat_list(states)
        return reformatted_states
    
    def get_states(self):
        return self.states

    def return_list_of_causes(self):
        causes = self.retrieve_causes_from_database()
        causes.sort()
        return causes
    
    def retrieve_causes_from_database(self, search = SearchArgs(None, None, None, None)):
        query, query_inputs = self.return_query_with_search_arguments("SELECT DISTINCT cause FROM death_data WHERE TRUE", search)
        causes = self.source.get_query_result(query, query_inputs)
        causes = self.reformat_list(causes)
        return causes
    
    def get_causes(self):
        return self.causes
    
    def reformat_list(self, list):
        new_list = []
        for item in list:
            new_list.append(item[0])
        return new_list
    
    def get_fact(self):
        """
        Retrieve fact from facts at given random int
        
        Returns:
            a string from facts 
        """
        index = random.randint(0,4)
        random_fact = self.facts[index]
        return random_fact
    
    def return_arguments_as_search(self, search_arguments):
        search = SearchArgs(None, None, None, None)

        for key in search_arguments:
            value = search_arguments[key]
            if value != "None":
                search.set_term_from_string(key, value)
        return search
    

    def get_search_result_from_function(self, function_type, search_args):
        """
        Returns the search result for the passed arguments and function.

        Args:
            function_type: either 'dp' or 'lc', determines which function is used
            search_args: SearchArgs object with the search arguments
        
        Returns:
            the data for the search_args arguments using the passed function
        """

        search_args = self.return_arguments_as_search(search_args)

        if function_type == 'dp':
            return self.get_deaths_per_arguments(search_args), search_args
        else:
            return self.get_leading_cause_per_arguments(search_args), search_args
    
    def return_search_as_query(self, search):
        query = ""
        query_inputs = ()
        for key in search.get_arguments():
            if (search.get_term_from_string(key) != None):
                query += " AND "+key+" = %s"
                query_inputs += (search.get_term_from_string(key),)
        return query, query_inputs
    
    def return_query_with_search_arguments(self, query, search):
        search_query, query_inputs = self.return_search_as_query(search)
        query += search_query+";"
        return query, query_inputs
    
    def get_deaths_per_arguments(self, search):
        query, query_inputs = self.return_query_with_search_arguments("SELECT SUM(deaths) FROM death_data WHERE TRUE", search)
        total_deaths = self.source.get_query_result(query, query_inputs)
        total_deaths = self.reformat_list(total_deaths)
        return total_deaths[0]
    
    def get_leading_cause_per_arguments(self, search):
        causes = self.retrieve_causes_from_database(search)
        causes.remove("Miscellaneous")
        leading_cause = ""
        leading_cause_deaths = 0

        for cause in causes:
            cause_deaths = self.get_deaths_per_cause(search, cause)
            leading_cause, leading_cause_deaths = self.return_greater_cause(cause, cause_deaths, leading_cause, leading_cause_deaths)
        
        return (leading_cause, leading_cause_deaths)
    
    def get_deaths_per_cause(self, search, cause):
        cause_search = search
        cause_search.set_cause(cause)
        cause_deaths = self.get_deaths_per_arguments(cause_search)
        return cause_deaths
    
    def return_greater_cause(self, cause, cause_deaths, leading_cause, leading_cause_deaths):
        if (leading_cause_deaths < cause_deaths):
            leading_cause = cause
            leading_cause_deaths = cause_deaths
        return leading_cause, leading_cause_deaths


# if __name__ == '__main__':
#     my_source = SiteData()
#     print(my_source.get_causes())

#referenced off of psycopg2 lab
#heavily referenced https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
