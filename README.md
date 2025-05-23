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
cd Open_API_Backend
docker build -t api_back:1 .
docker run --rm -d --name api_back --network=host api_back:1
```

### Agent UP
```Bash
cd ../../
adk web
# <IP:8000> Final service
```
