import unittest
from distance_calculator.calculator import calculate_distance_and_time_to_campuses

class TestDistanceCalculator(unittest.TestCase):

    def test_calculate_distance_and_time_to_campuses(self):
        street_address = "1600 Amphitheatre Parkway, Mountain View, CA"
        results = calculate_distance_and_time_to_campuses(street_address)
        self.assertIsNotNone(results)
        self.assertIn('North-West University', results)
        self.assertIn('University of Johannesburg', results)
        self.assertIn('Mafikeng', results['North-West University'])
        self.assertIn('Kingsway Campus', results['University of Johannesburg'])
        self.assertIn('driving', results['North-West University']['Mafikeng'])
        self.assertIn('distance', results['North-West University']['Mafikeng']['driving'])
        self.assertIn('duration', results['North-West University']['Mafikeng']['driving'])

if __name__ == '__main__':
    unittest.main()
