# Azure AI Agents and MCP Resources

Sources:
<https://devblogs.microsoft.com/foundry/integrating-azure-ai-agents-mcp/>
<https://code.visualstudio.com/docs/copilot/chat/mcp-servers>

Setup path and run server:
![alt text](image.png)

Add env vars to .env

Add tools to Github Copilot agent in Visual Studio Code:
![alt text](image-2.png)
![alt text](image-1.png)

Running the server standalone:

```shell
cd ../agents
source .venv/Scripts/activate
az login
uv run -m azure_agent_mcp_server
```
