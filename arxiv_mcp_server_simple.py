#!/usr/bin/env python3
import asyncio
import json
import sys
import traceback
from typing import Dict, List, Any, Optional

from arxiv_client import fetch_arxiv_papers

class ArxivMCPServerStdio:
    """
    Een vereenvoudigde MCP server die communiceert via stdin/stdout.
    Implementeert het MCP protocol zonder afhankelijkheid van de mcp module.
    """
    
    def __init__(self):
        self.tools = {
            "search_arxiv_papers": {
                "type": "function",
                "function": {
                    "name": "search_arxiv_papers",
                    "description": "Search for papers on Arxiv",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query"
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of results to return",
                                "default": 3
                            }
                        },
                        "required": ["query"]
                    }
                }
            }
        }
    
    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verwerkt een binnenkomend MCP bericht en retourneert een antwoord.
        """
        try:
            if message.get("type") == "capabilities":
                return self.handle_capabilities()
            elif message.get("type") == "tool_call":
                return await self.handle_tool_call(message)
            else:
                return {
                    "type": "error",
                    "error": {
                        "message": f"Unsupported message type: {message.get('type')}"
                    }
                }
        except Exception as e:
            traceback.print_exc()
            return {
                "type": "error",
                "error": {
                    "message": f"Error handling message: {str(e)}"
                }
            }
    
    def handle_capabilities(self) -> Dict[str, Any]:
        """
        Retourneert de capabilities van deze MCP server.
        """
        return {
            "type": "capabilities",
            "capabilities": {
                "tools": list(self.tools.values())
            }
        }
    
    async def handle_tool_call(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verwerkt een tool_call bericht en voert de gevraagde functie uit.
        """
        tool_call = message.get("tool_call", {})
        tool_name = tool_call.get("name")
        
        if tool_name != "search_arxiv_papers":
            return {
                "type": "error",
                "error": {
                    "message": f"Unknown tool: {tool_name}"
                }
            }
        
        # Haal parameters op
        params = tool_call.get("parameters", {})
        query = params.get("query")
        max_results = params.get("max_results", 3)
        
        if not query:
            return {
                "type": "error",
                "error": {
                    "message": "Missing required parameter: query"
                }
            }
        
        # Voer de zoekopdracht uit
        try:
            papers = fetch_arxiv_papers(query, max_results)
            return {
                "type": "tool_result",
                "tool_result": {
                    "content": papers
                }
            }
        except Exception as e:
            traceback.print_exc()
            return {
                "type": "error",
                "error": {
                    "message": f"Error searching Arxiv: {str(e)}"
                }
            }
    
    async def read_message(self) -> Optional[Dict[str, Any]]:
        """
        Leest een JSON bericht van stdin.
        """
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                return None
            return json.loads(line)
        except json.JSONDecodeError:
            print("Error: Invalid JSON received", file=sys.stderr)
            return None
    
    def write_message(self, message: Dict[str, Any]) -> None:
        """
        Schrijft een JSON bericht naar stdout.
        """
        json_str = json.dumps(message)
        print(json_str, flush=True)
    
    async def run(self) -> None:
        """
        Start de MCP server en verwerkt berichten totdat een afsluitsignaal wordt ontvangen.
        """
        print("Arxiv MCP server starting...", file=sys.stderr)
        try:
            while True:
                message = await self.read_message()
                if message is None:
                    break
                
                response = await self.handle_message(message)
                self.write_message(response)
        except Exception as e:
            print(f"Error in MCP server: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

async def main():
    server = ArxivMCPServerStdio()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())