import json
import boto3
import os
from analyzer import MatchAnalyzer
from data_manager import DataManager

s3_client = boto3.client('s3')
S3_BUCKET = os.environ.get('S3_BUCKET')

class S3DataManager(DataManager):
    """Data manager que usa S3 ao invés de arquivos locais"""
    
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        super().__init__("player_data.json")
    
    def load_data(self):
        try:
            response = s3_client.get_object(Bucket=self.bucket_name, Key="player_data.json")
            return json.loads(response['Body'].read())
        except:
            return []
    
    def save_account_data(self, account_data):
        existing_data = self.load_data()
        puuid = account_data.get('puuid')
        if not any(player.get('puuid') == puuid for player in existing_data):
            existing_data.append(account_data)
        
        s3_client.put_object(
            Bucket=self.bucket_name,
            Key="player_data.json",
            Body=json.dumps(existing_data, indent=2)
        )
    
    def load_match_data(self, puuid):
        try:
            response = s3_client.get_object(Bucket=self.bucket_name, Key=f"matches_{puuid}.json")
            return json.loads(response['Body'].read())
        except:
            return []
    
    def save_match_data(self, puuid, match_data):
        existing_matches = self.load_match_data(puuid)
        existing_match_ids = {match.get('metadata', {}).get('matchId') for match in existing_matches}
        new_matches = [match for match in match_data if match.get('metadata', {}).get('matchId') not in existing_match_ids]
        existing_matches.extend(new_matches)
        
        s3_client.put_object(
            Bucket=self.bucket_name,
            Key=f"matches_{puuid}.json",
            Body=json.dumps(existing_matches, indent=2)
        )

def get_champion_recommendations(puuid, role="ALL"):
    """Sugere campeões baseado no histórico do jogador"""
    data_manager = S3DataManager(S3_BUCKET)
    matches = data_manager.load_match_data(puuid)
    
    if not matches:
        return "Nenhum dado encontrado para este jogador"
    
    analyzer = MatchAnalyzer(puuid)
    player_matches = analyzer.extract_player_data(matches)
    
    top_champions = analyzer.get_top_champions_played(player_matches, 10)
    top_winrates = analyzer.get_top_champions_winrate(player_matches, 10)
    
    recommendations = []
    played_champions = {champ for champ, _ in top_champions[:5]}
    
    for champion, winrate in top_winrates:
        if champion not in played_champions and winrate > 0.6:
            recommendations.append(f"{champion} (WR: {winrate:.1%})")
            if len(recommendations) >= 3:
                break
    
    if not recommendations:
        recommendations = ["Continue praticando seus campeões principais"]
    
    result = f"🎯 Recomendações para {role}:\n" + "\n".join(f"• {rec}" for rec in recommendations)
    return result

def lambda_handler(event, context):
    """Handler principal do Lambda"""
    try:
        body = json.loads(event.get('body', '{}'))
        action = body.get('action')
        puuid = body.get('puuid')
        role = body.get('role', 'ALL')
        
        if action == 'get_champion_recommendations':
            result = get_champion_recommendations(puuid, role)
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'result': result})
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Ação não suportada'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }