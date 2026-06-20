# AutonDB

A self-hosted, AI-native credential store. Query your API keys in plain English.
No Oracle. No cloud. Runs on your machine.

## Stack
- FastAPI + Uvicorn
- Ollama (phi3 resolver + nomic-embed-text)
- ChromaDB (metadata vector store)
- SQLite + SQLCipher (encrypted secret vault)

## Setup

cp .env.example .env
# Edit .env with your secrets

pip install -r requirements.txt
uvicorn app.main:app --reload

## Usage

# Register
POST /auth/register  {"username": "you", "password": "pass"}

# Login
POST /auth/login  {"username": "you", "password": "pass"}

# Store a key
POST /keys/store  {"name": "Stripe production", "service": "stripe", "tags": ["payments", "prod"], "value": "sk_live_..."}

# Query in plain English
POST /query  {"query": "give me the stripe payments key"}
