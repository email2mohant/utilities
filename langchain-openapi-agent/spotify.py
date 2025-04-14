import os
import yaml
from langchain_community.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain_community.agent_toolkits.openapi import planner
from langchain_community.llms import Ollama

os.environ['SPOTIPY_CLIENT_ID']="de670fc0fcd9494abefe2139a8cfc7c0"
os.environ['SPOTIPY_CLIENT_SECRET']="c58b41205e094a8d871d9eb4ac8a2454"
os.environ["SPOTIPY_REDIRECT_URI"]="http://127.0.0.1:8080/callback"
ALLOW_DANGEROUS_REQUEST = True



with open("apispec/spotify-openapi.yml") as f:
    raw_spotify_api_spec = yaml.load(f, Loader=yaml.Loader)
spotify_api_spec = reduce_openapi_spec(raw_spotify_api_spec)

import spotipy.util as util
from langchain_community.utilities.requests import RequestsWrapper


def construct_spotify_auth_headers(raw_spec: dict):
    scopes = list(
        raw_spec["components"]["securitySchemes"]["oauth_2_0"]["flows"][
            "authorizationCode"
        ]["scopes"].keys()
    )
    access_token = util.prompt_for_user_token(scope=",".join(scopes))
    return {"Authorization": f"Bearer {access_token}"}


# Get API credentials.
headers = construct_spotify_auth_headers(raw_spotify_api_spec)
print(headers)
requests_wrapper = RequestsWrapper(headers=headers)
endpoints = [
    (route, operation)
    for route, operations in raw_spotify_api_spec["paths"].items()
    for operation in operations
    if operation in ["get", "post"]
]

llm = Ollama(model="llama3.1")

print(len(endpoints))
spotify_agent = planner.create_openapi_agent(
    spotify_api_spec,
    requests_wrapper,
    llm,
    allow_dangerous_requests=ALLOW_DANGEROUS_REQUEST,
    
)
user_query = (
    "Get my audio books"
)
spotify_agent.invoke(user_query)