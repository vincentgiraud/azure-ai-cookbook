# Search

## Install

```bash
python -m venv .venv
.venv\Scripts\activate.bat [if not Windows: source .venv/bin/activate]
pip install -r requirements.txt
```

## Run
Open a notebook, pick the `.venv` kernel (in VSC you may need to directly open the subfoder for it to be available), click `Run all`.

## Solution accelerator
- [RAG chat with Azure AI Search + Python](https://azure.github.io/ai-app-templates/repo/azure-samples/azure-search-openai-demo/)

## Todo
- Evaluate w/wout semantic ranker and query rewriting
- Evaluate w/wout semantic chunking
- AI Service integration to format response length
- Check out:
    - https://github.com/Azure-Samples/azure-search-python-samples
        - Focus: https://github.com/Azure-Samples/azure-search-python-samples/tree/main/Tutorial-RAG
        - Doc: https://learn.microsoft.com/en-us/azure/search/samples-python
    - https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python, 
    - https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/samples
