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


