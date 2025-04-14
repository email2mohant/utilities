"""LangChain agent creation and management."""

from typing import Dict, Any, Optional
import logging
from langchain_anthropic import ChatAnthropic

from langchain_community.agent_toolkits.openapi import planner
from langchain_community.llms import Ollama
from langchain_community.utilities.requests import RequestsWrapper

from .utils import load_openapi_spec
from .config import DEFAULT_MODEL_PARAMS, DEFAULT_OLLAMA_BASE_URL
from langchain_community.agent_toolkits.openapi.spec import reduce_openapi_spec

logger = logging.getLogger(__name__)

def create_agent(spec: Dict[str, Any], model: str, model_params: Optional[Dict[str, Any]] = None, 
                ollama_base_url: str = DEFAULT_OLLAMA_BASE_URL):
    """
    Create a LangChain agent for interacting with an OpenAPI spec.
    
    Args:
        spec: The OpenAPI specification as a dictionary
        model: The Ollama model to use
        model_params: Additional parameters for the Ollama model
        ollama_base_url: Base URL for the Ollama API
        
    Returns:
        A LangChain agent configured to use the provided spec
    """
    # Set up model parameters
    params = model_params or DEFAULT_MODEL_PARAMS.copy()
    params["model"] = model
    
    # Initialize the LLM
    llm = Ollama(base_url=ollama_base_url, **params)
    
    # Initialize the toolkit with the spec
    requests_wrapper = RequestsWrapper()
    
    
    # Create and return the agent
    return planner.create_openapi_agent(
    reduce_openapi_spec(spec),
    requests_wrapper,
    llm,
    allow_dangerous_requests=True)
   

class AgentManager:
    """
    Manages LangChain OpenAPI agents.
    
    This class handles the loading of OpenAPI specs and creation of agents.
    """
    
    def __init__(self, spec_path: Optional[str] = None, model: str = DEFAULT_MODEL_PARAMS["model"],
                 ollama_base_url: str = DEFAULT_OLLAMA_BASE_URL):
        """
        Initialize the agent manager.
        
        Args:
            spec_path: Path to the OpenAPI spec file (optional)
            model: The Ollama model to use
            ollama_base_url: Base URL for the Ollama API
        """
        self.spec = None
        self.agent = None
        self.model = model
        self.ollama_base_url = ollama_base_url
        
        if spec_path:
            self.load_spec(spec_path)
    
    def load_spec(self, spec_path: str) -> bool:
        """
        Load an OpenAPI spec from a file.
        
        Args:
            spec_path: Path to the OpenAPI spec file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.spec = load_openapi_spec(spec_path)
            logger.info(f"Successfully loaded OpenAPI spec from {spec_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load OpenAPI spec: {str(e)}")
            return False
    
    def initialize_agent(self, model_params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Initialize the LangChain agent with the loaded spec.
        
        Args:
            model_params: Parameters for the Ollama model
            
        Returns:
            True if successful, False otherwise
        """
        if not self.spec:
            logger.error("Cannot initialize agent: No OpenAPI spec loaded")
            return False
        
        try:
            self.agent = create_agent(
                self.spec, 
                self.model, 
                model_params, 
                self.ollama_base_url
            )
            logger.info(f"Successfully initialized agent with model {self.model}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize agent: {str(e)}",exc_info=True)
            return False
    
    def run_query(self, query: str, model_params: Optional[Dict[str, Any]] = None, 
                 override_model: Optional[str] = None) -> str:
        """
        Run a query using the agent.
        
        Args:
            query: The query to run
            model_params: Optional parameters to override the default model parameters
            override_model: Optional model to use instead of the default
            
        Returns:
            The result of the query
            
        Raises:
            ValueError: If the agent is not initialized
        """
        if not self.agent:
            raise ValueError("Agent not initialized")
        
        if model_params or override_model:
            # Create a temporary agent with the new parameters
            model_to_use = override_model or self.model
            temp_agent = create_agent(
                self.spec, 
                model_to_use, 
                model_params, 
                self.ollama_base_url
            )
            return temp_agent.run(query)
        
        return self.agent.run(query)