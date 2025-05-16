# adk_ai_agent
Integrating REST APIs with OpenAPI¶
ADK simplifies interacting with external REST APIs by automatically generating callable tools directly from an OpenAPI Specification (v3.x). 

### Resource
* Ubuntu 24.04.1 с среда контейнеров Docker/NGC
* NGC Cli
* Docker 27.3.1
* nvidia-container-toolkit
* cuda-toolkit 12.6
* anaconda 24.9.2 - python 3.9
* pytorch 2.5.1 - python 3.11
* tensorflow-gpu 2.4.1
* open-driver 560
* HDD 160Gb
* RTX2080TI 11GB 


### Infrastructure UP
```Bash
git clone https://github.com/geksogen/adk_ai_agent.git
cd adk_ai_agent/infrastructure/
sh configure_VM.sh
ollama run qwen2.5:7b
# <IP:11434> Final service
```

### Agent UP
```Bash
echo "from . import agent" > ../agent_open_api_tool/__init__.py
cd ../../
adk web
# <IP:8000> Final service
```
