from fastapi import FastAPI, UploadFile, File, HTTPException
from services.file_reader import FileReader
from services.vector_store import VectorStore
import logging
from typing import List
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize services
file_reader = FileReader()
vector_store = VectorStore()

from services.file_reader import FileReader
from services.vector_store import VectorStore

app = FastAPI()
logger = logging.getLogger(__name__)

# Initialize the services
file_reader = FileReader()
vector_store = VectorStore()

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    results = []

    allowed_types = {"application/pdf", "text/plain"}

    for file in files:
        logger.info(f"Processing file: {file.filename} of type {file.content_type}")

        if file.content_type not in allowed_types:
            logger.error(f"Unsupported file type: {file.filename}")
            results.append({"filename": file.filename, "status": "error", "message": "Unsupported file type"})
            continue

        try:
            # Step 1: Read and chunk the file
            text_chunks = file_reader.read_file(file)

            if not text_chunks:
                logger.warning(f"No text extracted from file: {file.filename}")
                results.append({"filename": file.filename, "status": "warning", "message": "No text extracted"})
                continue

            # Step 2: Store embeddings along with metadata
            store_result = vector_store.store_embeddings(text_chunks)

            results.append({"filename": file.filename, "status": "success", "processed_chunks": store_result["processed_chunks"]})
            logger.info(f"File processed successfully: {file.filename}")

        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            results.append({"filename": file.filename, "status": "error", "message": str(e)})

    return {"message": "Files processed", "results": results}


@app.post("/answer")
async def answer_query(data: dict):
    query = data["query"]

    # Step 1: Retrieve relevant chunks from vector store
    results = vector_store.search(query, top_k=5)

    if not results:
        return {"answer": "No relevant documents found.", "sources": []}

    # Convert any numpy.float32 values to Python float
    #for res in results:
    #    res["page_number"] = int(res["page_number"])  # Ensure it's an int
    #    res["distance"] = float(res["distance"])      # Ensure it's a float

    sources = "\n".join([
        f"Source: {res['filename']} (Page {res['page_number']})" 
        for res in results
    ])

    # Step 2: Prepare context for the LLM
    context = "\n".join([
        f"Source: {res['filename']} (Page {res['page_number']})\n{res['text']}" 
        for res in results
    ])


    full_prompt = f"Break down the following context into individual parts, analyse each part in complete detail and then answer the query by looking at the individual parts. Ensure that the answer is well detailed based on the breakdown of the context and the question {context}\nQuestion: {query}\nAnswer:"

    # Step 3: Run LLM
    try:
        process = subprocess.Popen(
            ["ollama", "run", "llama3", full_prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output, error = process.communicate()

        if error:
            return {"error": error.strip()}

        return {"answer": output.strip(), "sources": sources}
    except Exception as e:
        return {"error": str(e)}



