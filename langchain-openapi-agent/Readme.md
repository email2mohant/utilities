# LangChain Ollama OpenAPI Agent

A Python module that provides a FastAPI service for interacting with OpenAPI specifications using LangChain and Ollama's LLM models.

## Features

- 🚀 Expose OpenAPI specifications as conversational AI interfaces
- 🔄 Support for both YAML and JSON OpenAPI specifications
- 🧠 Powered by Ollama LLMs like llama3.2
- 🛠️ Configurable through environment variables, command line, or code
- 🧩 Modular design for easy extension and integration
- 🔌 REST API for integration with other services

## Installation

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed and running
- The desired Ollama model pulled (e.g., `ollama pull llama3.2`)

### Install from source

```bash
# Clone the repository
git clone https://github.com/yourusername/langchain-ollama-api.git
cd langchain-ollama-api

# Install in development mode
pip install -e .
```

## Quick Start

### Command Line Interface

The simplest way to use this module is through the command line interface:

```bash
# Start the server with an OpenAPI specification
langchain-ollama-api --spec path/to/your/openapi.yml --model llama3.2
```

This will start a FastAPI server at http://localhost:8000.

### Using in Python Code

```python
from langchain_ollama_api import create_app, AgentManager
from langchain_ollama_api.config import Settings

# Create a custom settings object
settings = Settings(
    openapi_spec_path="path/to/your/openapi.yml",
    model="llama3.2",
    model_params={"temperature": 0.2}
)

# Create a FastAPI app with these settings
app = create_app(settings)

# Or use the agent manager directly
manager = AgentManager("path/to/your/openapi.yml", model="llama3.2")
manager.initialize_agent()
result = manager.run_query("Find available pets")
```

## Configuration

### Command Line Options

| Option          | Description                                           | Default                  |
| --------------- | ----------------------------------------------------- | ------------------------ |
| `--spec`        | Path to the OpenAPI specification file (YAML or JSON) | _Required_               |
| `--model`       | Ollama model to use                                   | `llama3.2`               |
| `--temperature` | Model temperature                                     | `0.1`                    |
| `--top-p`       | Model top_p value                                     | `0.95`                   |
| `--ollama-url`  | Ollama API base URL                                   | `http://localhost:11434` |
| `--host`        | Host to bind to                                       | `0.0.0.0`                |
| `--port`        | Port to listen on                                     | `8000`                   |

### Environment Variables

| Variable             | Description                            | Default                  |
| -------------------- | -------------------------------------- | ------------------------ |
| `OPENAPI_SPEC_PATH`  | Path to the OpenAPI specification file | None                     |
| `OLLAMA_MODEL`       | Ollama model to use                    | `llama3.2`               |
| `OLLAMA_TEMPERATURE` | Model temperature                      | `0.1`                    |
| `OLLAMA_TOP_P`       | Model top_p value                      | `0.95`                   |
| `OLLAMA_BASE_URL`    | Ollama API base URL                    | `http://localhost:11434` |
| `API_HOST`           | Host to bind to                        | `0.0.0.0`                |
| `API_PORT`           | Port to listen on                      | `8000`                   |

## API Reference

### Endpoints

#### POST /query

Run a query using the agent.

Request body:

```json
{
  "query": "Find available pets with status available",
  "model_params": {
    "temperature": 0.2,
    "top_p": 0.9
  },
  "model": "llama3.2"
}
```

Response:

```json
{
  "result": "I found 3 pets with 'available' status: Fido (dog), Whiskers (cat), and Rex (dog)."
}
```

#### GET /health

Check the health of the service.

Response:

```json
{
  "status": "healthy",
  "agent_initialized": true,
  "model": "llama3.2"
}
```

## Example Uses

### Querying a Pet Store API

```bash
# Start the server with the Pet Store API spec
langchain-ollama-api --spec petstore.yml --model llama3.2

# Send a query
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find pets with status available"
  }'
```

### Using Different Models for Different Queries

```bash
# Start with llama3.2 as the default model
langchain-ollama-api --spec myapi.yml --model llama3.2

# Use a different model for a specific query
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find complex data patterns in the results",
    "model": "mistral"
  }'
```

## Module Structure

```
langchain_ollama_api/
├── __init__.py     # Package exports
├── agent.py        # Agent creation and management
├── api.py          # FastAPI server
├── config.py       # Configuration settings
└── utils.py        # Utility functions
```

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/langchain-ollama-api.git
cd langchain-ollama-api

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Running Tests

```bash
pytest
```

## Troubleshooting

### Common Issues

1. **"Agent not initialized" error**

   - Make sure the OpenAPI spec file exists and is valid
   - Check the server logs for detailed error messages

2. **Connection errors to Ollama**

   - Ensure Ollama is running: `ollama serve`
   - Verify you've pulled the model: `ollama pull llama3.2`
   - Check if the URL is correct with `--ollama-url`

3. **Slow or timeout responses**
   - Some queries may be complex and take longer to process
   - Try a smaller/faster model or adjust the model parameters

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
