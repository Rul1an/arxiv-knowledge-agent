# Arxiv Knowledge Agent

Dit project implementeert een kennis-agent die wetenschappelijke artikelen kan zoeken en samenvatten vanuit Arxiv.

## ✨ Features

- **Arxiv Zoeken**: Doorzoek de Arxiv database naar wetenschappelijke papers
- **MCP Integratie**: Implementeert het Model Context Protocol (MCP) voor modulaire tool-integratie
- **Webinterface**: Handige UI om met de agent te interacteren
- **CLI Interface**: Command-line interface voor snelle zoekopdrachten

## 🚀 Setup

1. **Clone de repository**:
   ```bash
   git clone https://github.com/Rul1an/arxiv-knowledge-agent.git
   cd arxiv-knowledge-agent
   ```

2. **Maak een virtual environment aan**:
   ```bash
   python -m venv env
   source env/bin/activate  # Op macOS/Linux
   ```

3. **Installeer dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Stel je API keys in**:
   Maak een `.env` bestand aan in de hoofddirectory en voeg je OpenAI API key toe:
   ```
   OPENAI_API_KEY=your-key-here
   ```

## 🔍 Gebruik

### Uitvoeren van scripts

> **Belangrijk**: Afhankelijk van je setup staan de bestanden ofwel in de hoofdmap ofwel in de `arxiv_agent_mvp/` submap.
>
> **GitHub Versie**: Als je de repository net hebt gecloned, staan de bestanden in de hoofdmap.
> 
> **Lokale Ontwikkelversie**: Als je werkt in de lokale kopie op je eigen machine, staan de bestanden mogelijk in de `arxiv_agent_mvp/` submap.

Pas de onderstaande commando's aan op basis van je bestandslocaties:

### Web Interface

Start de webserver:

```bash
# Voor GitHub versie (bestanden in root):
python mcp_web_app_simple.py

# Voor lokale ontwikkelversie (bestanden in submap):
python arxiv_agent_mvp/mcp_web_app_simple.py
```

Navigeer naar `http://127.0.0.1:5000` in je browser.

### Command Line

Run de agent direct vanaf de command line:

```bash
# Voor GitHub versie (bestanden in root):
python agent_with_mcp_simple.py

# Voor lokale ontwikkelversie (bestanden in submap):
python arxiv_agent_mvp/agent_with_mcp_simple.py
```

### Testen

Voor een snelle test van de agent:

```bash
# Voor GitHub versie (bestanden in root):
python test_agent.py

# Voor lokale ontwikkelversie (bestanden in submap):
python arxiv_agent_mvp/test_agent.py
```

## 📁 Projectstructuur

- `arxiv_client.py` - Client voor de Arxiv API
- `agent_with_mcp_simple.py` - Vereenvoudigde agent met MCP integratie
- `arxiv_mcp_server_simple.py` - Vereenvoudigde MCP server implementatie
- `mcp_web_app_simple.py` - Web interface voor de vereenvoudigde MCP agent
- `test_agent.py` - Test script voor de agent
- `templates/` - HTML templates voor de webinterface
- `README.md` - Deze documentatie
- `README_MCP.md` - Gedetailleerde documentatie over de MCP implementatie
- `FIXES.md` - Logboek van opgeloste technische uitdagingen
- `SUMMARY.md` - Overzicht van het project en toekomstplannen

## 🛠️ MCP Implementatie

Dit project bevat een vereenvoudigde implementatie van het Model Context Protocol:

- **Vereenvoudigde MCP** (arxiv_mcp_server_simple.py): Directe JSON-gebaseerde implementatie van het MCP protocol via stdin/stdout

De eenvoudige implementatie heeft de volgende voordelen:
1. **Geen externe dependencies**: Implementeert MCP direct zonder afhankelijkheid van externe libraries
2. **Betere stabiliteit**: Omzeilt compatibiliteitsproblemen met de officiële MCP libraries
3. **Expliciete foutafhandeling**: Bevat uitgebreide error handling specifiek voor onze use case
4. **Directe JSON-communicatie**: Gebruikt eenvoudige JSON-berichten over stdin/stdout

## 📚 Technische Details

Zie `README_MCP.md` voor gedetailleerde informatie over de MCP-integratie en architectuur.
Zie `FIXES.md` voor een overzicht van opgeloste technische uitdagingen.

## 🧩 Uitbreiden

Om een nieuwe kennisbron toe te voegen:

1. Maak een nieuwe client voor de kennisbron (zoals `pubmed_client.py`)
2. Implementeer een MCP server voor deze bron (zoals `pubmed_mcp_server.py`)
3. Voeg de nieuwe MCP server toe aan de agent of webinterface