import unittest
from distance_calculator.calculator import calculate_distance_and_time_to_campuses

class TestDistanceCalculator(unittest.TestCase):

    def test_calculate_distance_and_time_to_campuses(self):
        street_address = "Your test address here"
        results = calculate_distance_and_time_to_campuses(street_address)
        self.assertIsNotNone(results)
        self.assertIn('Mafikeng', results)
        self.assertIn('driving', results['Mafikeng'])
        self.assertIn('distance', results['Mafikeng']['driving'])
        self.assertIn('duration', results['Mafikeng']['driving'])

if __name__ == '__main__':
    unittest.main()
