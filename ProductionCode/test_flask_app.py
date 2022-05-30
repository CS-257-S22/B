"""
Written by Kai Weiner
"""

import unittest
from flask_app import *
from csv_reading import *

"""
The test suite for flask app
"""

class test_return_leading_cause(unittest.TestCase):

    def test_sum_deaths_per_by_state(self):
        """ Test that it can sum the death data for one state """
        result = get_response("deaths_per", "(-s%20California)")
        self.assertEqual(result, "The number of people who died under the category: state = California, age = all, gender = all, cause = all, is: 90.")

    def test_sum_deaths_per_by_age(self):
        """ Test that it can sum the death data for one age """
        result = get_response("dp", "(-a%2037)")
        self.assertEqual(result, "The number of people who died under the category: state = all, age = 37, gender = all, cause = all, is: 100.")

    def test_sum_deaths_per_by_gender(self):
        """ Test that it can sum the death data for one gender """
        result = get_response("deaths_per", "(-g%20M)")
        self.assertEqual(result, "The number of people who died under the category: state = all, age = all, gender = M, cause = all, is: 130.")

    def test_sum_deaths_per_by_cause(self):
        """ Test that it can sum the death data for one cause of death """
        result = get_response("dp", "(-c%20Infection)")
        self.assertEqual(result, "The number of people who died under the category: state = all, age = all, gender = all, cause = Infection, is: 70.")

    def test_intersection_sum_deaths_per_by_age_and_gender(self):
        """ Test that it can sum the death data for the intersection of age and gender """
        result = get_response("deaths_per", "(-a%2049%20-g%20F)")
        self.assertEqual(result, "The number of people who died under the category: state = all, age = 49, gender = F, cause = all, is: 70.")

    def test_intersection_single_deaths_per_by_age_and_gender(self):
        """ Test that it can find the death data for the intersection of age and gender """
        result = get_response("dp", "(-g%20F%20-a%2037)")
        self.assertEqual(result, "The number of people who died under the category: state = all, age = 37, gender = F, cause = all, is: 20.")

    def test_get_single_datapoint_deaths_per_all_terms(self):
        """ Test that it can sum the death data for one search with all terms specified """
        result = get_response("deaths_per", "(-c%20Infection%20-a%202%20-s%20Nebraska%20-g%20F)")
        self.assertEqual(result, "The number of people who died under the category: state = Nebraska, age = 2, gender = F, cause = Infection, is: 20.")

    def test_deaths_per_all_datapoints(self):
        """ Test that it can sum of all deaths """
        result = get_response("dp", "(all)")
        self.assertEqual(result, "The number of people who died under the category: state = all, age = all, gender = all, cause = all, is: 270.")

    def test_sum_leading_cause_based_on_state(self): 
        """ Test if return_leading_cause() can find the top causes of death of a given state """
        result = get_response("leading_cause", "(-s%20New%20Jersey)")
        self.assertEqual(result, "The leading cause of death for people under the category: state = New Jersey, age = all, gender = all, is: Infection, which was responsible for the deaths of 50 people in this catergory.")

    def test_sum_leading_cause_based_on_age(self): 
        """ Test if return_leading_cause() can find the top causes of death of a given age """
        result = get_response("lc", "(-a%2049)")
        self.assertEqual(result, "The leading cause of death for people under the category: state = all, age = 49, gender = all, is: Car Accident, which was responsible for the deaths of 60 people in this catergory.")

    def test_sum_leading_cause_based_on_gender(self): 
        """ Test if return_leading_cause() can find the top causes of death of a given gender """
        result = get_response("leading_cause", "(-g%20M)")
        self.assertEqual(result, "The leading cause of death for people under the category: state = all, age = all, gender = M, is: Heart Attack, which was responsible for the deaths of 80 people in this catergory.")

    def test_intersection_sum_leading_cause_by_age_and_gender(self):
        """ Test if return_leading_cause() can find the top causes of death of a given age and gender that multiple datapoints fall under """
        result = get_response("lc", "(-a%2049%20-g%20F)")
        self.assertEqual(result, "The leading cause of death for people under the category: state = all, age = 49, gender = F, is: Car Accident, which was responsible for the deaths of 60 people in this catergory.")

    def test_intersection_single_leading_cause_by_age_and_gender(self):
        """ Test if return_leading_cause() can find the top causes of death of a given age and gender that a single datapoint falls under """
        result = get_response("leading_cause", "(-g%20F%20-a%2037)")
        self.assertEqual(result, "The leading cause of death for people under the category: state = all, age = 37, gender = F, is: Heart Attack, which was responsible for the deaths of 20 people in this catergory.")

    def test_get_single_datapoint_leading_cause_all_terms(self):
        """ Test if return_leading_cause() can find the top causes of death for an individual datapoint """
        result = get_response("lc", "(-g%20F%20-s%20Alabama%20-a%2053)")
        self.assertEqual(result, "The leading cause of death for people under the category: state = Alabama, age = 53, gender = F, is: Cancer, which was responsible for the deaths of 30 people in this catergory.")

    def test_leading_cause_all_datapoints(self):
        """ Test if return_leading_cause() can find the top causes of death for the whole dataset """
        result = get_response("leading_cause", "(all)")
        self.assertEqual(result, "The leading cause of death for people under the category: state = all, age = all, gender = all, is: Heart Attack, which was responsible for the deaths of 100 people in this catergory.")

if __name__ == '__main__':
    unittest.main()