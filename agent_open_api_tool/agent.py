import datetime
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


root_agent = Agent(
    name="weather_time_agent",
    model=LiteLlm(model="ollama/qwen2.5:7b", api_base="http://<IP>>:11434"),
    description="Answers user questions about the capital city of a given country.",
    instruction="""You are an agent that provides the capital city of a country... (previous instruction text)""",
    tools=[] # Provide the function directly
)
