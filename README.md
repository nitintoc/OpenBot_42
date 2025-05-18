# OpenBot_42

Project Vision:
Build a fully open source AI agent that is resource efficient and can be run locally to ensure complete data privacy and security.

Project Goals:
1. Enable Retrieval Augmented Generation
2. Enable referencing to sources
3. Enable reasoning capabilities in the model
4. Enable multi-modal capabilities and the ability to work with different types of data that include text files, pdf files, web url, etc
5. Enable web search and abstract indexation
6. Ensure plug and play use of open source models
7. Make this open source API that other projects can use to build their own LLM agents
8. Ensure robust, reliable and scalable code.


Using API:
Requirements:
Python 3.10 and above

1. clone the repo
2. move to the folder where the repo is cloned (using terminal like powershell etc)
3. pip install -r requirements.txt
4. run the app using the command : python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000 ( note that one can change the port based on the availability)
5. The app would be running on  http://127.0.0.1:8000
6. Either use curl request or the FastAPI swagger UI to use the api. In order to use the UI go to: http://127.0.0.1:8000/docs


