from typing import List, Tuple

class DataVisualizer:
    def __init__(self):
        pass
        
    def plot_top_champions_played(self, data: List[Tuple[str, int]], title: str = "Top 5 Campeões Mais Jogados"):
        """Exibe dados dos campeões mais jogados em formato texto"""
        if not data:
            print("Nenhum dado disponível para visualização")
            return
            
        print(f"\n{title}")
        print("=" * len(title))
        for i, (champion, count) in enumerate(data, 1):
            bar = "█" * min(count, 20)  # Barra visual simples
            print(f"{i:2d}. {champion:15s} │{bar:<20s}│ {count} jogos")
    
    def plot_top_champions_wins(self, data: List[Tuple[str, int]], title: str = "Top 5 Campeões com Mais Vitórias"):
        """Exibe dados dos campeões com mais vitórias em formato texto"""
        if not data:
            print("Nenhum dado disponível para visualização")
            return
            
        print(f"\n{title}")
        print("=" * len(title))
        for i, (champion, wins) in enumerate(data, 1):
            bar = "█" * min(wins, 20)  # Barra visual simples
            print(f"{i:2d}. {champion:15s} │{bar:<20s}│ {wins} vitórias")
    
    def plot_top_champions_winrate(self, data: List[Tuple[str, float]], title: str = "Top 5 Campeões com Maior Win Rate"):
        """Exibe dados dos campeões com maior win rate em formato texto"""
        if not data:
            print("Nenhum dado disponível para visualização")
            return
            
        print(f"\n{title}")
        print("=" * len(title))
        for i, (champion, winrate) in enumerate(data, 1):
            wr_percent = winrate * 100
            bar_length = int(wr_percent / 5)  # Escala para 20 caracteres max
            bar = "█" * bar_length
            print(f"{i:2d}. {champion:15s} │{bar:<20s}│ {wr_percent:.1f}%")