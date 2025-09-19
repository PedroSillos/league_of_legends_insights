# Project Context: League of Legends Insights

## Project Overview
This is a data analytics application that provides League of Legends players with competitive insights by analyzing their match history through Riot Games APIs.

## Core Components
- **riot_api.py**: Handles all Riot Games API interactions
- **data_manager.py**: Manages local data storage and caching
- **analyzer.py**: Processes match data and calculates statistics
- **visualizer.py**: Creates ASCII-based data visualizations
- **main.py**: Main application orchestrator
- **mcp_server.py**: MCP server for AI-powered recommendations

## Key Features
- Fetches player account data and match history
- Analyzes champion performance (most played, highest winrate)
- Provides champion recommendations via MCP
- Caches data locally to minimize API calls
- Filters for ranked Solo/Duo matches only

## Data Flow
1. User provides gameName and tagLine
2. System fetches PUUID from Riot Account API
3. Retrieves match IDs from Match API (queue=420, ranked)
4. Downloads match details and extracts player data
5. Analyzes performance and generates insights
6. Displays results via ASCII visualizations

## Important Constraints
- Only analyzes ranked Solo/Duo queue matches
- Requires minimum 3% of total matches for winrate calculations
- Respects Riot Games API rate limits
- Stores data locally in JSON format