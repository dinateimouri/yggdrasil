import unittest
from api.utils import profanity_replacement


class test_profanity_replacement(unittest.TestCase):
    def test_file_not_found(self):
        """
        Test profanity_replacement function with file not found scenario
        """
        self.assertNotEqual(
            profanity_replacement("This is a test"),
            {
                'message': 'Profanity list not found',
                'profanity_found': False,
                'successful': False,
            },
        )

    def test_no_profanity(self):
        """
        Test profanity_replacement function with no profanity word scenario
        """
        self.assertEqual(
            profanity_replacement("This is a test"),
            {
                'message': 'This is a test',
                'profanity_found': False,
                'successful': True,
            },
        )

    def test_profanity(self):
        """
        Test profanity_replacement function with profanity word scenario
        """
        self.assertEqual(
            profanity_replacement("5hit"),
            {
                'message': '****',
                'profanity_found': True,
                'successful': True,
            },
        )

    def test_empty_input(self):
        """
        Test profanity_replacement function with empty input scenario
        """
        self.assertEqual(
            profanity_replacement(""),
            {
                'message': '',
                'profanity_found': False,
                'successful': True,
            },
        )

    def test_int_input(self):
        """
        Test profanity_replacement function with int input scenario
        """
        self.assertEqual(
            profanity_replacement(123),
            {
                'message': '123',
                'profanity_found': False,
                'successful': True,
            },
        )

    def test_invalid_input(self):
        """
        Test profanity_replacement function with invalid input scenario
        """
        self.assertEqual(
            profanity_replacement(None),
            {
                'message': 'The input is not Valid',
                'profanity_found': False,
                'successful': False,
            },
        )
