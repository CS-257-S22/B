"""
Written by Lazuli Kleinhans with modifications by Jonas Bartels
"""

from sys import argv
from deaths_per import *
from SearchArgs import *
from csv_reading import *
from leading_cause import *

def print_usage_statement():
    """
    Exits and prints the usage statement.
    """
    exit("\nUSAGE: command_line_interface.py [deaths_per | leading_cause | --help] [--state STATE] [--age AGE] [--gender GENDER] [--cause CAUSE]\n")

def print_help_statement():
    """
    Exits and prints the help statement.
    """
    exit("\nUSAGE: command_line_interface.py [deaths_per | leading_cause | --help] [--state STATE] [--age AGE] [--gender GENDER] [--cause CAUSE]\n" +
         "\n" +
         "deaths_per (dp) : prints the number of deaths that are tagged with the passed search parameters.\n" +
         "    POSSIBLE SEARCH PARAMETERS:\n" +
         "    --state (-s) STATE : replace STATE with the name of the state you want to search for. Case sensitive.\n" +
         "    --age (-a) AGE : replace AGE with the age you want to search for. Takes integers.\n" +
         "    --gender (-g) GENDER : replace GENDER with the gender you want to search for. Either M or F.\n" +
         "    --cause (-c) CAUSE : replace CAUSE with the name of the cause you want to search for. Has to be exactly the same as a cause in data.csv.\n" +
         "\n" +
         "leading_cause (lc): prints the leading causes of death that are tagged with the passed search parameters.\n" +
         "    POSSIBLE SEARCH PARAMETERS:\n" +
         "    --state (-s) STATE : replace STATE with the name of the state you want to search for. Case sensitive.\n" +
         "    --age (-a) AGE : replace AGE with the age you want to search for. Takes integers.\n" +
         "    --gender (-g) GENDER : replace GENDER with the gender you want to search for. Either M or F.\n" +
         "\n" +
         "--help (-h): prints this help information.\n")

def return_argument_value(argument, value):
    """
    Takes an argument and it's value, and then returns a dictionary entry
    with the name of the value and the value itself.

    Args:
        argument: a string that is the argument identifier
        value: the value that the user passed as that argument
    Returns:
        a dictionary entry with the name of the value and the value itself
    """
    if argument == "-s" or argument == "--state":
        return {"state": value}
    if argument == "-a" or argument == "--age":
        return {"age": value}
    if argument == "-g" or argument == "--gender":
        return {"gender": value}
    if argument == "-c" or argument == "--cause":
        return {"cause": value}
    else:
        print_usage_statement()

def return_dictionary_of_arguments(input_arguments):
    """
    Returns a dictionary of the arguments in input_arguments.

    Returns:
        a dictionary of the arguments in input_arguments
    """
    argument_dictionary = {
        "state": None,
        "age": None,
        "gender": None,
        "cause": None
    }
    for i, argument in enumerate(input_arguments):
        if "-" == argument[0]:
            argument_value = return_argument_value(argument, input_arguments[i+1])
            argument_dictionary.update(argument_value)
    return argument_dictionary

def create_search_args(input_arguments):
    """
    Creates and returns a SearchArgs object that has
    all of the arguments the user passed loaded into it.

    Returns:
        a SearchArgs object that has all of the arguments
        the user passed loaded into it
    """
    argument_dictionary = return_dictionary_of_arguments(input_arguments)
    state = argument_dictionary["state"]
    age = argument_dictionary["age"]
    gender = argument_dictionary["gender"]
    cause = argument_dictionary["cause"]
    return SearchArgs(state, age, gender, cause)

# def initialize_data(data_file_name):
#     """
#     Initializes and returns data.csv transformed into an array.
    
#     Returns:
#         data.csv transformed into an array
#     """
#     initialized_file = read_CSV(data_file_name)
#     return transform_CSV_data_to_array(initialized_file)

def find_deaths_per(input_arguments, data_file_name):
    """
    Initializes data, creates a SearchArgs object, and the passes
    them into deaths_per() and returns that output.

    Returns:
        an integer of the number of deaths that are a part of the
        group indicated in search_args
    """
    data = get_CSV_data_as_list(data_file_name)
    search_args = create_search_args(input_arguments)
    return get_deaths_per_arguments(data, search_args)

def find_leading_cause(input_arguments, data_file_name):
    """
    Initializes data, creates a SearchArgs object, and the passes
    them into return_leading_cause() and returns that output.

    Returns:
        a list with the first item being the top cause of death of people that matched the
        search_args arguments and the second as the number of deaths attributed to that cause
    """
    data = get_CSV_data_as_list(data_file_name)
    search_args = create_search_args(input_arguments)
    return return_leading_cause(data, search_args)

def check_length_of_input_arguments(input_arguments):
    """
    Checks if the length of input_arguments is less than 2, and if so,
    print_usage_statement() is called.
    """
    if len(input_arguments) < 2:
        print_usage_statement()

def determine_and_execute_call(input_arguments, data_file_name):
    """ 
    Checks the argument containing the request type and executes that request
    """
    if input_arguments[1] == "deaths_per" or input_arguments[1] == "dp":
        deaths = find_deaths_per(input_arguments, data_file_name)
        return deaths
    elif input_arguments[1] == "leading_cause" or input_arguments[1] == "lc":
        leading_cause = find_leading_cause(input_arguments, data_file_name)
        return leading_cause
    elif input_arguments[1] == "--help" or input_arguments[1] == "-h":
        print_help_statement()
    else:
        print_usage_statement()



if __name__ == "__main__":
    """
    Calls check_length_of_input_arguments(), then prints the results of determine_and_execute_call()
    """
    data_file_name = 'data.csv'
    input_arguments = argv
    check_length_of_input_arguments(input_arguments)
    print(determine_and_execute_call(input_arguments, data_file_name))
    
    