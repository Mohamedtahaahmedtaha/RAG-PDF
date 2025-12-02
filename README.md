# RAG PDF


This project provides a complete Retrieval-Augmented Generation (RAG) pipeline implemented in Python, designed for extracting and analyzing data from complex PDF documents. The architecture efficiently handles various content types and uses a Large Language Model (LLM) to answer questions based strictly on the extracted context.


![licensed-image](https://github.com/user-attachments/assets/f48696ba-7055-4328-8d46-00d2ddc440ac)



## Key Features
Integrated RAG Architecture: A robust system for building a Vector Store to enable contextual retrieval and question answering.

Multi-Format Extraction: Supports direct extraction of Arabic and English text blocks, and structured tables from PDFs.

Advanced OCR Support: Utilizes Tesseract OCR with image pre-processing techniques (Grayscale & Contrast Enhancement) to improve the reading of embedded images (including challenging handwritten content).

LLM Integration: Connects to the OpenRouter API endpoint for enhanced language model generation capabilities.

PDF Generation: Includes utility to generate test PDFs containing mixed content (text, tables, and images).


## Prerequisites
Ensure the following components are installed on your system:

Python 3.9+

Git

Tesseract OCR: Must be installed as a standalone program.


## Setup and Installation
## 1. Clone and Virtual Environment
   Clone the repository
   git clone https://github.com/MohamedTahaAhmedTaha/RAG-PDF.git
   cd RAG-PDF
   
   Create and activate the virtual environment
## 2. Install Dependencies
   Install all necessary libraries (it's recommended to create a requirements.txt file, but you can use this command):
python -m venv venv
### For Windows (PowerShell):
.\venv\Scripts\activate



