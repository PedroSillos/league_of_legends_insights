import json
import os
from typing import Dict, List

class DataManager:
    def __init__(self, data_file: str = "player_data.json"):
        self.data_file = data_file
        
    def save_account_data(self, account_data: Dict):
        """Salva dados da conta no arquivo local"""
        existing_data = self.load_data()
        
        # Verifica se o PUUID já existe
        puuid = account_data.get('puuid')
        if not any(player.get('puuid') == puuid for player in existing_data):
            existing_data.append(account_data)
            
        with open(self.data_file, 'w') as f:
            json.dump(existing_data, f, indent=2)
    
    def load_data(self) -> List[Dict]:
        """Carrega dados existentes do arquivo"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_match_data(self, puuid: str, match_data: List[Dict]):
        """Salva dados das partidas para um PUUID específico"""
        filename = f"matches_{puuid}.json"
        
        existing_matches = []
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                existing_matches = json.load(f)
        
        # Adiciona apenas partidas novas
        existing_match_ids = {match.get('metadata', {}).get('matchId') for match in existing_matches}
        new_matches = [match for match in match_data if match.get('metadata', {}).get('matchId') not in existing_match_ids]
        
        existing_matches.extend(new_matches)
        
        with open(filename, 'w') as f:
            json.dump(existing_matches, f, indent=2)
    
    def load_match_data(self, puuid: str) -> List[Dict]:
        """Carrega dados das partidas para um PUUID específico"""
        filename = f"matches_{puuid}.json"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return []