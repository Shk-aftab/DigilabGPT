from fastapi import FastAPI, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import yaml
from llama_index.llms import Ollama, OpenAI
from rag.rag import RAG
from fastapi.middleware.cors import CORSMiddleware

# Load config
config_file = "config.yml"
with open(config_file, "r") as conf:
    config = yaml.safe_load(conf)

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modified Query model to match frontend expectations
class Query(BaseModel):
    text: str
    collection_name: Optional[str] = None

# Modified Response model to match frontend expectations
class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]

# Initialize RAG components
if config["llm_provider"] == "ollama":
    llm = Ollama(model=config["ollama"]["llm_name"], url=config["ollama"]["llm_url"])
elif config["llm_provider"] == "openai":
    llm = OpenAI(model=config["openai"]["llm_name"], api_key=config["openai"]["api_key"])
else:
    raise ValueError("Unsupported LLM provider specified in the configuration.")

rag = RAG(config_file=config, llm=llm)

@app.get("/")
async def root():
    return {"message": "Welcome to the Research RAG API"}

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(query: Query):
    if not query.text:
        raise HTTPException(status_code=400, detail="Query text is required.")
    
    try:
        # Use your existing query engine with the prompt
        query_engine = rag.qdrant_index().as_query_engine(
            similarity_top_k=1,
            response_mode="tree_summarize",
            verbose=True
        )
        
        response = query_engine.query(
            query.text + " You can only answer based on the provided context. If a response cannot be formed strictly using the context, politely say you don't have knowledge about that topic"
        )
        
        # Format the response to match frontend expectations
        sources = [{
            "file_path": response.metadata[k]["file_path"],
            "content": response.metadata[k].get("content", ""),
        } for k in response.metadata.keys()]
        
        return QueryResponse(
            answer=str(response).strip(),
            sources=sources
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the query: {str(e)}"
        )