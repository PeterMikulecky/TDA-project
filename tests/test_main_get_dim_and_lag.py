import unittest
from io import StringIO
import sys
import os

# Add the 'src' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import get_dimension_and_lag


class TestUserInput(unittest.TestCase):
        def test_valid_integer_inputs(self):
            inputs = iter(['3', '5'])
            dimension, lag = get_dimension_and_lag(input_func=lambda prompt: next(inputs))
            self.assertEqual(dimension, 3)
            self.assertEqual(lag, 5)
    
        def test_non_integer_input(self):
            inputs = iter(['abc', '3', '5'])
            output = StringIO()
            sys.stdout = output  # Redirect stdout to capture print statements
    
            dimension, lag = get_dimension_and_lag(input_func=lambda prompt: next(inputs))
    
            sys.stdout = sys.__stdout__  # Reset stdout back to default
            self.assertEqual(dimension, 3)  # Ensure the valid input '3' is processed correctly for dimension
            self.assertEqual(lag, 5)        # Ensure the valid input '5' is processed correctly for lag
            self.assertIn("Invalid input. Please enter an integer value.", output.getvalue())
    
        def test_negative_integer_input(self):
            inputs = iter(['-3', '-5', '2', '2'])
            output = StringIO()
            sys.stdout = output  # Redirect stdout to capture print statements
    
            dimension, lag = get_dimension_and_lag(input_func=lambda prompt: next(inputs))
    
            sys.stdout = sys.__stdout__  # Reset stdout back to default
            self.assertEqual(dimension, 2)
            self.assertEqual(lag, 2)
            self.assertIn("Both dimension and lag must be positive integers. Please try again.", output.getvalue())
    
if __name__ == "__main__":
    unittest.main()
