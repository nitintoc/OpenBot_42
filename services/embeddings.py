from typing import List
from sentence_transformers import SentenceTransformer

class EmbeddingManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the EmbeddingManager with a pre-trained model.
        
        Args:
            model_name (str): Name of the pre-trained model to use.
        """
        self.model = SentenceTransformer(model_name)
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of text documents.

        Args:
            texts (List[str]): List of text strings to generate embeddings for.

        Returns:
            List[List[float]]: A list of embeddings (one per input text).
        """
        if not texts:
            raise ValueError("Input text list is empty")
        
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        return embeddings.tolist()

    def process_document(self, document_id: str, text: str, vector_store):
        """
        Generate embeddings for a single document and store them in a vector database.

        Args:
            document_id (str): Unique identifier for the document.
            text (str): The document's content.
            vector_store: Instance of the vector store to save embeddings.

        Returns:
            None
        """
        # Generate embedding for the document
        embedding = self.generate_embeddings([text])[0]
        
        # Store embedding in the vector database
        vector_store.add_embedding(document_id=document_id, embedding=embedding, metadata={"text": text})
    
    def process_documents(self, documents: List[dict], vector_store):
        """
        Batch-process multiple documents, generating embeddings and storing them.

        Args:
            documents (List[dict]): List of documents, each with 'id' and 'content'.
            vector_store: Instance of the vector store to save embeddings.

        Returns:
            None
        """
        document_ids = [doc["id"] for doc in documents]
        texts = [doc["content"] for doc in documents]
        
        # Generate embeddings in batches
        embeddings = self.generate_embeddings(texts)
        
        # Store embeddings in the vector database
        for doc_id, embedding, text in zip(document_ids, embeddings, texts):
            vector_store.add_embedding(document_id=doc_id, embedding=embedding, metadata={"text": text})
