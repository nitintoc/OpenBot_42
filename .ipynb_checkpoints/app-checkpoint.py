from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from pydantic import BaseModel
from typing import List
import numpy as np
from services.file_manager import FileManager
from services.embeddings import EmbeddingManager
from services.vector_store import VectorStoreManager
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

# Initialize services
file_manager = FileManager(upload_dir="uploads")
embedding_manager = EmbeddingManager(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize vector store with embedding dimension
DIMENSION = 384  # Embedding dimension used by the model
vector_store = VectorStoreManager(dimension=DIMENSION)

# Request body model for querying documents
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Upload multiple documents and store their embeddings.
    """
    stored_documents = []
    
    for file in files:
        try:
            # Validate the file type
            if not file_manager.file_validate(file):
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

            # Save file to disk
            file_path = await file_manager.save_file(file)
            
            # Extract text from the file
            text_content = file_manager.parse_file(file_path)
            
            # Generate embeddings
            embeddings = embedding_manager.generate_embeddings([text_content])
            
            # Ensure embeddings are NumPy arrays
            if not isinstance(embeddings, np.ndarray):
                embeddings = np.array(embeddings, dtype="float32")
            
            # Store embeddings in the vector store
            doc_id = file.filename  # Using filename as unique document ID
            vector_store.store_embeddings(doc_id, embeddings[0], text_content)
            
            stored_documents.append({"id": doc_id, "content": text_content})
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file '{file.filename}': {str(e)}")
    
    return JSONResponse(
        content={"message": "Files uploaded and embeddings stored", "documents": stored_documents},
        status_code=201
    )


@app.post("/query")
async def query_documents(query: str = Query(..., description="The query text to search for"),
                           top_k: int = Query(5, description="The number of results to return")):
    """
    Query the stored embeddings for similar documents.
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query text is required")

    try:
        # Generate embeddings for the query
        embeddings = embedding_manager.generate_embeddings([query])
        
        # Ensure embeddings are NumPy arrays
        if not isinstance(embeddings, np.ndarray):
            embeddings = np.array(embeddings, dtype="float32")
        
        # Query the vector store
        query_embedding = embeddings[0]
        results = vector_store.query_embeddings(query_embedding, top_k=top_k)

        # Convert results to a JSON serializable format
        serializable_results = []
        for result in results:
            serializable_results.append({
                "id": result["id"],
                "content": result["content"],
                "score": float(result["score"])
            })
        
        return JSONResponse(
            content={"query": query, "results": serializable_results},
            status_code=200
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the query: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
