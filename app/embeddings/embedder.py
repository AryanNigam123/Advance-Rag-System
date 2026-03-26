import streamlit as st
from sentence_transformers import SentenceTransformer
from app.config.settings import EMBEDDING_MODEL_NAME, EMBEDDING_DEVICE

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(
        EMBEDDING_MODEL_NAME,
        device=EMBEDDING_DEVICE
    )

class EmbeddingGenerator:
    def __init__(self):
        self.model = load_embedding_model()

    def embed_chunks(self, chunks):
        texts = [chunk["chunk_text"] for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        embedded_chunks = []

        for chunk, vector in zip(chunks, embeddings):
            embedded_chunks.append({
                   "chunk_id": chunk["chunk_id"],
    "embedding": vector,
    "chunk_text": chunk["chunk_text"],  
    "metadata": {
        "session_id": chunk["session_id"],
        "source_pdf": chunk["source_pdf"],
        "page_number": chunk["page_number"],
                }
            })

        return embedded_chunks
