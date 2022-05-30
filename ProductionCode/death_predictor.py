'''
Written by Jonas Bartels
'''

from datetime import datetime, date, timedelta
from email.mime import base
from sys import argv
from SearchArgs import *
import random
from csv_reading import *

class Prediction():
    def __init__(self, date_of_death, age_at_death, main_cause, misc_cause):
        self.date = date_of_death
        self.age_at_death = age_at_death
        self.main_cause = main_cause
        self.misc_cause = misc_cause
        self.today = date.today()
        self.set_combined_cause()
        self.reformat_date()

    def set_combined_cause(self):
        if self.misc_cause != None:
            base_string = '{} ({})' 
            self.combined_cause = base_string.format(self.misc_cause, self.main_cause)
        else:
            self.combined_cause = self.main_cause

    def get_days_remaining(self):
        print(self.date - self.today)

    def reformat_date(self):
        listed = str(self.date).split('-')
        base = "{}/{}/{}"
        self.reformatted_date = base.format(listed[1], listed[2], listed[0])
                
            
class DataLine():
    def __init__(self, line):
        self.state = line[0]
        self.age = line[1]
        self.gender = line[2]
        self.cause = line[3]
        self.code = line[4]
        self.death_toll = line[5]
        self.parts_per = line[6]
        self.list = line

class InputArguments():
    def __init__(self, list_of_inputs):
        self.name = list_of_inputs[0]
        self.state = list_of_inputs[1]
        self.birthday = list_of_inputs[2]
        self.gender = list_of_inputs[3]

class DeathPredictor():
    def __init__(self, list_of_inputs, seed_influencer):
        self.seed_influencer = seed_influencer
        self.input_arguments = InputArguments(list_of_inputs)
        self.data, self.misc_data = self.initialize_data("data.csv"), self.initialize_data("all_states_misc.csv")
        self.search_args = SearchArgs(self.input_arguments.state, None, None, None)
        self.misc_search_args = SearchArgs(None, None, None, None)
        self.set_gender()
        self.set_today()
        self.set_age_and_DoB()
        self.generate_seed()
        self.set_seed()

    def list_to_line_object(self, list):
        '''
        Takes a list of lines of data (in list form)
        and returns it as a list of DataLine objects.
        
        Args:
            list: a 2D list of data
        Returns:
            a 1D list of DataLine objects
        '''
        output_list = []
        for line in list:
            output_list.append(DataLine(line))
        return output_list

    def initialize_data(self, data_file_name):
        '''
        Turns data from a CSV into a list of DataLine objects

        Args:
            data_file_name: The name of the CSV to be converted
        Returns:
            a 1D list of DataLine objects
        '''
        initialized_file = get_CSV_data_as_list(data_file_name)
        list_of_lists = load_CSV_list(initialized_file)
        return self.list_to_line_object(list_of_lists)
        
    def is_relevant_line(self, line):
        '''
        Checks whether a line of data could describe a possible death of the user
        
        Args:
            line: a DataLine object containing death data
        Returns:
            a Boolean.
        '''
        if self.equal_or_none(line.state, self.search_args.state) & \
            self.equal_or_none(line.gender, self.search_args.gender) & \
            (int(line.age) >= int(self.search_args.age)):
            return True
        else:
            return False

    def set_relevant_lines(self):
        '''
        Adds DataLine lines to self.relevant_lines if they are possible ways the user might perish
        '''
        self.relevant_lines = []
        for line in self.data:
            if self.is_relevant_line(line):
                self.relevant_lines.append(line)

    def set_death_toll(self):
        '''
        Sets self.total_relevant_deaths to the total
        number of deaths in the combined relevant_lines list.
        '''
        self.total_relevant_deaths = 0
        for line in self.relevant_lines:
            if line.death_toll == "under 10":
                line.death_toll = 5
            self.total_relevant_deaths += int(line.death_toll)

    def is_within_bounds(self, age_range):
        '''
        Determines whether the self.age_at_death lies 
        between the two numbers in age_range(inclusive), 
        returns True or False
        
        Args:
            age_range: A string of the form #-# with the 
            first # being the lower bound and the second
            # being the upper bound.
        Returns:
            A boolean value accordingly
        '''
        bound_list = age_range.split("-") 
        bottom = int(bound_list[0])
        top = int(bound_list[1])
        if bottom-1 < self.age_at_death & self.age_at_death < top+1:
            return True
        else:
            return False

    def set_codes_list(self):
        '''
        Creates a list of the ICD-10 codes in relevant_data at the age_at_death and stores it in self.codes_list.
        '''
        self.codes_list = []
        for line in self.relevant_lines:
            if line.age == str(self.age_at_death):
                self.codes_list.append(line.code)

    def is_relevant_misc_line(self, line):
        '''
        Checks whether a line (DataLine object) from the misc data is relevant to the user
        
        Args:
            line: DataLine object containing misc data
        Returns:
            Boolean value in accordance with the conditional
        '''
        if self.equal_or_none(line.gender, self.search_args.gender) & \
            (line.code not in self.codes_list) & \
            (self.is_within_bounds(line.age)):
            return True
        else:
            return False

    def set_relevant_misc_lines(self):
        '''
        Creates a list of 'Miscellaneous' deaths to replace that is
        relevant to the user at the predicted age of death
        and stores it in self.relevant_misc_lines.
        '''
        self.relevant_misc_lines = []
        for line in self.misc_data:
            if self.is_relevant_misc_line(line):
                self.relevant_misc_lines.append(line)
                
    def set_misc_death_toll(self):
        '''
        Sums up the total number of miscellaneous deaths
        in self._relevant_misc_lines and stores it in 
        self.total_relevant_misc_deaths
        '''
        self.total_relevant_misc_deaths = 0
        for line in self.relevant_misc_lines:
            self.total_relevant_misc_deaths += int(line.death_toll)

    def flip(self, data):
        '''
        Takes in a list and reverses it
        
        Args:
            data: a list of DataLine objects
        Returns:
            the same list but reversed.
        '''
        new_list = []
        for i in range(len(data), 0, -1):
            new_list.append(data[i-1])
        return new_list

    def select_death(self, relevant_data, pick_number):
        '''
        Takes in relevant_data list, and then returns the line with the 
        the pick_number-th death contained in it from that list 
        counting from the upper end of the list

        Args:
            relevant_data: list of data relevant to the picking.
            pick_number: a integer that has been randomly generated
            laying between 0 and the total relevant death count
        Returns:
            the DataLine object that contains the predicted death
        '''    
        flipped_data = self.flip(relevant_data)
        line_num = 0
        for line in flipped_data:
            for i in range(int(line.death_toll)):
                line_num += 1
                if line_num == pick_number:
                    return line

    def find_random_death_circumstance(self, relevant_data, total_relevant_deaths):
        '''
        generates a number between 0 and the total number of relevant deaths
        and then uses select_death() to pick one and returns that
        
        Args: 
            relevant_data: a list of DataLine objects with relevant data
            total_relevant_deaths: the total number of deaths described in relevant_data
        Returns:
            a DataLine object with the cause of death and age
            at death that will be used in the prediction
        '''
        pick_number = random.randint(0, total_relevant_deaths)
        death_line = self.select_death(relevant_data, pick_number)
        return death_line

    def equal_or_none(self, compared, value):
        '''
        detects if compared and value are equal or value is None, returns True if so
        
        Args: 
            compared: main test subject value
            value: value as it would be found in search_args
        Returns:
            Boolean
        '''
        return (value == compared) or (value == None)

    def remove_zeros(self, number_string):
        '''
        Removes redundant zeros from inputs
        
        Args:
            number_string: a integer as a string
        Returns:
            the same string with any zeros removed from the front 
        '''
        while number_string[0] == '0':
            number_string = number_string[1:]
        return(number_string)

    def set_DoB(self, date_of_birth_list):
        '''
        Takes in date_of_birth_list and creates date object from datetime library. Stores it in self.date_of_birth
        
        Args:
            date_of_birth_list: the user's birthday split into month, day, and year
        '''
        birth_day = int(self.remove_zeros(date_of_birth_list[1]))
        birth_month = int(self.remove_zeros(date_of_birth_list[0]))
        birth_year = int(date_of_birth_list[2])
        self.date_of_birth = date(birth_year, birth_month, birth_day)

    def date_to_list(self, date):
        '''
        Takes in the data as the user wrote it and splices it into a list for further processing.
        
        Args:
            date: user input form of date
        Returns:
            date as a list [M, D, Y]
        '''
        list = str(date).split('/')
        return list

    def set_today(self):
        '''
        Stores current date in self.today
        '''
        self.today = date.today() 

    def set_age(self):
        '''
        Determines user's age using the current date and their birthday
        by subtracting the latter from the former.
        '''
        self.age_in_days = int(str(self.today - self.date_of_birth).split(' ')[0])
        self.age = int(self.age_in_days//365.25)
        self.search_args.age = self.age

    def set_age_and_DoB(self):
        '''
        Uses date_of_birth to determine age of user and stores that in age.
        '''
        self.set_DoB(self.date_to_list(self.input_arguments.birthday))
        self.set_age()

    def set_gender(self):
        '''
        Interprets user_input for gender as 'M', 'F', or None
        '''
        gender_user_input = self.input_arguments.gender
        if gender_user_input != 'M' and gender_user_input != 'F':
            gender_user_input = None
        self.search_args.gender, self.misc_search_args.gender = gender_user_input, gender_user_input
        
    def set_date_of_death(self):
        '''
        takes in date_of_birth and age_at_death and randomly chooses a date according to those parameters
        by adding a number between 0 and 365 of days to their last birthday.
        '''
        death_age_in_days = int(self.age_at_death*365.25)
        earliest_date_of_death = self.date_of_birth + timedelta(days = death_age_in_days)
        extra_days = random.randint(0, 364)
        self.date_of_death = earliest_date_of_death + timedelta(days = extra_days)

    def encode_string(self, string):
        '''
        Takes in a string and turns it into a string of numbers using the seed_influencer and their ascii values.
        
        Args:
            string: string that could be the name or DoB of the user.
        Returns:
            string of numbers determined but the original string.
        '''
        out_string = ''
        prev = self.seed_influencer
        for character in string:
            ascii_value = ord(character)
            rand_value = str(int(ascii_value * prev))
            prev = ascii_value
            out_string += rand_value
        return out_string

    def split_and_mix(self, string1, string2):
        '''
        Mixes two strings by splitting them both in half and merging
        the first half of the former with the second half of the latter.
        
        Args:
            String1: just a string
            String2: just another string
        Returns:
            The mixed string
        '''
        return string1[:len(string1)//2] + string2[len(string2)//2:]
        
    def generate_seed(self):
        '''
        Takes the name and DoB of the user and encodes them into long number
        strings that are then subtracted from eachother to create a seed number that is stored in self.seed
        '''
        inputs_string1 = self.split_and_mix(self.input_arguments.name, str(self.date_of_birth))
        inputs_string2 = self.split_and_mix(str(self.date_of_birth), self.input_arguments.name)
        encoded_number_1 = self.encode_string(inputs_string1)
        encoded_number_2 = self.encode_string(inputs_string2)
        self.seed = int(encoded_number_1)-int(encoded_number_2)

    def set_seed(self):
        '''
        sets the random seeding value to self.seed
        '''
        random.seed(self.seed)

    def set_base_prediction(self):
        '''
        creates a base prediction and stores it and its specific details
        '''
        self.base_death_line = self.find_random_death_circumstance(self.relevant_lines, self.total_relevant_deaths)
        self.age_at_death = int(self.base_death_line.age)
        self.set_date_of_death()

    def is_date_of_death_possible(self):
        '''
        checks whether the predicted date_of_death is earlier than today's date. If so, returns False
        
        Returns:
            Boolean
        '''
        difference = str(self.date_of_death - self.today)
        days_diff = int(difference.split(' ')[0])
        if days_diff > 0:
            return True
        else:
            return False

    def generate_base_prediction(self):
        '''
        makes base predictions until one is possible and stores that one.
        '''
        base_prediction_unverified = True
        while base_prediction_unverified:
            self.set_base_prediction()
            if self.is_date_of_death_possible():
                self.base_cause_of_death = self.base_death_line.cause
                base_prediction_unverified = False
            else:
                self.seed +=1
                self.set_seed()

    def needs_replacement(self):
        '''
        Checks whether the cause of death for the base prediction was vague. Returns True if so.
        
        Returns:
            Boolean
        '''
        if self.base_cause_of_death == "Miscellaneous" or self.base_cause_of_death == "Other ill-defined and unspecified causes of mortality":
            return True
        else:
            return False

    def prepare_misc_prediction(self):
        '''
        Prepares some lists and variables that are required for set_misc_prediction().
        '''
        self.set_codes_list()
        self.misc_search_args.age = self.age_at_death
        self.set_relevant_misc_lines()
        self.set_misc_death_toll()

    def set_misc_prediction(self):
        '''
        Selects a misc_death_line from relevant_misc_lines in the same manner as set_base_prediction does.
        '''
        self.misc_death_line = self.find_random_death_circumstance(self.relevant_misc_lines, self.total_relevant_misc_deaths)
        
    def generate_misc_prediction(self):
        '''
        Checks whether the base prediction needs replacement and if so, replaces it.
        '''
        if self.needs_replacement():
            self.prepare_misc_prediction()
            self.set_misc_prediction()
            self.needed_replacement = True
        else:
            self.needed_replacement = False

    def make_final_prediction(self):
        '''
        Creates and stores a Prediction object with the date of death, the cause of death, 
        the misc cause of death, and the age at death.
        '''
        if self.needed_replacement:
            misc_cause = self.misc_death_line.cause
        else:
            misc_cause = None
        self.final_prediction = Prediction(self.date_of_death, self.age_at_death, self.base_death_line.cause, misc_cause)

    def get_prediction(self):
        '''
        Returns a Prediction object based on the user's inputs.

        Returns:
            a Prediction object
        '''
        self.set_relevant_lines()
        self.set_death_toll()
        self.generate_base_prediction()
        self.generate_misc_prediction()
        self.make_final_prediction()
        return self.final_prediction

if __name__ == "__main__":
    seed_influencer = 1600.5
    input_list = argv[1:]
    predictor_1 = DeathPredictor(input_list, seed_influencer)
    prediction_1 = predictor_1.get_prediction()
    print(prediction_1.combined_cause, prediction_1.reformatted_date)
    prediction_1.get_days_remaining()