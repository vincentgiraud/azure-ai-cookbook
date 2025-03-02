"""
Text-to-Image Generation Agent using Azure OpenAI and SmalAgents.

This script sets up an AI agent capable of generating images from text descriptions
using Azure OpenAI's language model and HuggingFace's text-to-image tools.
"""

import os
from dotenv import load_dotenv
from smolagents.models import AzureOpenAIServerModel
from smolagents import CodeAgent, load_tool, GradioUI, DuckDuckGoSearchTool, ToolCallingAgent, VisitWebpageTool

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

endpoint = "http://0.0.0.0:6006/v1/traces"
trace_provider = TracerProvider()
trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))

SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)

load_dotenv()

model = AzureOpenAIServerModel(
    model_id = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
)

search_tool = DuckDuckGoSearchTool()

search_agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool(), VisitWebpageTool()],
    model=model,
    name="search_agent",
    description="This is an agent that can do web search.",
)

manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[search_agent],
)
manager_agent.run(
    "If the US keeps its 2024 growth rate, how many years will it take for the GDP to double?"
)

# Navigate to http://0.0.0.0:6006/projects/ to inspect your run.