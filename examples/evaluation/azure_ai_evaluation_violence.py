import os 
from azure.ai.evaluation import ViolenceEvaluator
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

project = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)

# Initializing Violence Evaluator with project information
violence_eval = ViolenceEvaluator(
    azure_ai_project=project.scope,
    credential=DefaultAzureCredential())

# Running Violence Evaluator on single input row
violence_score = violence_eval(query="what's the capital of france", response="Paris")
print(violence_score)
