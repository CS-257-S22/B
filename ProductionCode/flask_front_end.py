""" Written by Lazuli Kleinhans """

from flask import Flask, render_template, request
from SearchInfo import SearchInfo
from deaths_per import *
from leading_cause import *
from csv_reading import *

app = Flask(__name__)

# list of states copied from here: https://python-forum.io/thread-3105.html
states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
    "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
    "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
    "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
    "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
    "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
    "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
    "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
# states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado"]

def get_data(function_type, search_info):
    """
    Returns the data for the passed state using the passed function.

    Args:
        function_type: either 'dp' or 'lc', determines which function is used
        search_info: search_info object with the search arguments
    
    Returns:
        the data for the search_info arguments using the passed function
    """
    CSV_data = get_CSV_data_as_list("data.csv")
    if function_type == 'dp':
        return deaths_per(CSV_data, search_info)
    else:
        return return_leading_cause(CSV_data, search_info)

def return_dictionary_of_arguments():
    """
    Returns a dictionary of the arguments in request.args.

    Returns:
        a dictionary of the arguments in request.args
    """
    argument_dictionary = {
        "state_choice": None,
        "age_choice": None,
        "gender_choice": None,
        "cause_choice": None
    }
    
    for key in request.args:
        value = request.args[key]
        if value != "None":
            argument_dictionary.update({key: value})
    return argument_dictionary

def create_search_info():
    """
    Creates and returns a SearchInfo object that has
    all of the arguments the user passed loaded into it.

    Returns:
        a SearchInfo object that has all of the arguments
        the user passed loaded into it
    """
    argument_dictionary = return_dictionary_of_arguments()
    state = argument_dictionary["state_choice"]
    age = argument_dictionary["age_choice"]
    gender = argument_dictionary["gender_choice"]
    cause = argument_dictionary["cause_choice"]
    return SearchInfo(state, age, gender, cause)

def return_render_template(function_type):
    """
    Creates a SearchInfo object, gets the correct data for the search arguments and
    returns the correct render template for the passed function.

    Args:
        function_type: either 'dp' or 'lc', determines which function is used
    
    Returns:
        the correct render template for the passed function
    """
    search_info = create_search_info()
    returned_data = get_data(function_type, search_info)
    return render_template(f'{function_type}.html', states=states, 
        search_info=search_info, data=returned_data)

@app.route('/')
def homepage():
    """
    Returns the homepage render template.
    
    Returns:
        the homepage render template
    """
    return render_template('home.html')

@app.route('/dp/')
def deaths_per_template():
    """
    Returns the render template for deaths per with no search_info.
    
    Returns:
        the render template for deaths per with no search_info
    """
    return render_template('dp.html', states=states, search_info=None)

@app.route('/dp/choose_arguments')
def deaths_per_template_arguments():
    """
    Returns the render template for deaths per.

    Returns:
        the render template for deaths per
    """
    return return_render_template('dp')

@app.route('/lc/')
def leading_cause_template():
    """
    Returns the render template for leading cause, with no search_info.
    
    Returns:
        the render template for leading cause, with no search_info
    """
    return render_template('lc.html', states=states, search_info=None)

@app.route('/lc/choose_arguments')
def leading_cause_template_arguments():
    """
    Returns the render template for leading cause.

    Returns:
        the render template for leading cause
    """
    return return_render_template('lc')

@app.errorhandler(404)
def page_not_found(e):
    """
    Returns the render template for a 404 error.

    Args:
        e: error that was thrown

    Returns:
        the render template for a 404 error
    """
    return render_template('404.html', error=e)

@app.errorhandler(500)
def python_bug(e):
    """
    Returns a string that has a general error.

    Returns:
        a string that has a general error
    """
    return "Sorry, my programmer is bad at their job. :)"

if __name__ == '__main__':
    """ Runs the app. """
    app.run()