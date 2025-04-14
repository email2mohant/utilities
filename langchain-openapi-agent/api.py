"""FastAPI server for the LangChain Ollama OpenAPI agent."""

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import uvicorn

from .agent import AgentManager
from .config import Settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define request/response models
class QueryRequest(BaseModel):
    query: str
    model_params: Optional[Dict[str, Any]] = None
    model: Optional[str] = None

class QueryResponse(BaseModel):
    result: str

def create_app(settings: Optional[Settings] = None) -> FastAPI:
    """
    Create a FastAPI application for the LangChain Ollama OpenAPI agent.
    
    Args:
        settings: Configuration settings
        
    Returns:
        A configured FastAPI application
    """
    # Use provided settings or create default ones
    if settings is None:
        settings = Settings.from_env()
    
    # Initialize FastAPI app
    app = FastAPI(
        title="LangChain OpenAPI Agent API", 
        description="API for interacting with OpenAPI specifications using LangChain and Ollama"
    )
    
    # Initialize the agent manager
    agent_manager = AgentManager(
        model=settings.model,
        ollama_base_url=settings.ollama_base_url
    )
    
    # Define startup event
    @app.on_event("startup")
    async def startup_event():
        """Initialize the agent during startup."""
        if settings.openapi_spec_path:
            if agent_manager.load_spec(settings.openapi_spec_path):
                agent_manager.initialize_agent(settings.model_params)
    
    # Define query endpoint
    @app.post("/query", response_model=QueryResponse)
    async def query_agent(request: QueryRequest = Body(...)):
        """
        Run a query using the agent.
        
        Args:
            request: The query request
            
        Returns:
            The query response
            
        Raises:
            HTTPException: If an error occurs
        """
        if not agent_manager.agent:
            raise HTTPException(
                status_code=503,
                detail="Agent not initialized. Check server logs for details."
            )
        
        try:
            result = agent_manager.run_query(
                request.query, 
                request.model_params, 
                request.model
            )
            return QueryResponse(result=result)
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing request: {str(e)}"
            )
    
    # Define health check endpoint
    @app.get("/health")
    async def health_check():
        """Check the health of the service."""
        return {
            "status": "healthy",
            "agent_initialized": agent_manager.agent is not None,
            "model": agent_manager.model
        }
    
    return app

def run_server(settings: Optional[Settings] = None):
    """
    Run the FastAPI server.
    
    Args:
        settings: Configuration settings
    """
    if settings is None:
        settings = Settings.from_env()
    
    app = create_app(settings)
    uvicorn.run(app, host=settings.host, port=settings.port)