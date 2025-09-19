import requests
import json
import os
from typing import Dict, List, Optional

class RiotAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"X-Riot-Token": api_key}
        
    def get_account_by_riot_id(self, game_name: str, tag_line: str) -> Optional[Dict]:
        """Busca dados da conta pelo gameName e tagLine"""
        url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao buscar conta: {response.status_code}")
            return None
    
    def get_match_ids_by_puuid(self, puuid: str, count: int = 100) -> List[str]:
        """Busca IDs das partidas pelo PUUID"""
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {"count": count, "queue": 420, "type": "ranked"}
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao buscar partidas: {response.status_code}")
            return []
    
    def get_match_data(self, match_id: str) -> Optional[Dict]:
        """Busca dados detalhados de uma partida"""
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao buscar dados da partida {match_id}: {response.status_code}")
            return None