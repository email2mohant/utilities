#!/usr/bin/env python3
"""
Main script to run the LangChain Ollama OpenAPI agent server.
"""

import argparse
import sys
import os

from langchain_ollama_api import run_server
from langchain_ollama_api.config import Settings

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Start the LangChain Ollama OpenAPI agent server"
    )
    parser.add_argument(
        "--spec", 
        help="Path to the OpenAPI specification file (YAML or JSON)",
        required=True
    )
    parser.add_argument(
        "--model", 
        default="llama3.2",
        help="Ollama model to use (default: llama3.2)"
    )
    parser.add_argument(
        "--temperature", 
        type=float, 
        default=0.1,
        help="Model temperature (default: 0.1)"
    )
    parser.add_argument(
        "--top-p", 
        type=float, 
        default=0.95,
        help="Model top_p (default: 0.95)"
    )
    parser.add_argument(
        "--ollama-url",
        default="http://localhost:11434",
        help="Ollama API base URL (default: http://localhost:11434)"
    )
    parser.add_argument(
        "--host", 
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port to listen on (default: 8000)"
    )
    
    return parser.parse_args()

def main():
    """Main entry point."""
    args = parse_args()
    
    # Validate the spec file
    if not os.path.exists(args.spec):
        print(f"Error: OpenAPI spec file not found at {args.spec}", file=sys.stderr)
        return 1
    
    # Create settings
    settings = Settings(
        openapi_spec_path=args.spec,
        model=args.model,
        model_params={
            "temperature": args.temperature,
            "top_p": args.top_p
        },
        ollama_base_url=args.ollama_url,
        host=args.host,
        port=args.port
    )
    
    # Run the server
    print(f"Starting server with OpenAPI spec: {args.spec}")
    print(f"Using Ollama model: {args.model} (temperature={args.temperature}, top_p={args.top_p})")
    print(f"Ollama base URL: {args.ollama_url}")
    run_server(settings)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())