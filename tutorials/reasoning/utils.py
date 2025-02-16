import os
import base64
from openai import AzureOpenAI

def o1_tools(messages,model,tools):

    # Set up Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint = os.environ.get("AZURE_OPENAI_API_ENDPOINT"),
        api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )

    # Request OpenAI API
    response = client.beta.chat.completions.parse(
        messages=messages,
        tools=tools,
        model=model
    )

    # print(response.choices[0].message.content)
    return response.model_dump_json()

def o1_vision(file_path,prompt,model):
    
    with open(file_path, 'rb') as file:
        base64_image = base64.b64encode(file.read()).decode('utf-8')
    
    chat_prompt = [
        {
            "role": "developer",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64,"+base64_image
                    }
                }
            ]
        }
    ] 

    # Set up Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint = os.environ.get("AZURE_OPENAI_API_ENDPOINT"),
        api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )

    # Request OpenAI API
    response = client.beta.chat.completions.parse(
        messages=chat_prompt,
        model=model
    )

    # print(response.choices[0].message.content)
    return response.model_dump_json()
