"""
Central configuration file for the Multi-Document RAG System.

This file contains ONLY configuration values.
No business logic, no API calls, no processing code.

Changing values here should tune system behavior
without modifying core logic.
"""

from pathlib import Path

# =====================================================
# APPLICATION SETTINGS
# =====================================================

APP_NAME = "Multi-Document Conversational RAG"
ENVIRONMENT = "development"  # development | production


# =====================================================
# BASE PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
VECTOR_INDEX_DIR = DATA_DIR / "vector_index"

# Ensure these directories exist at runtime
# (creation logic will be handled elsewhere)
# No directory creation logic here


# =====================================================
# DOCUMENT PROCESSING SETTINGS
# =====================================================

# Text chunking parameters
CHUNK_SIZE = 1000          # characters or tokens (decide once and be consistent)
CHUNK_OVERLAP = 200        # overlap to preserve context across chunks
MIN_CHUNK_LENGTH = 100     # discard very small chunks


# =====================================================
# EMBEDDING MODEL SETTINGS
# =====================================================

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DEVICE = "cpu"   # cpu | cuda (if available)

# Used for validation / debugging (optional)
EMBEDDING_DIMENSION = 384


# =====================================================
# VECTOR RETRIEVAL SETTINGS
# =====================================================

TOP_K_RETRIEVAL = 5        # number of most relevant chunks to retrieve
SIMILARITY_METRIC = "cosine"  # conceptual (FAISS handles internally)


# =====================================================
# LLM GENERATION SETTINGS
# =====================================================
LLM_MODEL_NAME = "llama-3.1-8b-instant"
LLM_TEMPERATURE = 0.2      # low temperature to reduce hallucinations
MAX_RESPONSE_TOKENS = 512

SYSTEM_PROMPT = (
    "You are a helpful AI assistant. "
    "Answer ONLY using the provided document context. "
    "If the answer is not found in the documents, say so clearly."
)


# =====================================================
# CONVERSATION MEMORY SETTINGS
# =====================================================

MAX_CONVERSATION_TURNS = 5     # how many previous Q&A pairs to remember
MEMORY_STRATEGY = "window"    # window-based memory


# =====================================================
# VALIDATION FLAGS
# =====================================================

STRICT_SOURCE_ATTRIBUTION = True   # answers must include source references
ALLOW_OUT_OF_CONTEXT_ANSWER = False




