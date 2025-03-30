#!/usr/bin/env python3
"""
Agent die de MCP server gebruikt met de officiële MCP Python SDK.
"""

import asyncio
import os
import sys
import traceback
from typing import Dict, Any, List, Optional

from dotenv import load_dotenv
from openai import OpenAI

# Import MCP client functionaliteit
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# Load environment variables
load_dotenv()

# Pad naar de MCP server script
MCP_SERVER_PATH = os.path.join(os.path.dirname(__file__), "arxiv_mcp_server_sdk.py")


class ArxivAgent:
    """Een agent die de Arxiv MCP server gebruikt om papers te vinden."""

    def __init__(self, openai_api_key: str):
        """Initialiseer de agent met OpenAI client."""
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.server_params = StdioServerParameters(
            command=sys.executable,  # Python executable
            args=[MCP_SERVER_PATH],  # MCP server script
            env=os.environ.copy(),  # Geef huidige environment door
        )

    async def run_conversation(self, user_question: str) -> str:
        """
        Voer een gesprek met de gebruiker, gebruik makend van de MCP server voor tools.
        """
        try:
            # Start de MCP client
            async with stdio_client(self.server_params) as (read_stream, write_stream):
                # Maak een client sessie
                async with ClientSession(read_stream, write_stream) as session:
                    # Initialiseer de verbinding
                    await session.initialize()

                    # Haal beschikbare tools op
                    tools = await session.list_tools()

                    # Converteer MCP tools naar OpenAI tool format
                    openai_tools = [
                        {
                            "type": "function",
                            "function": {
                                "name": tool.name,
                                "description": tool.description or "",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        param.name: {
                                            "type": param.type,
                                            "description": param.description or "",
                                        }
                                        for param in tool.parameters
                                    },
                                    "required": [
                                        param.name
                                        for param in tool.parameters
                                        if param.required
                                    ],
                                },
                            },
                        }
                        for tool in tools
                    ]

                    # Creëer de berichten voor de OpenAI API
                    messages = [
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that can search for scientific papers on Arxiv. Use the search_arxiv_papers tool to find papers related to the user's query.",
                        },
                        {"role": "user", "content": user_question},
                    ]

                    # Maak de API call naar OpenAI
                    response = self.openai_client.chat.completions.create(
                        model="gpt-4-turbo",
                        messages=messages,
                        tools=openai_tools,
                        tool_choice="auto",
                    )

                    # Verwerk het antwoord
                    assistant_message = response.choices[0].message

                    # Voeg het assistant bericht toe met tool_calls
                    messages.append(
                        {
                            "role": "assistant",
                            "content": assistant_message.content or "",
                            "tool_calls": [
                                {
                                    "id": tc.id,
                                    "type": "function",
                                    "function": {
                                        "name": tc.function.name,
                                        "arguments": tc.function.arguments,
                                    },
                                }
                                for tc in (assistant_message.tool_calls or [])
                            ]
                            if assistant_message.tool_calls
                            else None,
                        }
                    )

                    # Verwerk tool calls indien aanwezig
                    if assistant_message.tool_calls:
                        for tool_call in assistant_message.tool_calls:
                            # Haal de tool parameters op
                            function_name = tool_call.function.name
                            arguments = json.loads(tool_call.function.arguments)

                            # Roep de tool aan via de MCP client
                            tool_result = await session.call_tool(
                                function_name, arguments=arguments
                            )

                            # Voeg het resultaat toe aan de berichten
                            messages.append(
                                {
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "content": tool_result,
                                }
                            )

                        # Vraag OpenAI om een definitief antwoord
                        second_response = self.openai_client.chat.completions.create(
                            model="gpt-4-turbo", messages=messages
                        )

                        return second_response.choices[0].message.content

                    # Als er geen tool calls zijn, retourneer het originele antwoord
                    return assistant_message.content or "No response from assistant"

        except Exception as e:
            return f"Error running agent: {str(e)}"


async def main():
    """Hoofdfunctie die de agent start en een vraag verwerkt."""
    # Laad environment variables
    load_dotenv()

    # Controleer of de OpenAI API key is ingesteld
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: OPENAI_API_KEY is not set in the environment or .env file")
        sys.exit(1)

    # Maak en start de agent
    agent = ArxivAgent(openai_api_key)

    # Vraag om input van de gebruiker of gebruik een default vraag
    user_question = input(
        "Enter your scientific question (or press Enter for a default): "
    ).strip()
    if not user_question:
        user_question = "What are the latest developments in quantum computing?"

    try:
        # Voer het gesprek uit
        response = await agent.run_conversation(user_question)
        print("\nAgent Response:")
        print(response)
    except Exception as e:
        print(f"Error running agent: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    import json  # Voeg json import toe voor argumenten parsing
    
    # Start de main functie
    asyncio.run(main())