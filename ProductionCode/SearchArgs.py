"""
Written by Kai R. Weiner
"""

"""
Stores information about a search for the amount of deaths given a set of search terms.
"""
class SearchArgs:

    def __init__(self, state, age, gender, cause):
        """
        Sets up an instance of SearchArgs.

        Args
            state : state being searched for. If this term is not being searched: None
            age : age being searched for. If this term is not being searched: None
            gender : gender being searched for. If this term is not being searched: None
            cause : cause of death being searched for. If this term is not being searched: None
        Return:
            An SearchArgs object.
        """
        self.arguments = {
            "state_name": state,
            "age": age,
            "gender": gender,
            "cause": cause
        }
    
    def set_state_name(self, new_state):
        """
        Sets the state being searched for to a specified input.

        Args:
            new_state : the new state being searched for
        """
        self.arguments.update({"state_name": new_state})

    def set_age(self, new_age):
        """
        Sets the age being searched for to a specified input.

        Args:
            new_age : the new age being searched for
        """
        self.arguments.update({"age": new_age})

    def set_gender(self, new_gender):
        """
        Sets the gender being searched for to a specified input.
        Args:
            new_gender : the new gender being searched for
        """
        self.arguments.update({"gender": new_gender})

    def set_cause(self, new_cause):
        """
        Sets the cause of death being searched for to a specified input.

        Args:
            new_cause : the new cause of death being searched for
        """
        self.arguments.update({"cause": new_cause})
    
    def set_term_from_string(self, key, new_value):
        """
        Sets a search term specified by a string.

        Args:
            key : the term being set
            new_value : the new value of the term being set
        """
        self.arguments.update({key: new_value})
    
    def get_state(self):
        return self.arguments.get("state_name")
    
    def get_age(self):
        return self.arguments.get("age")
    
    def get_gender(self):
        return self.arguments.get("gender")
    
    def get_cause(self):
        cause = self.arguments.get("cause")
        if cause == None:
            return cause
        else:
            return cause.lower()
    
    def get_arguments(self):
        return self.arguments
    
    def get_term_from_string(self, key):
        return self.arguments.get(key)