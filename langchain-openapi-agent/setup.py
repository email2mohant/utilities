from setuptools import setup, find_packages

setup(
    name="langchain-ollama-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Core web framework
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.2",
        
        # LangChain packages
        "langchain>=0.0.267",
        "langchain-community>=0.0.16",
        
        # Parsing and data handling
        "pyyaml>=6.0",
        "requests>=2.28.0",
        "jsonschema>=4.17.0",
        
        # Type annotations (for Python 3.8 compatibility)
        "typing-extensions>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "langchain-ollama-api=langchain_ollama_api.main:main",
        ],
    },
    author="Mohan Krishna",
    author_email="email2mohant@gmail.com",
    description="A FastAPI service for interacting with OpenAPI specs using LangChain and Ollama",
    keywords="langchain, ollama, openapi, fastapi",
    python_requires=">=3.8",
)