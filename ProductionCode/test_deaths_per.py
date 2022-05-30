"""
Written By Kai R. Weiner
"""

import unittest
from webbrowser import get
from deaths_per import *
from SearchArgs import *
from csv_reading import *

class TestSOMETHING(unittest.TestCase):

    def test_sum_deaths_by_state(self):
        """ Test that it can sum the data for one state """
        search = SearchArgs("California",None,None,None)
        result = get_deaths_per_arguments(deaths_data, search)
        self.assertEqual(result, 90)
    
    def test_sum_deaths_by_age(self):
        """ Test that it can sum the data for one age """
        search = SearchArgs(None,"37",None,None)
        result = get_deaths_per_arguments(deaths_data, search)
        self.assertEqual(result, 100)
    
    def test_sum_deaths_by_gender(self):
        """ Test that it can sum the data for one gender """
        search = SearchArgs(None,None,"M",None)
        result = get_deaths_per_arguments(deaths_data, search)
        self.assertEqual(result, 130)

    def test_sum_deaths_by_cause(self):
        """ Test that it can sum the data for one state """
        search = SearchArgs(None,None,None,"Infection")
        result = get_deaths_per_arguments(deaths_data, search)
        self.assertEqual(result, 70)

    def test_intersection_sum_deaths_by_age_and_gender(self):
        """ Test that it can sum the data for the intersection of age and gender """
        search = SearchArgs(None,"49","F",None)
        result = get_deaths_per_arguments(deaths_data, search)
        self.assertEqual(result, 70)
    
    def test_intersection_single_deaths_by_age_and_gender(self):
        """ Test that it can find the data for the intersection of age and gender """
        search = SearchArgs(None,"37","F",None)
        result = get_deaths_per_arguments(deaths_data, search)
        self.assertEqual(result, 20)

    def test_get_single_datapoint_all_terms(self):
        """ Test that it can sum the data for one search with all terms specified """
        search = SearchArgs("Nebraska","2","F","Infection")
        result = get_deaths_per_arguments(deaths_data, search)
        self.assertEqual(result, 20)
    
    def test_get_all_deaths(self):
        """ Test that it can sum of all deaths """
        search = SearchArgs(None,None,None,None)
        result = get_deaths_per_arguments(deaths_data, search)
        self.assertEqual(result, 270)

if __name__ == '__main__':
    deaths_data = get_CSV_data_as_list("Test Data CSV - Sheet1.csv")
    unittest.main()