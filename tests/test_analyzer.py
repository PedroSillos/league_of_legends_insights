import unittest
from analyzer import MatchAnalyzer

class TestMatchAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = MatchAnalyzer("test_puuid")
        self.sample_matches = [
            {'championName': 'Jinx', 'win': True, 'kills': 10, 'deaths': 2, 'assists': 5},
            {'championName': 'Jinx', 'win': False, 'kills': 3, 'deaths': 8, 'assists': 2},
            {'championName': 'Caitlyn', 'win': True, 'kills': 8, 'deaths': 1, 'assists': 7},
            {'championName': 'Ashe', 'win': True, 'kills': 5, 'deaths': 3, 'assists': 12},
        ]

    def test_get_top_champions_played(self):
        result = self.analyzer.get_top_champions_played(self.sample_matches, 2)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], 'Jinx')
        self.assertEqual(result[0][1], 2)

    def test_get_top_champions_wins(self):
        result = self.analyzer.get_top_champions_wins(self.sample_matches, 3)
        self.assertEqual(len(result), 3)
        self.assertIn(('Jinx', 1), result)
        self.assertIn(('Caitlyn', 1), result)
        self.assertIn(('Ashe', 1), result)

    def test_get_top_champions_winrate_with_filter(self):
        result = self.analyzer.get_top_champions_winrate(self.sample_matches, 5)
        self.assertEqual(len(result), 3)
        jinx_winrate = next((wr for champ, wr in result if champ == 'Jinx'), None)
        self.assertEqual(jinx_winrate, 0.5)

    def test_extract_player_data(self):
        mock_matches = [{
            'metadata': {'matchId': 'test1'},
            'info': {
                'participants': [{
                    'puuid': 'test_puuid',
                    'championName': 'Jinx',
                    'win': True,
                    'kills': 10,
                    'deaths': 2,
                    'assists': 5,
                    'gameDuration': 1800,
                    'gameMode': 'CLASSIC'
                }]
            }
        }]
        
        result = self.analyzer.extract_player_data(mock_matches)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['championName'], 'Jinx')
        self.assertTrue(result[0]['win'])

    def test_empty_matches(self):
        result = self.analyzer.get_top_champions_played([], 5)
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()