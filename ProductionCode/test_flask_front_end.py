from flask_front_end import *
import unittest

class TestFrontEnd(unittest.TestCase):
    
    def test_homepage(self):
        """ Test that the requested page loads correctly """
        self.app = app.test_client()
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'Welcome to Predictor of Passing!', response.data)

    def test_dp_route(self):
        """ Test that the requested page loads correctly """
        self.app = app.test_client()
        response = self.app.get('/dp', follow_redirects=True)
        self.assertIn(b'Which state would you like to see the number of deaths of?', response.data)

    def test_dp_state_route(self):
        """ Test that it can return the correct response for the data entered """
        self.app = app.test_client()
        response = self.app.get('/dp/choosestate?statechoice=Alabama', follow_redirects=True)
        self.assertIn(b'278943', response.data)
        
    def test_dp_state_route_and_function(self):
        """ Test that two functions have the same output for the same input """
        self.app = app.test_client()
        response = self.app.get('/dp/choosestate?statechoice=California', follow_redirects=True)
        state_data = get_state_data('dp', 'California')
        self.assertIn(str(state_data), str(response.data))

    def test_lc_route(self):
        """ Test that the requested page loads correctly """
        self.app = app.test_client()
        response = self.app.get('/lc', follow_redirects=True)
        self.assertIn(b'Which state would you like to see the leading cause of death of?', response.data)

    def test_lc_state_route(self):
        """ Test that it can return the correct response for the data entered """
        self.app = app.test_client()
        response = self.app.get('/lc/choosestate?statechoice=Alabama', follow_redirects=True)
        self.assertIn(b'Unspecified dementia', response.data)

    def test_get_state_data_dp(self):
        """ Test that it can return the correct data for the data entered """
        state_data = get_state_data('dp', 'Colorado')
        self.assertEqual(state_data, 200424)

    def test_get_state_data_lc(self):
        """ Test that it can return the correct data for the data entered """
        state_data = get_state_data('lc', 'Colorado')
        self.assertEqual(state_data, 'Chronic obstructive pulmonary disease, unspecified')

if __name__ == '__main__':
    unittest.main()