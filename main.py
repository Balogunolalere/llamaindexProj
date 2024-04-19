# Python
import os
import re
import subprocess
import time
import nest_asyncio

from dotenv import load_dotenv
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from chromadb.config import Settings as ChromaSettings

# Apply nest_asyncio to enable asynchronous I/O operations
nest_asyncio.apply()

# Load environment variables
load_dotenv()

# Set up API keys
cohere_api_key = os.getenv("COHERE_API_KEY")
llm_api_key = os.getenv("GROQ_API_KEY")

# Set up settings
Settings.embed_model = CohereEmbedding(cohere_api_key=cohere_api_key)
Settings.llm = Groq(model="mixtral-8x7b-32768", api_key=llm_api_key)

# Utility functions
def parse_github_url(url):
    """Parse GitHub URL to extract owner and repo."""
    pattern = r"https://github\.com/([^/]+)/([^/]+)"
    match = re.match(pattern, url)
    return match.groups() if match else (None, None)

def clone_github_repo(repo_url):
    """Clone GitHub repository."""
    print('Cloning the repo ...')
    try:
        subprocess.run(["git", "clone", repo_url], check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository: {e}")
        return None

def validate_owner_repo(owner, repo):
    """Validate owner and repo."""
    return bool(owner) and bool(repo)

def setup_query_engine(github_url):
    """Set up query engine."""
    owner, repo = parse_github_url(github_url)
    
    if not validate_owner_repo(owner, repo):
        print('Invalid github repo, try again!')
        return None

    # Clone the GitHub repo & save it in a directory
    input_dir_path = f"{repo}"
    if not os.path.exists(input_dir_path):
        clone_github_repo(github_url)

    loader = SimpleDirectoryReader(input_dir_path, recursive=True)
    try:
        docs = loader.load_data()
        if not docs:
            print("No data found, check if the repository is not empty!")
            return None

        # Create vector store and upload data
        client = chromadb.PersistentClient(path="./db")
        chroma_collection = client.get_or_create_collection(repo)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(docs, storage_context=storage_context, show_progress=True)
        query_engine = index.as_query_engine(similarity_top_k=3)

        print("Data loaded successfully!!")
        print("Ready to chat!!")
        return query_engine

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Main function
def main():
    github_url = input("\033[36mEnter the GitHub URL of the repository you want to chat with: \033[0m")
    query_engine = setup_query_engine(github_url=github_url)

    while True:
        question = input("\033[35mEnter your question (or 'quit' to stop):\033[0m ")
        if question.lower() == 'quit':
            break
        start_time = time.time()
        response = query_engine.query(question)
        end_time = time.time()
        print("\033[32m" + str(response) + "\033[0m")
        print(f"\033[33mQuery took {end_time - start_time:.2f} seconds\033[0m")

if __name__ == "__main__":
    main()