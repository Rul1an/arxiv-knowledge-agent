# Arxiv Knowledge Agent

Dit project implementeert een kennis-agent die wetenschappelijke artikelen kan zoeken en samenvatten vanuit Arxiv.

## ✨ Features

- **Arxiv Zoeken**: Doorzoek de Arxiv database naar wetenschappelijke papers
- **MCP Integratie**: Implementeert het Model Context Protocol (MCP) voor modulaire tool-integratie
- **Webinterface**: Handige UI om met de agent te interacteren
- **CLI Interface**: Command-line interface voor snelle zoekopdrachten

## 🚀 Setup

1. **Maak een virtual environment aan**:
   ```bash
   python -m venv env
   source env/bin/activate  # Op macOS/Linux
   ```

2. **Installeer dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Stel je API keys in**:
   Maak een `.env` bestand aan in de hoofddirectory en voeg je OpenAI API key toe:
   ```
   OPENAI_API_KEY=your-key-here
   ```

## 🔍 Gebruik

### Web Interface

Start de webserver:

```bash
python mcp_web_app.py  # Voor de originele MCP implementatie
# of
python mcp_web_app_simple.py  # Voor de vereenvoudigde MCP implementatie
```

Navigeer naar `http://127.0.0.1:5000` in je browser.

### Command Line

Run de agent direct vanaf de command line:

```bash
python main_agent.py  # Voor de originele agent zonder MCP
# of
python agent_with_mcp.py  # Voor de agent met MCP integratie
# of 
python agent_with_mcp_simple.py  # Voor de vereenvoudigde MCP implementatie
```

## 📁 Projectstructuur

- `arxiv_client.py` - Client voor de Arxiv API
- `main_agent.py` - De oorspronkelijke agent implementatie zonder MCP
- `agent_with_mcp.py` - Agent implementatie met MCP integratie
- `agent_with_mcp_simple.py` - Vereenvoudigde agent met MCP integratie
- `arxiv_mcp_server.py` - MCP server die de Arxiv functionaliteit beschikbaar stelt
- `arxiv_mcp_server_simple.py` - Vereenvoudigde MCP server implementatie
- `mcp_web_app.py` - Web interface voor de agent met MCP
- `mcp_web_app_simple.py` - Web interface voor de vereenvoudigde MCP agent
- `templates/` - HTML templates voor de webinterface
- `README.md` - Deze documentatie
- `README_MCP.md` - Gedetailleerde documentatie over de MCP implementatie

## 🛠️ MCP Implementaties

Het project bevat twee MCP implementaties:

1. **Originele MCP** (arxiv_mcp_server.py): Gebruikt de volledige MCP library
2. **Vereenvoudigde MCP** (arxiv_mcp_server_simple.py): Directe JSON-gebaseerde implementatie van het MCP protocol via stdin/stdout

## 📚 Technische Details

Zie `README_MCP.md` voor gedetailleerde informatie over de MCP-integratie en architectuur.

## 🧩 Uitbreiden

Om een nieuwe kennisbron toe te voegen:

1. Maak een nieuwe client voor de kennisbron (zoals `pubmed_client.py`)
2. Implementeer een MCP server voor deze bron (zoals `pubmed_mcp_server.py`)
3. Voeg de nieuwe MCP server toe aan de agent of webinterface