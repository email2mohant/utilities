"""Configuration settings for the LangChain Ollama OpenAPI agent."""

import os
from typing import Dict, Any, Optional

# Default settings
DEFAULT_MODEL = "llama3.2"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434"

# Default model parameters
DEFAULT_MODEL_PARAMS = {
    "model": DEFAULT_MODEL,
    "temperature": 0.1,
    "top_p": 0.95
}

class Settings:
    """Settings for the LangChain Ollama OpenAPI agent."""
    
    def __init__(
        self,
        openapi_spec_path: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        model_params: Optional[Dict[str, Any]] = None,
        ollama_base_url: str = DEFAULT_OLLAMA_BASE_URL,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT
    ):
        self.openapi_spec_path = openapi_spec_path
        self.model = model
        
        # Initialize model params with defaults, then update with any provided params
        self.model_params = DEFAULT_MODEL_PARAMS.copy()
        if model_params:
            self.model_params.update(model_params)
        
        # Make sure the model is set to the specified model
        self.model_params["model"] = model
        
        self.ollama_base_url = ollama_base_url
        self.host = host
        self.port = port
    
    @classmethod
    def from_env(cls):
        """Create settings from environment variables."""
        model = os.environ.get("OLLAMA_MODEL", DEFAULT_MODEL)
        
        return cls(
            openapi_spec_path=os.environ.get("OPENAPI_SPEC_PATH"),
            model=model,
            model_params={
                "temperature": float(os.environ.get("OLLAMA_TEMPERATURE", "0.1")),
                "top_p": float(os.environ.get("OLLAMA_TOP_P", "0.95")),
            },
            ollama_base_url=os.environ.get("OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASE_URL),
            host=os.environ.get("API_HOST", DEFAULT_HOST),
            port=int(os.environ.get("API_PORT", DEFAULT_PORT))
        )