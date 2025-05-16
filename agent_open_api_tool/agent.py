from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

import asyncio
import uuid # For unique session IDs
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# --- OpenAPI Tool Imports ---
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset

# --- Agent Definition ---
root_agent = Agent(
    name="weather_time_agent",
    model=LiteLlm(model="ollama/qwen2.5:7b", api_base="http://176.99.131.76:11434"),
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[],
)
