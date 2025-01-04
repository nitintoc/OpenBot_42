import uuid
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class VectorStore:
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2", embedding_dimension: int = 384):
        # Initialize embedding model
        self.model = SentenceTransformer(embedding_model)
        # Initialize FAISS index
        self.index = faiss.IndexFlatL2(embedding_dimension)  # L2 distance for similarity search
        self.metadata_store = {}  # Dictionary to map vector IDs to metadata

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generates an embedding for the given text.
        """
        return self.model.encode(text, convert_to_tensor=False)

    def store_embeddings(self, text_chunks):
        """
        Generates embeddings for text chunks and stores them in the FAISS vector database.
        """
        for chunk in text_chunks:
            embedding = self.generate_embedding(chunk["text"])
            vector_id = str(uuid.uuid4())
            self.index.add(np.array([embedding]))  # Add vector to FAISS index
            self.metadata_store[vector_id] = {**chunk["metadata"], "text": chunk["text"]}

        return {"status": "success", "processed_chunks": len(text_chunks)}

    def get_index(self):
        return self.index

    def get_metadata_store(self):
        return self.metadata_store
