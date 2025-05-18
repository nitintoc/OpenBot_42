# OpenBot_42

**OpenBot_42** is a fully open source AI agent focused on resource efficiency, local operation, and complete data privacy and security.

## Vision

Build an AI agent that is:
- Resource efficient
- Usable locally for maximum privacy and security

## Project Goals

1. Support Retrieval Augmented Generation (RAG)
2. Reference sources in responses
3. Provide reasoning capabilities
4. Enable multi-modal data handling (text, PDF, web URLs, etc.)
5. Integrate web search and abstract indexation
6. Allow plug-and-play use of open source models
7. Expose an open API for building custom LLM agents
8. Ensure robust, reliable, and scalable code

---

## Getting Started

### Requirements

- Python 3.10 or above

### Installation & Usage

1. **Clone the repository:**
    ```bash
    git clone https://github.com/nitintoc/OpenBot_42.git
    cd OpenBot_42
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application:**
    ```bash
    python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
    ```
    *(You may change the port if needed)*

4. **Access the API:**
    - The app will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)
    - Use cURL or the FastAPI Swagger UI at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## License

This project is open source and available under the [appropriate license]. *(Replace with actual license if available.)*
