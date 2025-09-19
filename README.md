# league_of_legends_insights by PedroSillos
Data analytics free solution that aims to give League of Legends players valuable insights.

## Qual problema inspirou a ideia do projeto?
Sou um jogador de League of Legends e gostaria de uma ferramenta que retorna análises de como estou jogando competitivamente.

## Como a solução foi construída
Essa solução foi construída usando a extensão Amazon Q para VS Code. O Amazon Q Developer é um assistente de IA generativa da AWS que ajuda desenvolvedores a escrever, depurar e otimizar código de forma mais eficiente, oferecendo sugestões inteligentes e automação de tarefas de desenvolvimento.

## Instruções para rodar
1. Instale as dependências:
```bash
pip install requests
```

2. Execute a aplicação:
```bash
python main.py
```

3. Forneça os dados solicitados:
   - gameName (seu nome no jogo)
   - tagLine (sua tag, ex: BR1)
   - API Key (obtida em https://developer.riotgames.com/)

4. A aplicação irá:
   - Buscar seus dados na API da Riot
   - Salvar localmente para futuras execuções
   - Analisar suas últimas 100 partidas ranqueadas
   - Gerar visualizações dos seus campeões mais jogados, com mais vitórias e maior win rate

## Próximos passos
<Adicionarei depois>

## Prompts utilizados
### Prompt 1
Sou um jogador de League of Legends e gostaria de uma ferramenta que retorna análises de como estou jogando competitivamente.

Para isso, quero construir uma aplicação que extraia dados de algumas APIs da riot games e que crie dashboards e visualizações para tomadas de decisões.

O usuário deve passar apenas gameName, tagLine e apiKey.

Esses dados serão usados para consultar a API "https://developer.riotgames.com/apis#account-v1/GET_getByRiotId".

A aplicação deve armazenar esses dados em um arquivo local. Para cada nova execução, os dados devem ser adicionados aos invés de sobrescritos.

Então, para cada "puuid" nesse arquivo local, faça uma requisição para a API "https://developer.riotgames.com/apis#match-v5/GET_getMatchIdsByPUUID" e para, para cada matchId retornado, faça uma requisição para "https://developer.riotgames.com/apis#match-v5/GET_getMatch". Traga apenas os dados de match referentes ao "puuid" em questão.

Depois disso, transforme esses dados e calcule:

1) Quais são os 5 campeões mais jogados
2) Quais são os 5 campeões com mais vitórias
3) Quais são os 5 campeões com maior win rate (número de vitórias com aquele campeão dividido pelo total de jogos com aquele campeão).

Traga essas informações em forma de visualizações.

Como eu poderia construir essa aplicação?

### Prompt 2
Faça as seguintes melhorias:
1) Retorne os top 5 win rates, mesmo que alguns dos valores sejam iguais a 0%
2) Ao trazer os matchIds, passe o valor de queue = 420, o de type = "ranked" e o de count = 100

### Prompt 3
Altere para que, caso uma partida já esteja armazenada, não seja feita uma nova requisição pelos dados da partida

### Prompt 4
Atualmente todos os maiores win rates são todos 100% pois os são win rates de campeões pouco jogados.
Altere para que só venham win rates de campeões com pelo menos 3% do número total de partidas