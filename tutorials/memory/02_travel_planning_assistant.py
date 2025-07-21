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

####################################################
# Building a Travel Planning Assistant with Memory #
####################################################

class TravelAssistant:
    def __init__(self, user_id):
        """Initialize travel assistant with memory for a specific user"""
        self.user_id = user_id

        # Configure memory for travel planning
        memory_config = {
            "vector_store": {
                "provider": "azure_ai_search",
                "config": {
                    "service_name": SEARCH_SERVICE_NAME,
                    "api_key": SEARCH_SERVICE_API_KEY,
                    "collection_name": "travel_memories",
                    "embedding_model_dims": AZURE_OPENAI_EMBEDDING_MODEL_DIMS,
                    "compression_type": "binary",
                },
            },
            "llm": {
                "provider": "azure_openai",
                "config": {
                    "model": AZURE_OPENAI_CHAT_COMPLETION_DEPLOYED_MODEL_NAME,
                    "temperature": 0.7,
                    "max_tokens": 800,
                    "azure_kwargs": {
                        "azure_deployment": AZURE_OPENAI_CHAT_COMPLETION_DEPLOYED_MODEL_NAME,
                        "api_version": AZURE_OPENAI_API_VERSION,
                        "azure_endpoint": AZURE_OPENAI_ENDPOINT,
                        "api_key": AZURE_OPENAI_API_KEY,
                    },
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
            "version": "v1.1",
        }

        self.memory = Memory.from_config(memory_config)
        self.azure_client = azure_openai_client
        print(f"Travel Assistant initialized for user {user_id}")

    def get_response(self, query, memory_context=True):
        """Get response from Azure OpenAI with memory context"""
        # Retrieve relevant memories if enabled
        memory_text = ""
        if memory_context:
            memories = self.memory.search(query, user_id=self.user_id)
            if 'results' in memories and memories['results']:
                memory_text = "\n\nRelevant information from previous conversations:\n"
                for i, mem in enumerate(memories['results'][:5], 1):
                    memory_text += f"{i}. {mem['memory']}\n"
                print(f"Including {len(memories['results'][:5])} memories in context")
            else:
                print("No relevant memories found")

        # Construct messages with system prompt and memory context
        messages = [
            {
                "role": "system",
                "content": "You are a helpful travel assistant for Singapore travel planning. "
                           "Be concise, specific, and helpful. Refer to the user by name when appropriate. "
                           "Recommend specific places when relevant."
            },
            {
                "role": "user",
                "content": f"{query}\n{memory_text}"
            }
        ]

        # Get response from Azure OpenAI
        response = self.azure_client.chat.completions.create(
            model=AZURE_OPENAI_CHAT_COMPLETION_DEPLOYED_MODEL_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=800,
        )

        # Extract response content
        response_content = response.choices[0].message.content

        # Store the conversation in memory
        conversation = [
            {"role": "user", "content": query},
            {"role": "assistant", "content": response_content}
        ]
        self.memory.add(conversation, user_id=self.user_id)

        return response_content

    def verify_memories(self):
        """Verify what memories have been stored"""
        all_memories = self.memory.get_all(user_id=self.user_id)
        print(f"\n===== STORED MEMORIES ({len(all_memories['results'])}) =====")
        for i, memory in enumerate(all_memories['results'], 1):
            print(f"{i}. {memory['memory']}")
        print("==============================\n")
        return all_memories
    
##############################
# Using the Travel Assistant #
##############################

# Create travel assistant for a user
assistant = TravelAssistant(user_id="vincent_singapore_2025")

# First interaction - Initial inquiry
query1 = "Hi, my name is Vincent. I'm planning a business trip to Singapore next month for about 5 days."
print(f"User: {query1}")
response1 = assistant.get_response(query1, memory_context=False)  # No memories yet
print(f"Assistant: {response1}\n")

# Second interaction - Specific question about fish and chips
query2 = "I need recommendations for Chili crab restaurants near Singapore Marina Bay cause I love the taste!"
print(f"User: {query2}")
response2 = assistant.get_response(query2)  # Should use memory context
print(f"Assistant: {response2}\n")

# Verify what memories have been stored
assistant.verify_memories()

######################################
# Searching for Specific Preferences #
######################################

search_query = "What are Vincent's preferences for food in Singapore?"
search_results = assistant.memory.search(search_query, user_id="vincent_singapore_2025")
print(f"Found {len(search_results['results'])} relevant memories:")
for i, result in enumerate(search_results['results'][:3], 1):
    print(f"{i}. {result['memory']} (Score: {result['score']:.4f})")