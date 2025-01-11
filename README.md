# documentation_rag
Interact with knowledge base using an ai agent with this project

Why I created this project?
One can upload any text file and interact with it using llm locally on one's system. 
You can ask queries about the document you uploaded.
This means no data leaves your system and you can even run it without internet connection or external server side API calls.
This ensure better privacy than doing the same on similar online tools.

Example use case:
https://app.ekipa.de/challenges/ai-telekom-iot/brief

The LLM used for this is : Llama
You can install the open source version of llama to run on your system here : https://ollama.com/download 

Requirements:
1. User should be able to upload documents : text files and pdf
2. The system should pull relevant context from the uploaded files using a vector database.
3. The user should be able to input a query
4. The system should provide an output with indexing of the source from which it generated the result.


Architecture
The overall application is packaged as FastAPI.
The  software architecture involves developing a service based architecture that allows better separation of concerns and modularity.
It currently includes 3 services:
1. FileManager : allows user to upload text, extract content out of the file and save it
2. Embedding: creates an embedding out of the saved text
3. VectorStore: stores the embedding in a vector database

Using API:
Requirements:
Python 3.10 and above

1. clone the repo
2. move to the folder where the repo is cloned (using terminal like powershell etc)
3. pip install -r requirements.txt
4. run the app using the command : python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000 ( note that one can change the port based on the availability)
5. The app would be running on  http://127.0.0.1:8000
6. Either use curl request or the FastAPI swagger UI to use the api. In order to use the UI go to: http://127.0.0.1:8000/docs

The client uploads a document (sending a HTTP POST request) to file_manager service. 
The content is extracted within the file_manager and saved.
The extracted content is then passed to the EmbeddingManager. An embedding is created out of the extracted content
The embedding is then passed to the vector store where it is stored in the vector database.
The user then asks a query (sending a HTTP POST request) to the vector store and retracts the content-
