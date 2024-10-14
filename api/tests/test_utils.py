import unittest
from api.utils import (
    profanity_replace,
    detect_harmful_content,
    similarity_cosine,
    similarity_euclidean,
)


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
        self.assertIsNone(detect_harmful_content("pipe", None))

    def test_invalid_pipeline_input(self):
        """
        Test handle_harmful_content function with invalid text input scenario
        """
        self.assertIsNone(detect_harmful_content("pipe", "text"))


class TestSimilarityCosine(unittest.TestCase):
    def test_similarity_cosine_non_list_input(self):
        """
        Test similarity_cosine function with non-list input scenario
        """
        self.assertDictEqual(
            similarity_cosine("input"),
            {
                'similarity_matrix': None,
                'successful': False,
            },
        )

    def test_similarity_cosine_empty_list_input(self):
        """
        Test similarity_cosine function with empty list input scenario
        """
        self.assertDictEqual(
            similarity_cosine([]),
            {
                'similarity_matrix': None,
                'successful': False,
            },
        )

    def test_similarity_cosine_same_input(self):
        """
        Test similarity_cosine function with same input scenario
        """
        self.assertDictEqual(
            similarity_cosine(["input1", "input1"]),
            {
                'similarity_matrix': {
                    "input1": {"input1": 1.0},
                },
                'successful': True,
            },
        )

    def test_similarity_cosine_not_string_input(self):
        """
        Test similarity_cosine function with not string input scenario
        """
        self.assertDictEqual(
            similarity_cosine([123, 123]),
            {
                'similarity_matrix': None,
                'successful': False,
            },
        )

    def test_similarity_cosine_different_input(self):
        """
        Test similarity_cosine function with different input scenario
        """
        self.assertDictEqual(
            similarity_cosine(["input1", "input2"]),
            {
                'similarity_matrix': {
                    'input1': {
                        'input1': 1.0,
                        'input2': 0.0,
                    },
                    'input2': {
                        'input1': 0.0,
                        'input2': 1.0,
                    },
                },
                'successful': True,
            },
        )


class TestSimilarityEuclidean(unittest.TestCase):
    def test_similarity_euclidean_non_list_input(self):
        """
        Test similarity_euclidean function with non-list input scenario
        """
        self.assertDictEqual(
            similarity_euclidean("input"),
            {
                'similarity_matrix': None,
                'successful': False,
            },
        )

    def test_similarity_euclidean_empty_list_input(self):
        """
        Test similarity_euclidean function with empty list input scenario
        """
        self.assertDictEqual(
            similarity_euclidean([]),
            {
                'similarity_matrix': None,
                'successful': False,
            },
        )

    def test_similarity_euclidean_same_input(self):
        """
        Test similarity_euclidean function with same input scenario
        """
        self.assertDictEqual(
            similarity_euclidean(["input1", "input1"]),
            {
                'similarity_matrix': {
                    "input1": {"input1": 1.0},
                },
                'successful': True,
            },
        )

    def test_similarity_euclidean_not_string_input(self):
        """
        Test similarity_euclidean function with not string input scenario
        """
        self.assertDictEqual(
            similarity_euclidean([123, 123]),
            {
                'similarity_matrix': None,
                'successful': False,
            },
        )

    def test_similarity_euclidean_different_input(self):
        """
        Test similarity_euclidean function with different input scenario
        """
        self.assertDictEqual(
            similarity_euclidean(["input1", "input2"]),
            {
                'similarity_matrix': {
                    'input1': {
                        'input1': 0.0,
                        'input2': 1.4142135623730951,
                    },
                    'input2': {
                        'input1': 1.4142135623730951,
                        'input2': 0.0,
                    },
                },
                'successful': True,
            },
        )
