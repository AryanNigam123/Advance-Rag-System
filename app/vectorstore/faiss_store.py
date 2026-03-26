import faiss
import numpy as np
from typing import List, Dict

class FAISSVectorStore:
    """
    Handles FAISS index creation and vector storage.
    """

    def __init__(self, embedding_dim: int):
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.metadata_store = []

    def add_embeddings(self, embedded_chunks: List[Dict]):
        vectors = np.array(
            [chunk["embedding"] for chunk in embedded_chunks]
        ).astype("float32")

        self.index.add(vectors)
        self.metadata_store.extend(embedded_chunks)

    def search(self, query_vector: np.ndarray, top_k: int = 5):
        query_vector = query_vector.reshape(1, -1).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata_store):
                results.append(self.metadata_store[idx])

        return results
