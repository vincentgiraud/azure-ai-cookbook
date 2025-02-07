import os
import jsonref
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import OpenApiTool, OpenApiAnonymousAuthDetails
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# It should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# Customers need to login to Azure subscription via Azure CLI and set the environment variables

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)

with open(os.path.join(os.path.dirname(__file__), 'catfacts_api.json'), 'r') as f:
    openapi_spec = jsonref.loads(f.read())

# Create Auth object for the OpenApiTool (note that connection or managed identity auth setup requires additional setup in Azure)
auth = OpenApiAnonymousAuthDetails()

# Initialize agent OpenAPI tool using the read in OpenAPI spec
openapi = OpenApiTool(name="get_catfacts", spec=openapi_spec, description="Facts about cats", auth=auth)

# Create agent with OpenAPI tool and process assistant run
with project_client:
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-assistant",
        instructions="You are a helpful assistant",
        tools=openapi.definitions
    )
    print(f"Created agent, ID: {agent.id}")

    # Create thread for communication
    thread = project_client.agents.create_thread()
    print(f"Created thread, ID: {thread.id}")

    # Create message to thread
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Tell me a cat fact",
    )
    print(f"Created message, ID: {message.id}")

    # Create and process agent run in thread with tools
    run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Delete the assistant when done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")

    # Fetch and log all messages
    messages = project_client.agents.list_messages(thread_id=thread.id)
    print(f"Messages: {messages}")