# Enterprise Document Assistant (RAG)

A modular Retrieval-Augmented Generation (RAG) application for intelligent question answering over enterprise documents. The system enables users to upload documents, indexes them into a persistent vector database, and generates context-aware responses using semantic retrieval and Large Language Models (LLMs).

---

## Overview

Enterprise Document Assistant is built using **LangChain**, **ChromaDB**, **Hugging Face Embeddings**, **Llama 3.1 8B Instruct**, and **Streamlit**. The application supports multiple document formats, performs semantic search using vector embeddings, and generates grounded responses based solely on the retrieved document context.

Unlike traditional chatbots that rely primarily on the LLM's internal knowledge, this system retrieves relevant information from uploaded documents before generating an answer, significantly reducing hallucinations and improving response reliability.

---

## Features

- **Multi-format Document Support**
  - PDF
  - DOCX
  - TXT
  - CSV

- **Semantic Retrieval**
  - Dense vector embeddings for similarity search
  - Top-K relevant document retrieval

- **Persistent Vector Database**
  - ChromaDB for efficient document storage
  - Reusable index across application sessions

- **Incremental Document Indexing**
  - Index only newly uploaded documents
  - Avoid redundant embedding generation

- **Duplicate Detection**
  - SHA-256 hash-based duplicate file detection
  - Prevents repeated indexing

- **Grounded Question Answering**
  - Responses generated only from retrieved document context
  - Prompt designed to minimize hallucinations

- **Interactive User Interface**
  - Built with Streamlit
  - Multi-file upload
  - Chat interface
  - Conversation history

- **Source Transparency**
  - Displays retrieved document chunks used for answer generation

---

## System Architecture

```
                    Enterprise Documents
        (PDF • DOCX • TXT • CSV)
                     │
                     ▼
              Document Loader
                     │
                     ▼
              Text Chunking
                     │
                     ▼
          Hugging Face Embeddings
                     │
                     ▼
             Chroma Vector Store
                     │
                     ▼
          Semantic Similarity Search
                     │
                     ▼
                Retriever
                     │
                     ▼
               Prompt Template
                     │
                     ▼
         Llama 3.1 8B Instruct
                     │
                     ▼
        AI Response + Source Citations
```

---

## Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| Framework | LangChain |
| Vector Database | ChromaDB |
| LLM | Llama 3.1 8B Instruct |
| Embeddings | Hugging Face Embeddings |
| UI | Streamlit |
| Document Processing | LangChain Document Loaders |
| Vector Search | Semantic Similarity Search |

---

## Project Structure

```
Enterprise-RAG/
│
├── embeddings/
├── loaders/
├── model/
├── prompts/
├── utils/
├── vector_store/
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Enterprise-RAG.git
cd Enterprise-RAG
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file and add your Hugging Face API token.

```text
HUGGINGFACEHUB_API_TOKEN=your_api_token
```

### Run the application

```bash
streamlit run app.py
```

---

## Usage

1. Launch the Streamlit application.
2. Upload one or more enterprise documents.
3. Click **Index Documents** to generate embeddings and store them in ChromaDB.
4. Ask questions in natural language.
5. View the generated answer along with the retrieved source documents.

---

## Current Capabilities

- Semantic document retrieval
- Retrieval-Augmented Generation (RAG)
- Persistent vector storage
- Multi-format document ingestion
- Modular software architecture
- Duplicate document detection
- Source attribution
- Context-grounded response generation



