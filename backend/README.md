# RAG: Research-assistant

This project aims to help LSBG employee

## Running the project

#### Starting a Qdrant docker instance

```bash
docker run -p 6333:6333 -v ~/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

#### Downloading & Indexing data

```bash
python rag/data.py --ingest
```

#### Starting Ollama LLM server (optional, just provide openai api keys in config.py for online serving)

Follow [this article](https://otmaneboughaba.com/posts/local-llm-ollama-huggingface/) for more infos on how to run models from hugging face locally with Ollama.

Create model from Modelfile

```bash
ollama create digilab_assistant -f ollama/Modelfile 
```

Start the model server

```bash
ollama run digilab_assistant
```

By default, Ollama runs on ```http://localhost:11434```

#### Starting the api server

```bash
uvicorn app:app --reload
```
