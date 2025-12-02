def retrieve_docs(vectordb, query, k=4):
    return vectordb.similarity_search(query, k=k)
