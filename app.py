from fastapi import FastAPI, UploadFile
from services.file_reader import FileReader
from services.vector_store import VectorStore
import subprocess

app = FastAPI()

# Initialize the classes
file_reader = FileReader()
vector_store = VectorStore()


@app.post("/upload")
async def upload_file(file: UploadFile):
    try:
        # Step 1: Read and chunk the file
        text_chunks = file_reader.read_file(file)
        # Step 2: Generate embeddings and store in vector database
        result = vector_store.store_embeddings(text_chunks)
        return result
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "An error occurred during file processing: " + str(e)}


@app.post("/answer")
async def answer_query(data: dict):
    query = data["query"]

    # Step 1: Generate query embedding
    query_embedding = vector_store.generate_embedding(query).reshape(1, -1)

    # Step 2: Search relevant documents in FAISS index
    k = 5  # Number of results to retrieve
    distances, indices = vector_store.get_index().search(query_embedding, k)

    # Step 3: Build context from search results
    context = ""
    for idx in indices[0]:
        if idx == -1:  # No more results
            continue
        vector_id = list(vector_store.get_metadata_store().keys())[idx]
        match = vector_store.get_metadata_store()[vector_id]
        context += f"Source: {match['filename']}, Page: {match.get('page_number', 'N/A')}\n{match['text']}\n"

    full_prompt = f"{context}Question: {query}\nAnswer:"

    # Step 4: Call the local LLM (Ollama or similar)
    try:
        process = subprocess.Popen(
            ["ollama", "run", "llama3", full_prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output, error = process.communicate()
        print(output)

        if error:
            return {"error": error.decode('utf-8')}

        return {"answer": str(output)}
    except Exception as e:
        return {"error": str(e)}

