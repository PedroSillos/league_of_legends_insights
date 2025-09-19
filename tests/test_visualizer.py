import unittest
from unittest.mock import patch
from io import StringIO
from visualizer import DataVisualizer

class TestDataVisualizer(unittest.TestCase):
    def setUp(self):
        self.visualizer = DataVisualizer()

    @patch('sys.stdout', new_callable=StringIO)
    def test_plot_top_champions_played(self, mock_stdout):
        data = [('Jinx', 10), ('Caitlyn', 8), ('Ashe', 5)]
        self.visualizer.plot_top_champions_played(data)
        
        output = mock_stdout.getvalue()
        self.assertIn('Top 5 Campeões Mais Jogados', output)
        self.assertIn('Jinx', output)
        self.assertIn('10 jogos', output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_plot_top_champions_wins(self, mock_stdout):
        data = [('Jinx', 7), ('Caitlyn', 5)]
        self.visualizer.plot_top_champions_wins(data)
        
        output = mock_stdout.getvalue()
        self.assertIn('Top 5 Campeões com Mais Vitórias', output)
        self.assertIn('7 vitórias', output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_plot_top_champions_winrate(self, mock_stdout):
        data = [('Jinx', 0.75), ('Caitlyn', 0.60)]
        self.visualizer.plot_top_champions_winrate(data)
        
        output = mock_stdout.getvalue()
        self.assertIn('Top 5 Campeões com Maior Win Rate', output)
        self.assertIn('75.0%', output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_empty_data_handling(self, mock_stdout):
        self.visualizer.plot_top_champions_played([])
        
        output = mock_stdout.getvalue()
        self.assertIn('Nenhum dado disponível', output)

if __name__ == '__main__':
    unittest.main()