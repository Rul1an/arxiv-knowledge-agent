#!/usr/bin/env python3
import asyncio
import os
import sys
import threading
import traceback
from typing import Dict, Any

# Voeg het pad naar de flask installatie toe indien nodig
# sys.path.append('/Users/roelschuurkes/miniconda3/lib/python3.12/site-packages')

# Importeer dependencies met foutafhandeling
try:
    from flask import Flask, render_template, request, jsonify
    from flask_cors import CORS
    import socketio
    from dotenv import load_dotenv
    from agent_with_mcp_simple import ArxivAgent
except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("\nZorg dat alle benodigde packages zijn geïnstalleerd met:")
    print("pip install flask flask-cors python-socketio python-dotenv")
    sys.exit(1)

# Laad environment variables
load_dotenv()

# Haal OpenAI API key op
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment or .env file")

# Initialiseer Flask app
app = Flask(__name__)
CORS(app)

# Initialiseer Socket.IO
sio = socketio.Server(cors_allowed_origins="*", async_mode='threading')
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# Maak een event loop voor asyncio in een aparte thread
async_loop = asyncio.new_event_loop()

def run_async(coroutine):
    """Functie om een coroutine uit te voeren in de event loop thread."""
    future = asyncio.run_coroutine_threadsafe(coroutine, async_loop)
    return future.result()

def start_background_loop():
    """Start de event loop in een background thread."""
    asyncio.set_event_loop(async_loop)
    async_loop.run_forever()

# Start de event loop thread
threading.Thread(target=start_background_loop, daemon=True).start()

# Agent instantie
try:
    arxiv_agent = ArxivAgent(openai_api_key)
except Exception as e:
    print(f"Error initializing ArxivAgent: {e}")
    traceback.print_exc()
    sys.exit(1)

@app.route('/')
def index():
    """Render de hoofdpagina."""
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    """
    API endpoint voor het zoeken naar papers op Arxiv.
    Verwacht een JSON body met een 'query' veld.
    """
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Missing query parameter'
        }), 400
    
    try:
        # Voer de agent uit met de query
        response = run_async(arxiv_agent.run_conversation(query))
        
        return jsonify({
            'success': True,
            'result': response
        })
    except Exception as e:
        print(f"Error processing query: {e}")
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Socket.IO events
@sio.event
def connect(sid, environ):
    """Handle client connection."""
    print(f"Client connected: {sid}")

@sio.event
def disconnect(sid):
    """Handle client disconnection."""
    print(f"Client disconnected: {sid}")

@sio.event
def search_query(sid, data):
    """
    Handle search query from client via Socket.IO.
    """
    query = data.get('query', '')
    if not query:
        sio.emit('error', {'message': 'Missing query parameter'}, room=sid)
        return
    
    def run_search():
        try:
            # Voer de agent uit met de query
            response = run_async(arxiv_agent.run_conversation(query))
            sio.emit('search_results', {'result': response}, room=sid)
        except Exception as e:
            print(f"Error processing query: {e}")
            traceback.print_exc()
            sio.emit('error', {'message': str(e)}, room=sid)
    
    # Start in een aparte thread om de Socket.IO event loop niet te blokkeren
    threading.Thread(target=run_search).start()

if __name__ == '__main__':
    # Start de Flask app
    print("Starting Arxiv Knowledge Agent Web App on http://127.0.0.1:5000")
    try:
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
    except Exception as e:
        print(f"Error starting Flask app: {e}")
        traceback.print_exc()