### RAG-PDF


This project provides a complete Retrieval-Augmented Generation (RAG) pipeline implemented in Python, designed for extracting and analyzing data from complex PDF documents. The architecture efficiently handles various content types and uses a Large Language Model (LLM) to answer questions based strictly on the extracted context.[K.html](https://github.com/user-attachments/files/23872589/K.html)

#Key Features
Multi-Format Extraction: Supports direct extraction of Arabic and English text blocks, and structured tables using libraries like PyMuPDF and pdfplumber.

Advanced OCR Processing: Utilizes Tesseract OCR with image pre-processing techniques (Grayscale and Contrast Enhancement) to accurately read embedded images and extract text (including challenging handwritten content) from PDFs.

Integrated RAG Architecture: Builds a robust Vector Store (using FAISS) from the extracted content to enable precise semantic search and contextual retrieval.

LLM Integration: Connects with the OpenRouter API endpoint for powerful language model generation, ensuring answers are grounded in the document data.

Multilingual Support: Designed to process, categorize, and answer based on both Arabic and English content efficiently.
