import faiss
import numpy as np

class VectorStoreManager:
    def __init__(self, dimension: int):
        """
        Initialize a local vector store using FAISS.
        
        Args:
            dimension (int): The dimension of the embedding vectors.
        """
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity search
        self.metadata = {}  # Store document metadata (e.g., text content)

    def store_embeddings(self, doc_id: str, embedding: np.ndarray, text_content: str):
        """
        Store a document's embedding locally.
        
        Args:
            doc_id (str): Unique identifier for the document.
            embedding (np.ndarray): The embedding vector.
            text_content (str): The document's content.
        """
        if doc_id in self.metadata:
            raise ValueError(f"Document ID '{doc_id}' already exists.")
        
        embedding = np.array(embedding).astype("float32")  # Ensure correct type for FAISS
        self.index.add(np.array([embedding]))  # Add the vector to the FAISS index
        self.metadata[self.index.ntotal - 1] = {"id": doc_id, "content": text_content}  # Map index to metadata

    def query_embeddings(self, query_embedding: np.ndarray, top_k: int = 5):
        """
        Query the vector store for similar embeddings.
        
        Args:
            query_embedding (np.ndarray): The query embedding vector.
            top_k (int): Number of closest matches to return.
        
        Returns:
            List[dict]: A list of matches with their metadata and similarity scores.
        """
        query_embedding = np.array(query_embedding).astype("float32").reshape(1, -1)
        distances, indices = self.index.search(query_embedding, top_k)  # Perform similarity search
        
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx != -1:  # Valid index
                result = self.metadata[idx]
                result["score"] = distance
                results.append(result)
        
        return results
