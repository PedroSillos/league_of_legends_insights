from riot_api import RiotAPI
from data_manager import DataManager
from analyzer import MatchAnalyzer
from visualizer import DataVisualizer

def main():
    # Entrada do usuário
    game_name = input("Digite seu gameName: ")
    tag_line = input("Digite sua tagLine: ")
    api_key = input("Digite sua API Key: ")
    
    # Inicializa classes
    riot_api = RiotAPI(api_key)
    data_manager = DataManager()
    visualizer = DataVisualizer()
    
    print(f"\nBuscando dados para {game_name}#{tag_line}...")
    
    # 1. Busca dados da conta
    account_data = riot_api.get_account_by_riot_id(game_name, tag_line)
    if not account_data:
        print("Erro ao buscar dados da conta!")
        return
    
    # 2. Salva dados da conta
    data_manager.save_account_data(account_data)
    puuid = account_data['puuid']
    print(f"PUUID encontrado: {puuid}")
    
    # 3. Busca IDs das partidas
    print("Buscando partidas...")
    match_ids = riot_api.get_match_ids_by_puuid(puuid, count=100)
    
    if not match_ids:
        print("Nenhuma partida encontrada!")
        return
    
    print(f"Encontradas {len(match_ids)} partidas")
    
    # 4. Carrega partidas já armazenadas
    existing_matches = data_manager.load_match_data(puuid)
    existing_match_ids = {match.get('metadata', {}).get('matchId') for match in existing_matches}
    
    # 5. Busca apenas partidas novas
    new_match_ids = [mid for mid in match_ids if mid not in existing_match_ids]
    
    new_matches = []
    if new_match_ids:
        print(f"Buscando {len(new_match_ids)} partidas novas...")
        for i, match_id in enumerate(new_match_ids, 1):
            print(f"Buscando partida {i}/{len(new_match_ids)}: {match_id}")
            match_data = riot_api.get_match_data(match_id)
            if match_data:
                new_matches.append(match_data)
    else:
        print("Todas as partidas já estão armazenadas")
    
    # 6. Salva apenas partidas novas
    if new_matches:
        data_manager.save_match_data(puuid, new_matches)
    
    # 7. Usa todas as partidas (existentes + novas)
    all_matches = existing_matches + new_matches
    
    # 8. Analisa os dados
    analyzer = MatchAnalyzer(puuid)
    player_matches = analyzer.extract_player_data(all_matches)
    
    if not player_matches:
        print("Nenhum dado de partida encontrado para análise!")
        return
    
    print(f"\nAnalisando {len(player_matches)} partidas...")
    
    # 9. Calcula estatísticas
    top_played = analyzer.get_top_champions_played(player_matches)
    top_wins = analyzer.get_top_champions_wins(player_matches)
    top_winrate = analyzer.get_top_champions_winrate(player_matches)
    
    # 10. Exibe resultados
    print("\n=== RESULTADOS ===")
    print("\nTop 5 Campeões Mais Jogados:")
    for i, (champion, count) in enumerate(top_played, 1):
        print(f"{i}. {champion}: {count} jogos")
    
    print("\nTop 5 Campeões com Mais Vitórias:")
    for i, (champion, wins) in enumerate(top_wins, 1):
        print(f"{i}. {champion}: {wins} vitórias")
    
    print("\nTop 5 Campeões com Maior Win Rate:")
    for i, (champion, winrate) in enumerate(top_winrate, 1):
        print(f"{i}. {champion}: {winrate:.1%}")
    
    # 11. Gera visualizações
    print("\nGerando visualizações...")
    visualizer.plot_top_champions_played(top_played)
    visualizer.plot_top_champions_wins(top_wins)
    visualizer.plot_top_champions_winrate(top_winrate)

if __name__ == "__main__":
    main()