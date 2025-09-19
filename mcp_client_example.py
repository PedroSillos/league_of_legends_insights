#!/usr/bin/env python3
"""
Exemplo de como usar o servidor MCP para obter recomendações
"""
import asyncio
import json
import subprocess
import sys

async def test_mcp_server():
    """Testa o servidor MCP localmente"""
    
    # Exemplo de requisição para recomendações
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "get_champion_recommendations",
            "arguments": {
                "puuid": "test_puuid",
                "role": "ADC"
            }
        }
    }
    
    print("🔧 Exemplo de uso do servidor MCP:")
    print("1. Execute o servidor: python mcp_server.py")
    print("2. Envie requisições JSON-RPC via stdin")
    print(f"3. Exemplo de requisição:\n{json.dumps(request, indent=2)}")
    
    # Exemplo de análise de tendências
    trend_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "analyze_performance_trends",
            "arguments": {
                "puuid": "test_puuid",
                "days": 30
            }
        }
    }
    
    print(f"\n📊 Exemplo de análise de tendências:\n{json.dumps(trend_request, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())