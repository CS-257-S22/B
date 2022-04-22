"""
Written by Tin Nguyen, Kai Weiner
"""

import unittest
import SearchInfo

# The test class for leading_cause(arguement) checks whether the function captures the causes and number of deaths of said cause. The function additionally will call a help method to order and return the top causes.   

class test_leading_cause(unittest.TestCase):

    def test_leading_cause_based_on_age(self): 
        """Test if leading_cause() can find and order the top causes of death of a given age"""
        search = SearchInfo(None,"37",None)
        result_age = leading_cause(search)
        sample_CoD_age = ["Person injured in collision between other specified motor vehicles (traffic)","Person injured in unspecified motor-vehicle accident, traffic","Assault by other and unspecified firearm discharge"]
        self.assertEqual(result_age, sample_CoD_age)

    def test_leading_cause_based_on_state(self): 
        """Test if leading_cause() can find and order the top causes of death of a given state"""
        search = SearchInfo("California",None,None)
        result_state = leading_cause(search)
        sample_CoD_state = ["Assault by handgun discharge","Intentional self-harm by other and unspecified firearm discharge","Assault by other and unspecified firearm discharge"]
        self.assertEqual(result_state, sample_CoD_state)
    
    def test_leading_cause_based_on_gender(self): 
        """Test if leading_cause() can find and order the top causes of death of a given gender"""
        search = SearchInfo(None,None,"F")
        result_gender = leading_cause(search)
        sample_CoD_gender = ["Assault by handgun discharge","Intentional self-harm by other and unspecified firearm discharge","Assault by other and unspecified firearm discharge"]
        self.assertEqual(result_gender, sample_CoD_gender)
        
    def test_leading_cause_based_on_ageGender(self): 
        """Test if leading_cause() can find and order the top causes of death of a given age and gender"""
        search = SearchInfo(None,"25","M")
        result_ageGender = leading_cause(search) 
        sample_CoD_ageGender = ["Assault by handgun discharge","Intentional self-harm by other and unspecified firearm discharge","Assault by other and unspecified firearm discharge"]
        self.assertEqual(result_ageGender, sample_CoD_ageGender)

    def test_find_leading_cause_based_on_genderLocation(self): 
        """Test if leading_cause() can find and order the top causes of death of a given gender and location"""
        search = SearchInfo("California",None,"M")
        result_genderLocation = leading_cause(search)
        sample_CoD_genderLocation = ["Assault by handgun discharge","Intentional self-harm by other and unspecified firearm discharge","Assault by other and unspecified firearm discharge"]
        self.assertEqual(result_genderLocation, sample_CoD_genderLocation)
    
    def test_find_leading_cause_based_on_ageLocation(self): 
        """Test if leading_cause() can find and order the top causes of death of a given age and location"""
        search = SearchInfo("California","25",None)
        result_ageLocation = leading_cause(self.age,self.state, "")
        sample_CoD_ageLocation = ["Assault by handgun discharge","Intentional self-harm by other and unspecified firearm discharge","Assault by other and unspecified firearm discharge"]
        self.assertEqual(result_ageLocation, sample_CoD_ageLocation)

    def test_find_leading_cause_based_on_genderAgeLocation(self):
        """Test if leading_cause() can find and order the top causes of death of a given age, location and gender"""
        search = SearchInfo("California","25","M")
        result = leading_cause(self.age,self.state,self.gender)
        sample_COD = ["Person injured in collision between other specified motor vehicles (traffic)","Person injured in unspecified motor-vehicle accident, traffic","Assault by other and unspecified firearm discharge"]
        self.assertEqual(result, sample_COD)
                

if __name__ == "__main__":
    unittest.main()
