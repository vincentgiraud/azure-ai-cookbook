import asyncio
from dotenv import load_dotenv
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.mcp import MCPSsePlugin

"""
The following sample demonstrates how to create a chat completion agent that
answers questions about Github using a Semantic Kernel Plugin from a MCP server. 

It uses the Azure OpenAI service to create a agent, so make sure to 
set the required environment variables for the Azure AI Foundry service:
- AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
- Optionally: AZURE_OPENAI_API_KEY 
If this is not set, it will try to use DefaultAzureCredential.

"""

load_dotenv()  

# Simulate a conversation with the agent
USER_INPUTS = [
    "What are the latest 5 python issues in Microsoft/semantic-kernel?",
    "Are there any untriaged python issues?",
    "What is the status of issue #12750?",
]


async def main():
    # 1. Create the agent
    async with MCPSsePlugin(
        name="Github",
        description="Github Plugin",
        url="https://gitmcp.io/microsoft/semantic-kernel",
    ) as github_plugin:
        agent = ChatCompletionAgent(
            service=AzureChatCompletion(),
            name="IssueAgent",
            instructions="Answer questions about the Microsoft semantic-kernel github project.",
            plugins=[github_plugin],
        )

        for user_input in USER_INPUTS:
            # 2. Create a thread to hold the conversation
            # If no thread is provided, a new thread will be
            # created and returned with the initial response
            thread: ChatHistoryAgentThread | None = None

            print(f"# User: {user_input}")
            # 3. Invoke the agent for a response
            response = await agent.get_response(messages=user_input, thread=thread)
            print(f"# {response.name}: {response} ")
            thread = response.thread

            # 4. Cleanup: Clear the thread
            await thread.delete() if thread else None

        """
        Sample output:
# User: What are the latest 5 python issues in Microsoft/semantic-kernel?
# IssueAgent: Here are the latest 5 Python issues in the Microsoft/Semantic-Kernel GitHub repository:

1. **[Python: New Feature: Multi-Agent Orchestration Termination Strategy Support](https://github.com/microsoft/semantic-kernel/issues/12750)**
   - *Author:* vamsithumma2812
   - *Created:* Jul 20, 2025
   - *Labels:* agents, python, feature
   - *Status:* Open

2. **[Python: Bug: adding TOOL message to ChatHistory causes validation error in ChatMessageContent](https://github.com/microsoft/semantic-kernel/issues/12744)**
   - *Author:* mattiasu96
   - *Created:* Jul 18, 2025
   - *Labels:* bug, chat history, python
   - *Status:* Open

3. **[.Net: Python: AsyncConnectionPool Connection Timeout with Semantic Kernel PostgresSettings](https://github.com/microsoft/semantic-kernel/issues/12732)**
   - *Author:* markwallace-microsoft
   - *Created:* Jul 16, 2025
   - *Labels:* .NET, memory connector, python, bug
   - *Status:* Open

4. **[Python: Message: Unsupported parameter: 'temperature' is not supported with this model.](https://github.com/microsoft/semantic-kernel/issues/12727)**
   - *Author:* mollaosmanoglu
   - *Created:* Jul 16, 2025
   - *Labels:* bug, python
   - *Status:* Open

5. **[Python: Bug: ChatHistoryTruncationReducer cuts off TOOL_CALLS role message making the following TOOL role messages orphan in AgentThread history](https://github.com/microsoft/semantic-kernel/issues/12708)**
   - *Author:* SaurabhNiket231
   - *Created:* Jul 12, 2025
   - *Labels:* bug, python
   - *Status:* Open

You can find more details or provide feedback on each issue by following the provided links.
# User: Are there any untriaged python issues?
# IssueAgent: There are currently no untriaged (no milestone, no assignee) open issues labeled "python" in the microsoft/semantic-kernel repository. 
# User: What is the status of issue #12750?
# IssueAgent: Issue [#12750](https://github.com/microsoft/semantic-kernel/issues/12750) is titled **"Python: New Feature: Multi-Agent Orchestration Termination Strategy Support"** and is currently in the **Open** state.

**Summary**:
- The request is for a termination strategy for multi-agent orchestrations (specifically in the "MagenticOne" orchestrator), similar to what is available in AutoGen and Semantic Kernel's AgentGroupChat.
- The issue points out problems like infinite loops, inadequate max_round_count behavior, and missing custom termination conditions for orchestrations, leading to excessive token usage and usability issues.
- It proposes implementing termination strategies for multi-agent orchestrations for consistency with other features.
- The issue is assigned to **TaoChenOSU**.
- There are no linked pull requests or milestone, and it's part of the "Semantic Kernel" project but has **no specific status set within the project board**.

**Current status:** Open, awaiting further feedback and action. No official response about when or if the feature will be implemented yet.

You can view or track the issue here: [https://github.com/microsoft/semantic-kernel/issues/12750](https://github.com/microsoft/semantic-kernel/issues/12750)
        """


if __name__ == "__main__":
    asyncio.run(main())
