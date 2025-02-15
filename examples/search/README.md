# Search

## Install
```bash
python -m venv .venv [alt: uv venv .venv --python 3.xx]
.venv\Scripts\activate.bat [if not Windows: source .venv/bin/activate]
pip install -r requirements.txt
```

## Run example
```bash
python my_example.py
```

## Solution accelerators
- [RAG chat with Azure AI Search + Python](https://azure.github.io/ai-app-templates/repo/azure-samples/azure-search-openai-demo/)

## Todo
- Evaluate w/wout semantic ranker and query rewriting
- Evaluate w/wout semantic chunking
- AI Service integration to format response length
- Check out:
    - https://learn.microsoft.com/en-us/azure/search/tutorial-rag-build-solution-pipeline
    - https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python, 
    - https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/samples
    - https://github.com/Azure-Samples/azure-search-python-samples
    - https://learn.microsoft.com/en-us/azure/search/samples-python