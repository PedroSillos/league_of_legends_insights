import unittest
import os
import json
import tempfile
from data_manager import DataManager

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_data.json")
        self.data_manager = DataManager(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_account_data(self):
        account_data = {"puuid": "test123", "gameName": "TestPlayer", "tagLine": "BR1"}
        self.data_manager.save_account_data(account_data)
        
        loaded_data = self.data_manager.load_data()
        self.assertEqual(len(loaded_data), 1)
        self.assertEqual(loaded_data[0]["puuid"], "test123")

    def test_no_duplicate_accounts(self):
        account_data = {"puuid": "test123", "gameName": "TestPlayer", "tagLine": "BR1"}
        self.data_manager.save_account_data(account_data)
        self.data_manager.save_account_data(account_data)
        
        loaded_data = self.data_manager.load_data()
        self.assertEqual(len(loaded_data), 1)

    def test_save_match_data(self):
        puuid = "test123"
        match_data = [{"metadata": {"matchId": "match1"}, "info": {"gameMode": "CLASSIC"}}]
        
        self.data_manager.save_match_data(puuid, match_data)
        loaded_matches = self.data_manager.load_match_data(puuid)
        
        self.assertEqual(len(loaded_matches), 1)
        self.assertEqual(loaded_matches[0]["metadata"]["matchId"], "match1")

    def test_load_nonexistent_file(self):
        result = self.data_manager.load_data()
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()