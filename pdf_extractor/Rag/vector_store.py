from langchain_community.vectorstores import FAISS

def build_vector_store(chunks, embedder):
    """Build FAISS vector store from text chunks and embeddings"""
    return FAISS.from_texts(chunks, embedder)
