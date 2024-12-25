from fastapi import FastAPI, UploadFile, File, HTTPException
from services.file_manager import FileManager
from services.embeddings import EmbeddingManager
from services.vector_store import VectorStoreManager
from services.query_handler import QueryHandler

app = FastAPI()

# Instantiate services
file_manager = FileManager(upload_dir="uploaded_files")
embedding_manager = EmbeddingManager(model_name="all-MiniLM-L6-v2")
vector_store = VectorStoreManager(database_url="http://localhost:8001")
query_handler = QueryHandler(embedding_manager, vector_store)

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    if not file_manager.validate_file(file):
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    
    file_path = await file_manager.save_file(file)
    text_content = file_manager.parse_file(file_path)
    embedding_manager.process_document(file_path, text_content, vector_store)
    
    return {"message": "Document uploaded and processed successfully"}

@app.post("/query/")
async def query_documents(query: str):
    response = query_handler.handle_query(query)
    return response
