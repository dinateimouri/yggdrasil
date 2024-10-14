import unittest
from api.utils import profanity_replace, handle_harmful_content


class test_profanity_replace(unittest.TestCase):
    def test_file_not_found(self):
        """
        Test profanity_replacement function with file not found scenario
        """
        self.assertNotEqual(
            profanity_replace("This is a test"),
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
            profanity_replace("This is a test"),
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
            profanity_replace("5hit"),
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
            profanity_replace(""),
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
            profanity_replace(123),
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
            profanity_replace(None),
            {
                'message': 'The input is not Valid',
                'profanity_found': False,
                'successful': False,
            },
        )


class TestHandleHarmfulContent(unittest.TestCase):
    def test_invalid_text_input(self):
        """
        Test handle_harmful_content function with invalid input scenario
        """
        self.assertIsNone(handle_harmful_content("pipe", None))

    def test_invalid_pipeline_input(self):
        """
        Test handle_harmful_content function with invalid text input scenario
        """
        self.assertIsNone(handle_harmful_content("pipe", "text"))
