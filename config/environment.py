from os import environ
from typing import Optional

from dotenv import load_dotenv
from pydantic import MongoDsn

load_dotenv()

PROJECT_NAME = environ.get("PROJECT_NAME", "ResumidorLLM")
LANGUAGE = environ.get("LANGUAGE", "en") # language code
NATURAL_LANGUAGE = environ.get("NATURAL_LANGUAGE", "English") # natural language

OPENAI_API_KEY = environ.get("OPENAI_API_KEY", "default")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

LOCALLY_API_BASE = environ.get("LOCALLY_API_BASE", "http://localhost:8502")
LOCALLY_API_KEY = environ.get("LOCALLY_API_KEY", "default")

# Set the OpenAI API base URL
OPENAI_API_BASE = environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")

# Set the OpenAI model to be used
OPENAI_MODEL = environ.get("OPENAI_MODEL", "gpt-4o-mini")

# Set the OpenAI embedding model to be used
OPENAI_EMBEDDING_MODEL = environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# Set the OpenAI temperature for randomness in responses
OPENAI_TEMPERATURE = float(environ.get("OPENAI_TEMPERATURE", .0))

# Set the OpenAI max tokens for response length
OPENAI_MAX_TOKENS = int(environ.get("OPENAI_MAX_TOKENS", 1000))

# MongoDB configuration
MONGODB_URI: Optional[MongoDsn] = environ.get("MONGODB_URI")
MONGODB_DATABASE: Optional[str] = environ.get("MONGODB_DATABASE", "summarizer")
if MONGODB_URI is None:
    raise ValueError("MONGODB_URI not found in environment variables.")
#

# Qdrant configuration
QDRANT_DSN: Optional[str] = environ.get("QDRANT_DSN", "http://localhost:6333")
QDRANT_COLLECTION: Optional[str] = environ.get("QDRANT_COLLECTION", "summarizer")
if QDRANT_DSN is None:
    raise ValueError("QDRANT_DSN not found in environment variables.")
#
