#!/usr/bin/env python3
"""
Agent die de vereenvoudigde Arxiv MCP server gebruikt.
"""

import asyncio
import json
import os
import subprocess
import sys
import traceback
from typing import Dict, Any, List, Optional

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Pad naar de MCP server script
MCP_SERVER_PATH = os.path.join(os.path.dirname(
    __file__), "arxiv_mcp_server_simple.py")


class ArxivAgent:
    """Een agent die de Arxiv MCP server gebruikt om papers te vinden."""

    def __init__(self, openai_api_key: str):
        """Initialiseer de agent met OpenAI client."""
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.mcp_server_process = None

    async def start_mcp_server(self) -> subprocess.Popen:
        """Start de MCP server als een subprocess en retourneer het process handle."""
        # Zorg ervoor dat het script uitvoerbaar is
        if not os.access(MCP_SERVER_PATH, os.X_OK):
            os.chmod(MCP_SERVER_PATH, 0o755)

        # Start de server als een subprocess
        process = subprocess.Popen(
            [sys.executable, MCP_SERVER_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            text=True,
            bufsize=1  # Line buffered
        )
        self.mcp_server_process = process
        return process

    async def send_receive_message(self, process: subprocess.Popen, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Stuur een bericht naar de MCP server en wacht op een antwoord."""
        # Stuur het bericht
        json_message = json.dumps(message) + "\n"
        if process.stdin is None:
            print("Error: process stdin is None", file=sys.stderr)
            return None

        process.stdin.write(json_message)
        process.stdin.flush()

        # Lees het antwoord
        if process.stdout is None:
            print("Error: process stdout is None", file=sys.stderr)
            return None

        response_line = await asyncio.get_event_loop().run_in_executor(None, process.stdout.readline)
        if not response_line:
            return None

        try:
            return json.loads(response_line)
        except json.JSONDecodeError:
            print(
                f"Error: Invalid JSON response: {response_line}", file=sys.stderr)
            return None

    async def get_server_capabilities(self, process: subprocess.Popen) -> List[Dict[str, Any]]:
        """Vraag de capabilities van de MCP server."""
        message = {"type": "capabilities"}
        response = await self.send_receive_message(process, message)

        if response and response.get("type") == "capabilities":
            return response.get("capabilities", {}).get("tools", [])
        return []

    async def call_tool(self, process: subprocess.Popen, tool_name: str, parameters: Dict[str, Any]) -> str:
        """Roep een tool aan op de MCP server."""
        message = {
            "type": "tool_call",
            "tool_call": {
                "name": tool_name,
                "parameters": parameters
            }
        }

        response = await self.send_receive_message(process, message)

        if response and response.get("type") == "tool_result":
            return response.get("tool_result", {}).get("content", "No content returned")
        elif response and response.get("type") == "error":
            return f"Error: {response.get('error', {}).get('message', 'Unknown error')}"
        else:
            return "Unknown response from MCP server"

    async def run_conversation(self, user_question: str) -> str:
        """
        Voer een gesprek met de gebruiker, gebruik makend van de MCP server voor tools.
        """
        # Start de MCP server
        process = await self.start_mcp_server()

        try:
            # Haal server capabilities op
            tools = await self.get_server_capabilities(process)
            if not tools:
                return "Failed to get MCP server capabilities"

            # Creëer de berichten voor de OpenAI API
            messages = [
                {"role": "system", "content": "You are a helpful assistant that can search for scientific papers on Arxiv. Use the search_arxiv_papers tool to find papers related to the user's query."},
                {"role": "user", "content": user_question}
            ]

            # Maak de API call naar OpenAI
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )

            # Verwerk het antwoord
            assistant_message = response.choices[0].message

            # Voeg het assistant bericht toe met tool_calls
            assistant_msg = {"role": "assistant", "content": assistant_message.content or ""}
            if assistant_message.tool_calls:
                assistant_msg["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in assistant_message.tool_calls
                ]

            messages.append(assistant_msg)

            # Verwerk tool calls indien aanwezig
            if assistant_message.tool_calls:
                for tool_call in assistant_message.tool_calls:
                    # Haal de tool parameters op
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)

                    # Roep de tool aan
                    tool_result = await self.call_tool(process, function_name, arguments)

                    # Voeg het resultaat toe aan de berichten
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })

                # Vraag OpenAI om een definitief antwoord
                second_response = self.openai_client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=messages
                )

                return second_response.choices[0].message.content

            # Als er geen tool calls zijn, retourneer het originele antwoord
            return assistant_message.content or "No response from assistant"

        finally:
            # Sluit de MCP server af
            if process.poll() is None:  # Als het process nog draait
                try:
                    process.terminate()
                    process.wait(timeout=2)
                except:
                    process.kill()  # Forceer afsluiting als terminate niet werkt


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
        "Enter your scientific question (or press Enter for a default): ").strip()
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
    # Start de main functie
    asyncio.run(main())