# MCP SDK Implementatie

Dit document beschrijft de implementatie van de Knowledge Agent met de officiële Model Context Protocol (MCP) Python SDK.

## Wat is de MCP Python SDK?

De Model Context Protocol (MCP) Python SDK is een officiële implementatie van het MCP protocol in Python. Het biedt eenvoudige en goed gestructureerde interfaces voor het bouwen van MCP servers en clients.

De SDK biedt ondersteuning voor:
- FastMCP API voor eenvoudige server definities met decorators
- Volledig getypeerde client/server communicatie
- Ondersteuning voor verschillende transportprotocollen zoals stdio en SSE
- Uitgebreide functionaliteit voor resources, tools en prompts

## Implementatie in dit project

We hebben drie componenten gebouwd die de MCP Python SDK gebruiken:

1. **Arxiv MCP Server (arxiv_mcp_server_sdk.py)**: Een MCP server die tools en resources biedt voor het zoeken naar wetenschappelijke papers op Arxiv.
2. **Arxiv Agent (agent_with_mcp_sdk.py)**: Een client die verbinding maakt met de MCP server, tools ophaalt en deze doorgeeft aan het OpenAI model.
3. **Web Interface (mcp_web_app_sdk.py)**: Een Flask-gebaseerde webinterface die de agent gebruikt om zoekresultaten te tonen.

### Arxiv MCP Server

De server is gebouwd met de `FastMCP` API, die een eenvoudige interface biedt voor het definiëren van tools en resources met decorators:

```python
mcp = FastMCP("Arxiv Knowledge")

@mcp.tool()
async def search_arxiv_papers(query: str, max_results: int = 10) -> str:
    # Implementatie van de zoekfunctie
```

Deze aanpak heeft verschillende voordelen:
- Automatische argumentvalidatie
- Gegenereerde schema's voor tools en resources
- Type-veilige communicatie
- Eenvoudige toevoeging van nieuwe functionaliteit

### Arxiv Agent

De agent gebruikt de MCP client API om verbinding te maken met de server:

```python
async with stdio_client(server_params) as (read_stream, write_stream):
    async with ClientSession(read_stream, write_stream) as session:
        # Vraag tools op, converteer ze naar OpenAI formaat, etc.
```

De client sessie zorgt voor proper resource management en biedt methoden voor alle MCP protocol operaties.

### Verschillen met custom implementatie

Vergeleken met de eerdere handgemaakte implementatie biedt de SDK-gebaseerde aanpak:

1. **Verbeterde stabiliteit**: De SDK implementeert het volledige protocol correct en is goed getest.
2. **Minder code**: We hebben minder custom code nodig om het protocol te implementeren.
3. **Toekomstbestendigheid**: De SDK zal worden bijgewerkt met nieuwe MCP protocol features.
4. **Type safety**: Volledige type annotaties en validatie van protocol berichten.
5. **Betere foutmeldingen**: Gedetailleerde error reporting en diagnostiek.

## Gebruik

Om de SDK-gebaseerde implementatie te gebruiken:

```bash
# Voor de command-line agent
python agent_with_mcp_sdk.py

# Voor de web interface
python mcp_web_app_sdk.py
```

## Configuratie

De MCP Python SDK kan worden geconfigureerd met verschillende opties voor de server en client. Zie de [officiële documentatie](https://github.com/modelcontextprotocol/python-sdk) voor meer informatie.

## Codestructuur

- **arxiv_mcp_server_sdk.py**: De MCP server implementatie met de SDK
- **agent_with_mcp_sdk.py**: De agent die de SDK client gebruikt
- **mcp_web_app_sdk.py**: De web interface die de agent integreert

## Toekomstige verbeteringen

Met de SDK kunnen we eenvoudig nieuwe functionaliteit toevoegen:

1. **Meer resources**: Dynamische resources voor specifieke papers, categorieën, auteurs
2. **Geavanceerde tools**: Tools voor het analyseren van papers, vergelijken van onderzoek, etc.
3. **Prompts**: Gedefinieerde prompt templates voor verschillende use cases
4. **SSE transport**: Server-sent events voor real-time communicatie
5. **WebSocket transport**: Bidirectionele communicatie voor complexere toepassingen