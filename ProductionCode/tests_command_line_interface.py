"""
Written by Jonas Bartels
"""
import random
from B.ProductionCode.death_predictor import initialize_data
from command_line_interface import *
import unittest

class TestCLI(unittest.TestCase):
    def test_initialize_data(self):
        """ Tests that the data is properly initialized and formatted into 2D list """
        actual_result = initialize_data("Test Data CSV - Sheet1.csv")
        expected_result = [['California', '37', 'M', 'Heart Attack', 'A09.0', '80', '1000'], ['Alabama', '53', 'F', 'Cancer', 'A09.0', '30', '2000'], ['Nebraska', '2', 'F', 'Infection', 'A09.0', '20', '3000'], ['California', '49', 'F', 'Bullet Wound', 'A09.0', '10', '1500'], ['New Jersey', '20', 'M', 'Infection', 'A09.0', '50', '400'], ['New Jersey', '37', 'F', 'Heart Attack', 'A09.0', '20', '400'], ['New York', '49', 'F', 'Car Accident', 'A09.0', '60', '300']]
        assert_equal(self, actual_result, expected_result)

    def test_return_dictionary(self):
        """ Tests whether argument_dictionary is properly created """
        arguments = ['command_line_interface.py', 'deaths_per', '-a', '26', '-g', 'F']
        actual_result = return_dictionary_of_arguments(arguments)
        expected_result = {'state': None, 'age': '26', 'gender': 'F', 'cause': None}
        assert_equal(self, actual_result, expected_result)

    def test_create_search_info(self):
        """ Tests if the SearchInfo object is created and contains the correct info """
        arguments = ['command_line_interface.py', 'lc', '-s', 'New Jersey', '-g', 'M']
        result_object = create_search_info(arguments)
        actual_result = [result_object.state, result_object.age, result_object.gender, result_object.cause]
        expected_result = ['New Jersey', None, 'M', None]
        assert_equal(self, actual_result, expected_result)

    def test_find_deaths_per(self):
        """ Tests if find_deaths_per successfully combines the functions tested above so that they output the correct integer value"""
        arguments = ['command_line_interface.py', 'dp', '-s', 'New Jersey', '-a', '34', '-g', 'F']
        dataset_name = 'data.csv'
        actual_result = find_deaths_per(arguments, dataset_name)
        expected_result = 266
        assert_equal(self, actual_result, expected_result)

    def test_find_leading_cause(self):
        """ Tests if find_leading_cause successfully combines the functions tested above so that they output a list with the correct cause and number of people afflicted """
        arguments = ['command_line_interface.py', 'leading_cause','-s', 'Alabama', '-a', '46', '-g', 'M']
        dataset_name = 'data.csv'
        actual_result = find_leading_cause(arguments, dataset_name)
        expected_result = ['Cardiac arrest, unspecified', 46]
        assert_equal(self, actual_result, expected_result)

    def test_determine_and_execute_call(self):
        """ Tests if the arguments are properly recognized and appropiate values are returned"""
        arguments_lists_to_test = [['command_line_interface.py','dp', '--age', '54'], ['command_line_interface.py', 'leading_cause', '--gender', 'F'], ['command_line_interface.py', 'deaths_per', '--state', 'New York'], ['command_line_interface.py', 'lc', '--gender', 'F','-s','Florida'], ['command_line_interface.py', 'dp', '-a', '66']]
        dataset_name = 'data.csv'
        expected_results = [127377, ['Alzheimer disease, unspecified', 406313], 826491, ['Atherosclerotic heart disease', 30922], 250668]
        i = 0

        for arguments in arguments_lists_to_test:
            actual_result = determine_and_execute_call(arguments, dataset_name)
            expected_result = expected_results[i]
            assert_equal(self,actual_result,expected_result)
            i+=1

def assert_equal(self, result, expected_result):
    self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()