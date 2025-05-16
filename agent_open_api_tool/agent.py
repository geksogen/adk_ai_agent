from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


root_agent = Agent(
    name="weather_time_agent",
    model=LiteLlm(model="ollama/qwen2.5:7b", api_base="http://81.94.155.187:11434"),
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[],
)
