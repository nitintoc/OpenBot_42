import uuid
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

class VectorStore:
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2", embedding_dimension: int = 384):
        # Initialize embedding model
        self.model = SentenceTransformer(embedding_model)

        # FAISS index with ID mapping (for retrieval)
        self.index = faiss.IndexFlatL2(embedding_dimension)  # L2 distance for similarity search
        
        # Store embeddings with associated metadata
        self.metadata_store = []  # List to track metadata corresponding to FAISS indices

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generates an embedding for the given text.
        """
        return self.model.encode(text, convert_to_numpy=True)

    def store_embeddings(self, text_chunks):
        """
        Generates embeddings for text chunks and stores them in the FAISS vector database with metadata.
        """
        embeddings = []
        for chunk in text_chunks:
            embedding = self.generate_embedding(chunk["text"])
            embeddings.append(embedding)
            
            # Store metadata separately in list (keeping index order consistent)
            self.metadata_store.append({
                "id": str(uuid.uuid4()),
                "filename": chunk["metadata"]["filename"],
                "page_number": chunk["metadata"].get("page_number", "N/A"),
                "text": chunk["text"]
            })

        # Convert embeddings list to numpy array and add to FAISS index
        self.index.add(np.array(embeddings))

        return {"status": "success", "processed_chunks": len(text_chunks)}

    def search(self, query: str, top_k: int = 5):
        query_embedding = self.generate_embedding(query).reshape(1, -1)
        distances, indices = self.index.search(query_embedding, top_k)
    
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx == -1 or idx >= len(self.metadata_store):
                continue
            
            metadata = self.metadata_store[idx]
            results.append({
                "filename": metadata["filename"],
                "page_number": metadata["page_number"],
                "text": metadata["text"],
                "distance": float(distance)  # Convert numpy.float32 to Python float
            })
    
        return results
    


    def get_index(self):
        """
        Returns the FAISS index.
        """
        return self.index

    def get_metadata_store(self):
        """
        Returns stored metadata.
        """
        return self.metadata_store
