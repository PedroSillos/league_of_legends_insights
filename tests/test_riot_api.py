import unittest
from unittest.mock import Mock, patch
from riot_api import RiotAPI

class TestRiotAPI(unittest.TestCase):
    def setUp(self):
        self.api = RiotAPI("fake_api_key")

    @patch('riot_api.requests.get')
    def test_get_account_by_riot_id_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"puuid": "test123", "gameName": "TestPlayer"}
        mock_get.return_value = mock_response

        result = self.api.get_account_by_riot_id("TestPlayer", "BR1")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["puuid"], "test123")

    @patch('riot_api.requests.get')
    @patch('builtins.print')
    def test_get_account_by_riot_id_failure(self, mock_print, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = self.api.get_account_by_riot_id("InvalidPlayer", "BR1")
        
        self.assertIsNone(result)
        mock_print.assert_called_once_with("Erro ao buscar conta: 404")

    @patch('riot_api.requests.get')
    def test_get_match_ids_with_correct_params(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = ["match1", "match2"]
        mock_get.return_value = mock_response

        result = self.api.get_match_ids_by_puuid("test_puuid", 100)
        
        expected_params = {"count": 100, "queue": 420, "type": "ranked"}
        mock_get.assert_called_with(
            unittest.mock.ANY, 
            headers=unittest.mock.ANY, 
            params=expected_params
        )
        self.assertEqual(len(result), 2)

    @patch('riot_api.requests.get')
    def test_get_match_data_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"metadata": {"matchId": "test_match"}}
        mock_get.return_value = mock_response

        result = self.api.get_match_data("test_match")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["metadata"]["matchId"], "test_match")

if __name__ == '__main__':
    unittest.main()