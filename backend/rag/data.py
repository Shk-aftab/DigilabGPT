from llama_index import (
    ServiceContext,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.vector_stores.qdrant import QdrantVectorStore
from tqdm import tqdm
import os
import argparse
import yaml
import qdrant_client
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.embeddings import LangchainEmbedding
from llama_index.llms import Ollama, OpenAI

class Data:
    def __init__(self, config):
        self.config = config

    def _create_data_folder(self, download_path):
        data_path = download_path
        if not os.path.exists(data_path):
            os.makedirs(self.config["data_path"])
            print("Output folder created")
        else:
            print("Output folder already exists.")

    def ingest(self, embedder):
        print("Indexing data...")
        documents = SimpleDirectoryReader(self.config["data_path"]).load_data()

        client = qdrant_client.QdrantClient(url=self.config["qdrant_url"])
        qdrant_vector_store = QdrantVectorStore(
            client=client, collection_name=self.config["collection_name"]
        )
        storage_context = StorageContext.from_defaults(vector_store=qdrant_vector_store)

        # Initialize the LLM based on the provider
        if self.config["llm_provider"] == "ollama":
            llm = Ollama(model=self.config["ollama"]["llm_name"], url=self.config["ollama"]["llm_url"])
        elif self.config["llm_provider"] == "openai":
            llm = OpenAI(model=self.config["openai"]["llm_name"], api_key=self.config["openai"]["api_key"])
        else:
            raise ValueError("Unsupported LLM provider specified in the configuration.")

        service_context = ServiceContext.from_defaults(
            llm=llm, embed_model=embedder, chunk_size=self.config["chunk_size"]
        )

        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, service_context=service_context
        )
        print(
            f"Data indexed successfully to Qdrant. Collection: {self.config['collection_name']}"
        )
        return index

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--ingest",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Ingest data to Qdrant vector Database.",
    )

    args = parser.parse_args()
    config_file = "config.yml"
    with open(config_file, "r") as conf:
        config = yaml.safe_load(conf)
    data = Data(config)

    if args.ingest:
        print("Loading Embedder...")
        embed_model = LangchainEmbedding(
            HuggingFaceEmbeddings(model_name=config["embedding_model"])
        )
        data.ingest(embedder=embed_model)
