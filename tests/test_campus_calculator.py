import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

from distance_calculator.campus_calculator import (
    find_nearest_campus,
    update_nearest_campus_in_db,
    print_results_from_db,
    Accommodation,
    UJ_CAMPUS_ADDRESSES,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestCampusCalculator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        cls.engine = create_engine('sqlite:///:memory:')
        Accommodation.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()

    def tearDown(self):
        self.session.rollback()  
        self.session.close()

    @patch('distance_calculator.google_maps.get_geocode')  
    def test_find_nearest_campus_success(self, mock_geocode):
        # Mock geocoding results (using data from the PDF)
        mock_geocode.side_effect = [
            [{'geometry': {'location': {'lat': -26.1685, 'lng': 28.0633}}}],  # Accommodation (e.g., 17 Putney)
            [{'geometry': {'location': {'lat': -26.18132, 'lng': 28.03946}}}],   # Kingsway Campus
        ]

        nearest_campus = find_nearest_campus("17 Putney Johannesburg", UJ_CAMPUS_ADDRESSES)
        self.assertEqual(nearest_campus, 'Kingsway Campus')

    @patch('distance_calculator.google_maps.get_geocode')  
    def test_find_nearest_campus_no_results(self, mock_geocode):
        mock_geocode.return_value = [] 
        nearest_campus = find_nearest_campus("Invalid Address", UJ_CAMPUS_ADDRESSES)
        self.assertIsNone(nearest_campus)

    def test_update_nearest_campus_in_db(self):
        # Add a test accommodation to the database
        accommodation = Accommodation(id=1, university='UJ', Street_Address='17 Putney Johannesburg', Nearest_Campus=None)
        self.session.add(accommodation)
        self.session.commit()

        update_nearest_campus_in_db(1, 'Kingsway Campus')

        # Query the database to verify the update
        updated_accommodation = self.session.query(Accommodation).get(1)
        self.assertEqual(updated_accommodation.Nearest_Campus, 'Kingsway Campus')

    def test_print_results_from_db(self):
        # Add test accommodations to the database
        accommodations = [
            Accommodation(id=1, university='UJ', Street_Address='17 Putney Johannesburg', Nearest_Campus='Kingsway Campus'),
            Accommodation(id=2, university='UJ', Street_Address='40 Portland Str Hursthill', Nearest_Campus='Bunting Road Campus'),
        ]
        self.session.add_all(accommodations)
        self.session.commit()

        # Capture printed output
        with patch('sys.stdout', new=StringIO()) as fake_output:
            print_results_from_db()
            output = fake_output.getvalue().strip()

        expected_output = (
            "Accommodation ID 1 - Nearest Campus: Kingsway Campus\n"
            "Accommodation ID 2 - Nearest Campus: Bunting Road Campus"
        )
        self.assertEqual(output, expected_output)
