import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from dotenv import load_dotenv

load_dotenv

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
deployment = os.getenv("AZURE_OPENAI_MODEL", "")
      
# Initialize Azure OpenAI client with Entra ID authentication
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

reasoningclient = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", ""),
)

question = "Write an article about planning, sizing and architecting AI Agents"

messages = [
        {
            "role": "user",
            "content": [
                { "type": "input_text", "text": f"{question}" },
            ]
        }
    ]

response = reasoningclient.responses.create(
    input=messages,
    model=deployment,
    reasoning={
                "effort": "high",
                "summary": "detailed" # auto, concise, or detailed (currently only supported with o4-mini and o3)
            },
    max_output_tokens=10000,
)

print(response.output_text)
