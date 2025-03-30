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
python mcp_web_app_simple.py  # Vereenvoudigde implementatie
python mcp_web_app_sdk.py     # SDK implementatie (aanbevolen)

# Voor lokale ontwikkelversie (bestanden in submap):
python arxiv_agent_mvp/mcp_web_app_simple.py
python arxiv_agent_mvp/mcp_web_app_sdk.py
```

Navigeer naar `http://127.0.0.1:5000` in je browser.

### Command Line

Run de agent direct vanaf de command line:

```bash
# Voor GitHub versie (bestanden in root):
python agent_with_mcp_simple.py  # Vereenvoudigde implementatie
python agent_with_mcp_sdk.py     # SDK implementatie (aanbevolen)

# Voor lokale ontwikkelversie (bestanden in submap):
python arxiv_agent_mvp/agent_with_mcp_simple.py
python arxiv_agent_mvp/agent_with_mcp_sdk.py
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

### Core Bestanden
- `arxiv_client.py` - Client voor de Arxiv API
- `test_agent.py` - Test script voor de agent
- `templates/` - HTML templates voor de webinterface

### MCP Implementaties
- **Vereenvoudigde Implementatie**:
  - `agent_with_mcp_simple.py` - Vereenvoudigde agent met MCP integratie
  - `arxiv_mcp_server_simple.py` - Vereenvoudigde MCP server implementatie
  - `mcp_web_app_simple.py` - Web interface voor de vereenvoudigde MCP agent

- **SDK-gebaseerde Implementatie**:
  - `agent_with_mcp_sdk.py` - Agent met Python MCP SDK
  - `arxiv_mcp_server_sdk.py` - MCP server met de officiële Python SDK
  - `mcp_web_app_sdk.py` - Web interface voor de SDK-gebaseerde agent

### Documentatie
- `README.md` - Deze documentatie
- `README_MCP.md` - Documentatie over de vereenvoudigde MCP implementatie
- `README_MCP_SDK.md` - Documentatie over de SDK-gebaseerde MCP implementatie
- `FIXES.md` - Logboek van opgeloste technische uitdagingen
- `SUMMARY.md` - Overzicht van het project en toekomstplannen

## 🛠️ MCP Implementaties

Dit project bevat twee implementaties van het Model Context Protocol:

### 1. Vereenvoudigde MCP Implementatie

Een directe JSON-gebaseerde implementatie van het MCP protocol via stdin/stdout met de volgende voordelen:
- **Geen externe dependencies**: Implementeert MCP direct zonder afhankelijkheid van externe libraries
- **Betere stabiliteit**: Omzeilt compatibiliteitsproblemen met de officiële MCP libraries
- **Expliciete foutafhandeling**: Bevat uitgebreide error handling specifiek voor onze use case
- **Directe JSON-communicatie**: Gebruikt eenvoudige JSON-berichten over stdin/stdout

### 2. SDK-gebaseerde MCP Implementatie (Aanbevolen)

Een implementatie die de officiële MCP Python SDK gebruikt:
- **Volledige protocal compliance**: Implementeert het gehele MCP protocol correct
- **Type safety**: Sterke type-checking en validatie
- **Minder code**: Minder boilerplate code door decorators en helpers
- **Toekomstbestendig**: Zal worden bijgewerkt met nieuwe MCP protocol features
- **Betere foutmeldingen**: Uitgebreide error reporting en diagnostiek

## 📚 Technische Details

- Zie `README_MCP.md` voor gedetailleerde informatie over de vereenvoudigde MCP-integratie.
- Zie `README_MCP_SDK.md` voor gedetailleerde informatie over de SDK-gebaseerde MCP-integratie.
- Zie `FIXES.md` voor een overzicht van opgeloste technische uitdagingen.

## 🧩 Uitbreiden

Om een nieuwe kennisbron toe te voegen:

1. Maak een nieuwe client voor de kennisbron (zoals `pubmed_client.py`)
2. Implementeer een MCP server voor deze bron (zoals `pubmed_mcp_server.py`)
3. Voeg de nieuwe MCP server toe aan de agent of webinterface