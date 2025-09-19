#!/usr/bin/env python3
from analyzer import MatchAnalyzer
from data_manager import DataManager
from riot_api import RiotAPI
import os
import getpass

def get_puuid_from_name(game_name, tag_line):
    """Busca PUUID pelos dados locais ou API da Riot"""
    data_manager = DataManager()
    players = data_manager.load_data()
    
    # Primeiro tenta encontrar nos dados locais
    for player in players:
        if (player.get('gameName', '').lower() == game_name.lower() and 
            player.get('tagLine', '').lower() == tag_line.lower()):
            return player.get('puuid')
    
    # Se não encontrou, busca na API
    print(f"\n🔍 Jogador não encontrado localmente. Buscando {game_name}#{tag_line} na API...")
    api_key = getpass.getpass("Digite sua API Key da Riot: ").strip()
    
    if not api_key:
        print("❌ API Key é obrigatória")
        return None
        
    riot_api = RiotAPI(api_key)
    account_data = riot_api.get_account_by_riot_id(game_name, tag_line)
    
    if not account_data:
        print("❌ Jogador não encontrado na API")
        return None
    
    # Salva dados da conta
    data_manager.save_account_data(account_data)
    puuid = account_data['puuid']
    
    # Busca partidas
    print("📥 Buscando partidas...")
    match_ids = riot_api.get_match_ids_by_puuid(puuid, count=100)
    
    if match_ids:
        existing_matches = data_manager.load_match_data(puuid)
        existing_match_ids = {match.get('metadata', {}).get('matchId') for match in existing_matches}
        new_match_ids = [mid for mid in match_ids if mid not in existing_match_ids]
        
        new_matches = []
        for i, match_id in enumerate(new_match_ids, 1):
            print(f"⏳ Buscando partida {i}/{len(new_match_ids)}: {match_id}")
            match_data = riot_api.get_match_data(match_id)
            if match_data:
                new_matches.append(match_data)
        
        if new_matches:
            data_manager.save_match_data(puuid, new_matches)
            print(f"✅ {len(new_matches)} partidas salvas")
    
    return puuid

def get_champion_recommendations(puuid, role="ALL"):
    """Sugere campeões baseado no histórico do jogador"""
    data_manager = DataManager()
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

def analyze_performance_trends(puuid, days=30):
    """Analisa tendências de performance do jogador"""
    data_manager = DataManager()
    matches = data_manager.load_match_data(puuid)
    
    if not matches:
        return "Nenhum dado encontrado"
    
    analyzer = MatchAnalyzer(puuid)
    player_matches = analyzer.extract_player_data(matches)
    
    recent_matches = player_matches[-10:] if len(player_matches) >= 10 else player_matches
    older_matches = player_matches[:-10] if len(player_matches) >= 20 else []
    
    recent_wr = sum(1 for m in recent_matches if m['win']) / len(recent_matches) if recent_matches else 0
    older_wr = sum(1 for m in older_matches if m['win']) / len(older_matches) if older_matches else recent_wr
    
    trend = "📈 Melhorando" if recent_wr > older_wr else "📉 Piorando" if recent_wr < older_wr else "➡️ Estável"
    
    result = f"📊 Análise de Tendência ({days} dias):\n"
    result += f"• Win Rate recente: {recent_wr:.1%}\n"
    result += f"• Tendência: {trend}\n"
    result += f"• Total de partidas: {len(player_matches)}"
    
    return result

def main():
    """Interface interativa do servidor MCP"""
    print("🎮 League of Legends Insights - Servidor MCP")
    print("=" * 50)
    
    while True:
        print("\nFerramentas disponíveis:")
        print("1. Recomendações de Campeões")
        print("2. Análise de Tendências")
        print("3. Sair")
        
        choice = input("\nEscolha uma opção (1-3): ").strip()
        
        if choice == "1":
            game_name = input("Digite o gameName: ").strip()
            tag_line = input("Digite a tagLine: ").strip()
            role = input("Digite a role (ou Enter para ALL): ").strip() or "ALL"
            
            puuid = get_puuid_from_name(game_name, tag_line)
            if not puuid:
                print("\n❌ Não foi possível obter dados do jogador")
                continue
                
            print("\n" + "="*50)
            result = get_champion_recommendations(puuid, role)
            print(result)
            print("="*50)
            
        elif choice == "2":
            game_name = input("Digite o gameName: ").strip()
            tag_line = input("Digite a tagLine: ").strip()
            days_input = input("Número de dias (ou Enter para 30): ").strip()
            days = int(days_input) if days_input.isdigit() else 30
            
            puuid = get_puuid_from_name(game_name, tag_line)
            if not puuid:
                print("\n❌ Não foi possível obter dados do jogador")
                continue
            
            print("\n" + "="*50)
            result = analyze_performance_trends(puuid, days)
            print(result)
            print("="*50)
            
        elif choice == "3":
            print("\n👋 Até logo!")
            break
            
        else:
            print("\n❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()