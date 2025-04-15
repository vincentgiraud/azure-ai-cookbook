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
