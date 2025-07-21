# https://devblogs.microsoft.com/foundry/azure-ai-mem0-integration/

import os
from mem0 import Memory
from openai import AzureOpenAI

from dotenv import load_dotenv
load_dotenv()

# Load Azure OpenAI configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_CHAT_COMPLETION_DEPLOYED_MODEL_NAME = os.getenv("AZURE_OPENAI_CHAT_COMPLETION_DEPLOYED_MODEL_NAME")
AZURE_OPENAI_EMBEDDING_DEPLOYED_MODEL_NAME = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYED_MODEL_NAME")
AZURE_OPENAI_EMBEDDING_MODEL_DIMS= os.getenv("AZURE_OPENAI_EMBEDDING_MODEL_DIMS")
AZURE_OPENAI_API_VERSION =  os.getenv("AZURE_OPENAI_API_VERSION")

# Load Azure AI Search configuration
SEARCH_SERVICE_ENDPOINT = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
SEARCH_SERVICE_API_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY")
SEARCH_SERVICE_NAME = os.getenv("AZURE_SEARCH_SERVICE_NAME")

# Create Azure OpenAI client
azure_openai_client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION
)

#########################################################
# Basic Memory Operations with Mem0 and Azure AI Search #
#########################################################

# Configure Mem0 with Azure AI Search
memory_config = {
    "vector_store": {
        "provider": "azure_ai_search",
        "config": {
            "service_name": SEARCH_SERVICE_NAME,
            "api_key": SEARCH_SERVICE_API_KEY,
            "collection_name": "memories",
            "embedding_model_dims": AZURE_OPENAI_EMBEDDING_MODEL_DIMS,
        },
    },
    "embedder": {
        "provider": "azure_openai",
        "config": {
            "model": AZURE_OPENAI_EMBEDDING_DEPLOYED_MODEL_NAME,
            "embedding_dims": AZURE_OPENAI_EMBEDDING_MODEL_DIMS,
            "azure_kwargs": {
                "api_version": AZURE_OPENAI_API_VERSION,
                "azure_deployment": AZURE_OPENAI_EMBEDDING_DEPLOYED_MODEL_NAME,
                "azure_endpoint": AZURE_OPENAI_ENDPOINT,
                "api_key": AZURE_OPENAI_API_KEY,
            },
        },
    },
    "llm": {
        "provider": "azure_openai",
        "config": {
            "model": AZURE_OPENAI_CHAT_COMPLETION_DEPLOYED_MODEL_NAME,
            "temperature": 0.1,
            "max_tokens": 2000,
            "azure_kwargs": {
                "azure_deployment": AZURE_OPENAI_CHAT_COMPLETION_DEPLOYED_MODEL_NAME,
                "api_version": AZURE_OPENAI_API_VERSION,
                "azure_endpoint": AZURE_OPENAI_ENDPOINT,
                "api_key": AZURE_OPENAI_API_KEY,
            },
        },
    },
    "version": "v1.1",
}

# Initialize memory 
memory = Memory.from_config(memory_config)
print("Mem0 initialized with Azure AI Search")

####################
# Storing Memories #
####################

# Simple statements
memory.add(
    "I enjoy hiking in national parks and taking landscape photos.",
    user_id="demo_user"
)

# Conversations
conversation = [
    {"role": "user", "content": "I'm planning a trip to Japan in the fall."},
    {"role": "assistant", "content": "That's a great time to visit Japan!"},
    {"role": "user", "content": "I'd like to visit Tokyo and Kyoto, and see Mount Fuji."}
]
memory.add(conversation, user_id="demo_user")

# Memories with metadata
memory.add(
    "I prefer window seats on long flights and usually bring my own headphones.",
    user_id="demo_user",
    metadata={"category": "travel_preferences", "importance": "medium"}
)

######################
# Searching Memories #
######################

search_results = memory.search(
    "What are this user's travel plans?",
    user_id="demo_user",
    limit=3
)

for i, result in enumerate(search_results['results'], 1):
    print(f"{i}. {result['memory']} (Score: {result['score']:.4f})")


###########################
# Retrieving All Memories #
###########################

all_memories = memory.get_all(user_id="demo_user")
print(f"Total memories: {len(all_memories['results'])}")
