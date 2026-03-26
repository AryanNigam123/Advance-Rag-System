from typing import List, Dict
from app.embeddings.embedder import EmbeddingGenerator

class SemanticRetriever:
    """
    Converts queries into embeddings and retrieves relevant chunks.
    """

    def __init__(self, vector_store, top_k: int = 5):
        self.vector_store = vector_store
        self.top_k = top_k
        self.embedder = EmbeddingGenerator()

    def retrieve(self, query: str) -> List[Dict]:
        query_embedding = self.embedder.model.encode(
            query,
            convert_to_numpy=True
        )

        return self.vector_store.search(
            query_embedding,
            self.top_k
        )
