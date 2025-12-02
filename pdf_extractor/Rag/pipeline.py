from .embeddings import OpenRouterEmbeddings as get_embedder
from .vector_store import build_vector_store
from .retriever import retrieve_docs
from .chunker import chunk_text
from pdf_extractor.llm_api import ask_llm
from pdf_extractor.extractor import PDFExtractor

def build_rag(pdf_path: str):
    print("Extracting PDF content...")
    extractor = PDFExtractor(pdf_path)
    data = extractor.extract_all()

    ocr_list = data.get("ocr", [])
    ocr_text = "\n".join(ocr_list) if isinstance(ocr_list, list) else str(ocr_list or "")

    combined = (
        "\n".join(data.get("text", {}).get("english", []))
        + "\n"
        + "\n".join(data.get("text", {}).get("arabic", []))
        + "\n"
        + ("\n".join([format_table_as_text(t) for t in data.get("tables", [])]) if data.get("tables") else "")
        + "\n"
        + ocr_text
    )

    print(f"Combined text length: {len(combined)} characters")

    print("Chunking text...")
    chunks = chunk_text(combined)
    print(f"Total chunks created: {len(chunks)}")

    print("Building vector store...")
    embedder = get_embedder()
    vectordb = build_vector_store(chunks, embedder)
    print("Vector store ready")

    def ask(query: str):
        docs = retrieve_docs(vectordb, query)
        print(f"Retrieved {len(docs)} docs for query: {query}")

        context = "\n".join([d.page_content for d in docs])
        if not context.strip():
            print("Context empty, using first 500 chars of combined text")
            context = combined[:500]

        #Specific prompt
        prompt = f"""
            You are a data extraction assistant. Your task is to answer the user's question 
            **based strictly on the provided context only.**

            **Important Instructions:**
            1.  Answer in **Arabic**.
            2.  When extracting information from the context, 
            **you must include all retrieved text relevant to the question, 
            including English text (whether it is standard text or text extracted via OCR)**.
            Context:\n{context}\n\nQuestion: {query}\nAnswer:
            """
        return ask_llm(prompt)

    return ask

def format_table_as_text(table_records):
    lines = []
    for row in table_records:
        if isinstance(row, dict):
            pair_texts = [f"{k}: {v}" for k, v in row.items()]
            lines.append(", ".join(pair_texts))
        else:
            lines.append(str(row))
    return "\n".join(lines)
