"""Utility functions for the LangChain Ollama OpenAPI agent."""

import yaml
import json
import os
from typing import Dict, Any

def load_openapi_spec(file_path: str) -> Dict[str, Any]:
    """
    Load an OpenAPI specification from a file (YAML or JSON).
    
    Args:
        file_path: Path to the OpenAPI spec file
        
    Returns:
        Parsed OpenAPI spec as a dictionary
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format is unsupported
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"OpenAPI spec file not found at {file_path}")
    
    file_extension = os.path.splitext(file_path)[1].lower()
    
    with open(file_path, 'r') as file:
        if file_extension in ('.yaml', '.yml'):
            return yaml.safe_load(file)
        elif file_extension == '.json':
            return json.load(file)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}. Expected .yaml, .yml, or .json")