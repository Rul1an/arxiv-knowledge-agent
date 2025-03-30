#!/usr/bin/env python3
"""
Test script voor de Arxiv Agent met MCP
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Zorg ervoor dat we de agent module kunnen vinden
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agent_with_mcp_simple import ArxivAgent
except ImportError as e:
    print(f"Error importeren van ArxivAgent: {e}")
    sys.exit(1)


async def test_agent():
    """Test de ArxivAgent met een eenvoudige vraag"""
    # Laad environment variables
    load_dotenv()

    # Controleer of de OpenAI API key is ingesteld
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: OPENAI_API_KEY is not set in the environment or .env file")
        sys.exit(1)

    print("Initialiseren van de agent...")
    agent = ArxivAgent(openai_api_key)

    # Test query
    test_query = "What are the latest developments in quantum computing?"
    print(f"Voer zoekopdracht uit: '{test_query}'")

    try:
        # Voer de gesprek uit
        response = await agent.run_conversation(test_query)
        print("\nAgent Antwoord:")
        print("-" * 40)
        print(response)
        print("-" * 40)
        return True
    except Exception as e:
        import traceback
        print(f"Error tijdens uitvoeren van agent: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== ArxivAgent MCP Test ===")
    success = asyncio.run(test_agent())

    if success:
        print("\n✅ Test geslaagd: De agent werkt correct!")
        sys.exit(0)
    else:
        print("\n❌ Test mislukt: Er zijn problemen met de agent.")
        sys.exit(1)