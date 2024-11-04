# DigilabGPT: Assistance for Digilab Employees

This project aims to help LSBG employees by providing a powerful assistant powered by a customized RAG (Retrieval-Augmented Generation) pipeline.

## Setting Up the Environment

### Creating a Conda Environment

To create a Conda environment with DigilabGPT using Python version 3.12.0, follow these steps:

1. Create the Conda environment:
   ```bash
   conda create -n digilabgpt python=3.12.0
   ```

2. Activate the environment:
   ```bash
   conda activate digilabgpt
   ```

3. Install the required packages from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

### Starting a Qdrant Docker Instance

To start a Qdrant instance, run the following command:

```bash
docker run -p 6333:6333 -v ~/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

### Downloading & Indexing Data

To download and index the data, execute:
```bash
python rag/data.py --ingest
```

## LLM Serving Options

You have two options for serving the LLM:

### Online LLM Serving

1. Add your OpenAI API keys to `config.py`.

### Offline LLM Serving

1. Follow [this article](https://otmaneboughaba.com/posts/local-llm-ollama-huggingface/) for instructions on running models from Hugging Face locally with Ollama.

2. Create the model from the Modelfile:
   ```bash
   ollama create digilab_assistant -f ollama/Modelfile 
   ```

3. Start the model server:
   ```bash
   ollama run digilab_assistant
   ```

   By default, Ollama runs on `http://localhost:11434`.

## Starting the FastAPI Server

To start the FastAPI server, run:
```bash
uvicorn app:app --reload
```

## Testing the API

If you just want to test the API, navigate to `http://localhost:8000/docs` in your web browser to access the interactive API documentation.