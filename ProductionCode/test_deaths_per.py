"""
Written By Kai R. Weiner
"""

import unittest
from deaths_per import *
import SearchInfo
from csv_reading import *

class TestSOMETHING(unittest.TestCase):

    def test_sum_deaths_by_state(self):
        """ Test that it can sum the data for one state """
        search = SearchInfo("California",None,None,None)
        result = deaths_per(search, deaths_data)
        self.assertEqual(result, 90)
    
    def test_sum_deaths_by_age(self):
        """ Test that it can sum the data for one age """
        search = SearchInfo(None,"37",None,None)
        result = deaths_per(search, deaths_data)
        self.assertEqual(result, 100)
    
    def test_sum_deaths_by_gender(self):
        """ Test that it can sum the data for one gender """
        search = SearchInfo(None,None,"M",None)
        result = deaths_per(search, deaths_data)
        self.assertEqual(result, 130)

    def test_sum_deaths_by_cause(self):
        """ Test that it can sum the data for one state """
        search = SearchInfo(None,None,None,"Infection")
        result = deaths_per(search, deaths_data)
        self.assertEqual(result, 70)

    def test_intersection_sum_deaths_by_age_and_gender(self):
        """ Test that it can sum the data for the intersection of age and gender """
        search = SearchInfo(None,"49","F",None)
        result = deaths_per(search, deaths_data)
        self.assertEqual(result, 70)
    
    def test_intersection_single_deaths_by_age_and_gender(self):
        """ Test that it can find the data for the intersection of age and gender """
        search = SearchInfo(None,"37","F",None)
        result = deaths_per(search, deaths_data)
        self.assertEqual(result, 20)

    def test_get_single_datapoint_all_terms(self):
        """ Test that it can sum the data for one search with all terms specified """
        search = SearchInfo("Nebraska","2","F","Infection")
        result = deaths_per(search, deaths_data)
        self.assertEqual(result, 20)
    
    def test_get_all_deaths(self):
        """ Test that it can sum of all deaths """
        search = SearchInfo(None,None,None,None)
        result = deaths_per(search, deaths_data)
        self.assertEqual(result, 270)

if __name__ == '__main__':
    initialized_file = read_CSV("Test Data CSV - Sheet1.csv")
    deaths_data = transform_CSV_data_to_array(initialized_file)
    unittest.main()