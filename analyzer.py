from typing import Dict, List, Tuple
from collections import Counter

class MatchAnalyzer:
    def __init__(self, puuid: str):
        self.puuid = puuid
    
    def extract_player_data(self, matches: List[Dict]) -> List[Dict]:
        """Extrai apenas os dados do jogador específico de cada partida"""
        player_matches = []
        
        for match in matches:
            participants = match.get('info', {}).get('participants', [])
            
            for participant in participants:
                if participant.get('puuid') == self.puuid:
                    player_data = {
                        'matchId': match.get('metadata', {}).get('matchId'),
                        'championName': participant.get('championName'),
                        'win': participant.get('win'),
                        'kills': participant.get('kills'),
                        'deaths': participant.get('deaths'),
                        'assists': participant.get('assists'),
                        'gameDuration': match.get('info', {}).get('gameDuration'),
                        'gameMode': match.get('info', {}).get('gameMode')
                    }
                    player_matches.append(player_data)
                    break
        
        return player_matches
    
    def get_top_champions_played(self, player_matches: List[Dict], top_n: int = 5) -> List[Tuple[str, int]]:
        """Retorna os N campeões mais jogados"""
        champions = [match['championName'] for match in player_matches]
        return Counter(champions).most_common(top_n)
    
    def get_top_champions_wins(self, player_matches: List[Dict], top_n: int = 5) -> List[Tuple[str, int]]:
        """Retorna os N campeões com mais vitórias"""
        winning_champions = [match['championName'] for match in player_matches if match['win']]
        return Counter(winning_champions).most_common(top_n)
    
    def get_top_champions_winrate(self, player_matches: List[Dict], top_n: int = 5) -> List[Tuple[str, float]]:
        """Retorna os N campeões com maior win rate"""
        champion_stats = {}
        
        for match in player_matches:
            champion = match['championName']
            if champion not in champion_stats:
                champion_stats[champion] = {'wins': 0, 'total': 0}
            
            champion_stats[champion]['total'] += 1
            if match['win']:
                champion_stats[champion]['wins'] += 1
        
        # Calcula win rate para todos os campeões
        winrates = []
        for champion, stats in champion_stats.items():
            winrate = stats['wins'] / stats['total']
            winrates.append((champion, winrate))
        
        return sorted(winrates, key=lambda x: x[1], reverse=True)[:top_n]