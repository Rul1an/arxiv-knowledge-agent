#!/usr/bin/env python3
"""
Arxiv MCP server implementatie met de officiële MCP Python SDK.
"""

import asyncio
import os
from typing import Dict, Any, List

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import Context

from arxiv_client import ArxivClient

# Maak een MCP server instance
mcp = FastMCP("Arxiv Knowledge")


@mcp.tool()
async def search_arxiv_papers(query: str, max_results: int = 10) -> str:
    """
    Zoek naar wetenschappelijke papers op Arxiv.
    
    Args:
        query: De zoekopdracht (keywords, auteurs, categorie, etc.)
        max_results: Maximum aantal resultaten om terug te geven
    
    Returns:
        Een geformatteerde lijst van relevante papers
    """
    try:
        # Maak een Arxiv client
        client = ArxivClient()
        
        # Zoek papers
        papers = await client.search_papers(query, max_results=max_results)
        
        # Geen resultaten?
        if not papers:
            return f"Geen papers gevonden voor de zoekopdracht: '{query}'"
        
        # Formatteer de resultaten
        results = []
        for i, paper in enumerate(papers, 1):
            paper_info = f"### {i}. {paper['title']}\n"
            paper_info += f"**Auteurs:** {paper['authors']}\n"
            paper_info += f"**Publicatiedatum:** {paper['published']}\n"
            paper_info += f"**Link:** {paper['pdf_url']}\n"
            paper_info += f"**Abstract:** {paper['summary']}\n"
            results.append(paper_info)
        
        header = f"# Zoekresultaten voor: '{query}'\n\n"
        return header + "\n\n".join(results)
    
    except Exception as e:
        return f"Error bij het zoeken naar papers: {str(e)}"


@mcp.resource("arxiv://help")
def arxiv_help() -> str:
    """
    Resource met help informatie over het gebruik van de Arxiv MCP server.
    """
    help_text = """
    # Arxiv Knowledge Server Help
    
    Dit is een MCP server die je toegang geeft tot wetenschappelijke papers op Arxiv.
    
    ## Beschikbare tools
    
    ### search_arxiv_papers
    
    Zoekt naar papers op Arxiv en geeft de meest relevante resultaten terug.
    
    Parameters:
    - query: Zoekopdracht (keywords, auteurs, categorieën, etc.)
    - max_results: Maximum aantal resultaten (standaard 10)
    
    Voorbeeld gebruik:
    ```
    Kun je papers over quantum computing vinden die zijn gepubliceerd in 2023?
    ```
    
    ## Tips voor effectief zoeken
    
    - Gebruik specifieke keywords voor nauwkeurigere resultaten
    - Combineer auteursnamen met onderwerpen
    - Specificeer categorieën voor gerichte zoekopdrachten
    """
    return help_text


if __name__ == "__main__":
    mcp.run()