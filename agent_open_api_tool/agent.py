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

APP_NAME_OPENAPI = "openapi_petstore_app"
USER_ID_OPENAPI = "user_openapi_1"
SESSION_ID_OPENAPI = f"session_openapi_{uuid.uuid4()}" # Unique session ID
AGENT_NAME_OPENAPI = "petstore_manager_agent"
GEMINI_MODEL = "gemini-2.0-flash"

# --- Sample OpenAPI Specification (JSON String) ---
# A basic Pet Store API example using httpbin.org as a mock server
openapi_spec_string = """
{
  "openapi": "3.0.2",
  "info": {
    "title": "FastAPI",
    "version": "0.1.0"
  },
  "servers": [
    {
      "url": "http://81.94.158.220:8082/",
      "description": "Mock server OpenAPI"
    }
  ],
  "paths": {
    "/users/": {
      "post": {
        "summary": "Create User",
        "operationId": "create_user_users__post",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/User"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/UserWithID"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      },
      "get": {
        "summary": "Read Users",
        "operationId": "read_users_users__get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/UserWithID"
                  }
                }
              }
            }
          }
        }
      }
    },
    "/users/name/{user_name}": {
      "delete": {
        "summary": "Delete User By Name",
        "operationId": "delete_user_by_name_users_name__user_name__delete",
        "parameters": [
          {
            "name": "user_name",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/openapi.json": {
      "get": {
        "summary": "Get Openapi Json",
        "operationId": "get_openapi_json_openapi_json_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "HTTPValidationError": {
        "type": "object",
        "properties": {
          "detail": {
            "type": "array",
            "items": {
              "$ref": "#/components/schemas/ValidationError"
            }
          }
        }
      },
      "User": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "email": {
            "type": "string"
          }
        },
        "required": [
          "name",
          "email"
        ]
      },
      "UserWithID": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string"
          },
          "name": {
            "type": "string"
          },
          "email": {
            "type": "string"
          }
        },
        "required": [
          "id",
          "name",
          "email"
        ]
      },
      "ValidationError": {
        "type": "object",
        "properties": {
          "loc": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "msg": {
            "type": "string"
          },
          "type": {
            "type": "string"
          }
        },
        "required": [
          "loc",
          "msg",
          "type"
        ]
      }
    }
  }
}

"""

# --- Create OpenAPIToolset ---
generated_tools_list = []
try:
    # Instantiate the toolset with the spec string
    petstore_toolset = OpenAPIToolset(
        spec_str=openapi_spec_string,
        spec_str_type="json"
        # No authentication needed for httpbin.org
    )
    # Get all tools generated from the spec
    generated_tools_list = petstore_toolset.get_tools()
    print(f"Generated {len(generated_tools_list)} tools from OpenAPI spec:")
    for tool in generated_tools_list:
        # Tool names are snake_case versions of operationId
        print(f"- Tool Name: '{tool.name}', Description: {tool.description[:60]}...")

except ValueError as ve:
    print(f"Validation Error creating OpenAPIToolset: {ve}")
    # Handle error appropriately, maybe exit or skip agent creation
except Exception as e:
    print(f"Unexpected Error creating OpenAPIToolset: {e}")
    # Handle error appropriately

# --- Agent Definition ---
openapi_agent = Agent(
    name="OpenAPI_agent",
    model=LiteLlm(model="ollama/qwen2.5:7b", api_base="http://81.94.158.220:11434"),
    description="Manages a Pet Store using tools generated from an OpenAPI spec.",
    instruction=f"""You are a Pet Store assistant managing pets via an API.
    Use the available tools to fulfill user requests.
    Available tools: {', '.join([t.name for t in generated_tools_list])}.
    When creating a pet, confirm the details echoed back by the API.
    When listing pets, mention any filters used (like limit or status).
    When showing a pet by ID, state the ID you requested.
    """,
    tools=generated_tools_list,
)

