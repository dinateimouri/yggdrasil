import unittest
from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


class TestSyncChat(unittest.TestCase):
    def test_sync_chat_empty_prompts_list(self):
        """
        Test sync_chat function with empty prompts list scenario
        """
        response = client.post(
            "/sync-chat",
            data='{prompts=[], similarity_measure="cosine"}',
        )
        self.assertEqual(response.status_code, 422)

    def test_sync_chat_one_prompts_list(self):
        """
        Test sync_chat function with one prompts list scenario
        """
        response = client.post(
            "/sync-chat",
            data='{prompts=["d"], similarity_measure="cosine"}',
        )
        self.assertEqual(response.status_code, 422)

    def test_sync_chat_with_prompts_list_empty_strings(self):
        """
        Test sync_chat function with prompts list with empty strings scenario
        """
        response = client.post(
            "/sync-chat",
            data='{prompts=["", ""], similarity_measure="cosine"}',
        )
        self.assertEqual(response.status_code, 422)

    def test_sync_chat_with_prompts_list_no_strings(self):
        """
        Test sync_chat function with prompts list with no strings scenario
        """
        response = client.post(
            "/sync-chat",
            data='{prompts=[1, 2], similarity_measure="cosine"}',
        )
        self.assertEqual(response.status_code, 422)

    def test_sync_chat_with_invalid_similarity_measure(self):
        """
        Test sync_chat function with invalid similarity measure scenario
        """
        response = client.post(
            "/sync-chat",
            data='{prompts=["a", "b"], similarity_measure="invalid"}',
        )
        self.assertEqual(response.status_code, 422)
