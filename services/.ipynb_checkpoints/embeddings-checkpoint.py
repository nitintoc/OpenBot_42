from typing import List
from sentence_transformers import SentenceTransformer
import logging

class EmbeddingManager:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the EmbeddingManager with a pre-trained model.
        
        Args:
            model_name (str): Name of the pre-trained model to use.
        """
        try:
            self.model = SentenceTransformer(model_name)
            logging.info(f"Embedding model '{model_name}' loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading model '{model_name}': {e}")
            raise

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
        
        try:
            embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            logging.error(f"Error generating embeddings: {e}")
            raise

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
        if not document_id or not text:
            raise ValueError("Document ID and text cannot be empty.")
        
        try:
            embedding = self.generate_embeddings([text])[0]
            vector_store.store_embeddings(doc_id=document_id, embedding=embedding, text_content=text)
            logging.info(f"Processed and stored document '{document_id}'.")
        except Exception as e:
            logging.error(f"Error processing document '{document_id}': {e}")
            raise

    def process_documents(self, documents: List[dict], vector_store, batch_size: int = 32):
        """
        Batch-process multiple documents, generating embeddings and storing them.

        Args:
            documents (List[dict]): List of documents, each with 'id' and 'content'.
            vector_store: Instance of the vector store to save embeddings.
            batch_size (int): Number of documents to process in each batch.

        Returns:
            None
        """
        if not documents:
            raise ValueError("Input documents list is empty.")
        
        document_ids = [doc["id"] for doc in documents]
        texts = [doc["content"] for doc in documents]
        
        try:
            for start in range(0, len(texts), batch_size):
                batch_ids = document_ids[start:start + batch_size]
                batch_texts = texts[start:start + batch_size]
                
                embeddings = self.generate_embeddings(batch_texts)
                for doc_id, embedding, text in zip(batch_ids, embeddings, batch_texts):
                    vector_store.store_embeddings(doc_id=doc_id, embedding=embedding, text_content=text)
                
                logging.info(f"Processed and stored batch of {len(batch_ids)} documents.")
        except Exception as e:
            logging.error(f"Error processing documents: {e}")
            raise
