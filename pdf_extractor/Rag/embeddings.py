from openai import OpenAI
from typing import List
from langchain_core.embeddings import Embeddings 
from dotenv import load_dotenv
import os

load_dotenv() 

api_key = os.environ.get("OPENROUTER_API_KEY")

if api_key:
    print("API Key loaded successfully!")
else:
    print("Error: API Key not found in environment.")

class OpenRouterEmbeddings(Embeddings): 
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    # The functions must adhere to a unified signature (consistent input/output parameters).
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
       Converts a list of text inputs/chunks into **Embeddings** (numerical vector representations). 
       This function is typically executed during the initial **Vector Store construction**
    (database building) to enable efficient semantic search for Retrieval-Augmented Generation (RAG).
        """
        texts = [t.replace("\n", " ") for t in texts]
        
        response = self.client.embeddings.create(
            model="text-embedding-3-small", 
            input=texts
        )
        return [item.embedding for item in response.data]

    def embed_query(self, text: str) -> List[float]:
        """
        Converts a single input query (question) into an **Embedding** (numerical vector). 
        This process is essential during the **retrieval/search phase** to find relevant information in the vector store.
        """
        # It invokes the same underlying text embedding function (as typically expected by LangChain).
        embeddings = self.embed_documents([text])
        return embeddings[0]