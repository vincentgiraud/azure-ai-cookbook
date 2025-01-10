<div style="display: flex; align-items: center; justify-content: left;">
  <img src="./images/azure-ai-foundry-logo.svg" alt="drawing" width="100"/>
  <h1>Azure AI Cookbook</h1>
</div>

Examples and guides for using the Azure AI services

## Local examples execution

The python project is managed by `pyproject.toml` and the [uv package manager](https://docs.astral.sh/uv/getting-started/installation/).
Install uv prior executing.

To run locally:

Mind the `sample.env` file - by default the application will try to read AZD environment variables and falls back on `.env` only when it does not find one.

Activate the `.venv` virtual environment:

```shell
cd examples/agents
uv sync
uv run hello.py
```