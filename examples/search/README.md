# Search

## Install
Install the [azd CLI](https://learn.microsoft.com/en-gb/azure/developer/azure-developer-cli/install-azd) for logging in.

Make sure you have the [uv](https://docs.astral.sh/uv/getting-started/installation) package manager installed.

Create and activate virtual environment:

```bash
uv venv --python=python3.12 .venv

# Windows:
.venv\Scripts\activate.bat
# Unix/MacOS:
source .venv/bin/activate

uv pip install -r requirements.txt
```

## Run
Open a notebook, pick the `.venv` kernel (in VS Code you may need to directly open the subfolder for it to be available), click `Run all`.

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
            - Tool with options: https://github.com/jelledruyts/azure-ai-search-lab
        - Multi turn chat demo: https://github.com/Azure-Samples/azure-search-openai-demo/
    - https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python, 
    - https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/search/azure-search-documents/samples
