from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


# --- OpenAPI Tool Imports ---
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset


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
      "url": "http://81.94.155.76:8082/",
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
toolset = OpenAPIToolset(spec_str=openapi_spec_string, spec_str_type="json")
api_tools = toolset.get_tools()

# --- Agent Definition ---
root_agent = Agent(
    name="OpenAPI_agent",
    model=LiteLlm(model="ollama/qwen2.5:7b", api_base="http://81.94.155.76:11434"),
    instruction="""
            You are a Mock server OpenAPI agent that interacts with Mock server OpenAPI REST API.
            
            When working with the Mock server OpenAPI:
            - Use parameters provided by the user
            - Ask for clarification if required parameters are missing
            - Format responses clearly for the user
            - Handle errors gracefully and explain issues in simple terms
            
            For content creation operations:
            - Use names and identifiers exactly as specified by the user
            - Add helpful descriptions when allowed by the API
            - Apply sensible defaults for optional parameters when not specified
            
            Always inform the user about the actions you're taking and the results received.
            """
    tools=api_tools,
)

