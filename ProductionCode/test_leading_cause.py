"""
Written by Tin Nguyen, Kai Weiner
"""

from leading_cause import *
import unittest
from SearchArgs import *

"""
The test class for return_leading_cause(arguement) checks whether the function captures the causes and number of deaths of said cause.
"""

class test_return_leading_cause(unittest.TestCase):

    def test_return_leading_cause_based_on_age(self): 
        """Test if return_leading_cause() can find and order the top causes of death of a given age"""
        search = SearchArgs(None,"37",None)
        result_age = return_leading_cause(search)
        sample_CoD_age = ["Person injured in collision between other specified motor vehicles (traffic)","Person injured in unspecified motor-vehicle accident, traffic","Assault by other and unspecified firearm discharge"]
        self.assertEqual(result_age, sample_CoD_age)

    def test_return_leading_cause_based_on_state(self): 
        """Test if return_leading_cause() can find and order the top causes of death of a given state"""
        search = SearchArgs("California",None,None)
        result_state = return_leading_cause(search)
        sample_CoD_state = ["Assault by handgun discharge","Intentional self-harm by other and unspecified firearm discharge","Assault by other and unspecified firearm discharge"]
        self.assertEqual(result_state, sample_CoD_state)
    
    def test_return_leading_cause_based_on_gender(self): 
        """Test if return_leading_cause() can find and order the top causes of death of a given gender"""
        search = SearchArgs(None,None,"F")
        result_gender = return_leading_cause(search)
        sample_CoD_gender = ["Assault by handgun discharge","Intentional self-harm by other and unspecified firearm discharge","Assault by other and unspecified firearm discharge"]
        self.assertEqual(result_gender, sample_CoD_gender)
        
    def test_return_leading_cause_based_on_ageGender(self): 
        """Test if return_leading_cause() can find and order the top causes of death of a given age and gender"""
        search = SearchArgs(None,"25","M")
        result_ageGender = return_leading_cause(search) 
        sample_CoD_ageGender = ["Assault by handgun discharge","Intentional self-harm by other and unspecified firearm discharge","Assault by other and unspecified firearm discharge"]
        self.assertEqual(result_ageGender, sample_CoD_ageGender)

    def test_find_return_leading_cause_based_on_genderLocation(self): 
        """Test if return_leading_cause() can find and order the top causes of death of a given gender and location"""
        search = SearchArgs("California",None,"M")
        result_genderLocation = return_leading_cause(search)
        sample_CoD_genderLocation = ["Assault by handgun discharge","Intentional self-harm by other and unspecified firearm discharge","Assault by other and unspecified firearm discharge"]
        self.assertEqual(result_genderLocation, sample_CoD_genderLocation)
    
    def test_find_return_leading_cause_based_on_ageLocation(self): 
        """Test if return_leading_cause() can find and order the top causes of death of a given age and location"""
        search = SearchArgs("California","25",None)
        result_ageLocation = return_leading_cause(self.age,self.state, "")
        sample_CoD_ageLocation = ["Assault by handgun discharge","Intentional self-harm by other and unspecified firearm discharge","Assault by other and unspecified firearm discharge"]
        self.assertEqual(result_ageLocation, sample_CoD_ageLocation)

    def test_find_return_leading_cause_based_on_genderAgeLocation(self):
        """Test if return_leading_cause() can find and order the top causes of death of a given age, location and gender"""
        search = SearchArgs("California","25","M")
        result = return_leading_cause(self.age,self.state,self.gender)
        sample_COD = ["Person injured in collision between other specified motor vehicles (traffic)","Person injured in unspecified motor-vehicle accident, traffic","Assault by other and unspecified firearm discharge"]
        self.assertEqual(result, sample_COD)
                

if __name__ == "__main__":
    unittest.main()
