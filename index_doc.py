# stores indexing of each document
# Run this whenever new documents are added or existing documents are updated.

import os

from config import UPLOAD_FOLDER
from loaders.loader_factory import LoaderFactory
from preprocessing.splitter import TextSplitter
from embeddings.embedding_model import EmbeddingModel
from vector_store.chroma_db import ChromaVectorStore


def index_documents(file_paths):
    """
    Runs the complete indexing pipeline.

    Phase 1 : Document Ingestion
    Phase 2 : Text Splitting
    Phase 3 : Embedding Model Initialization
    Phase 4 : Vector Database Creation
    """

    # ==========================================================
    # PHASE 1 : DOCUMENT INGESTION
    # ==========================================================

    all_documents = []

    for file_path in file_paths:

        loader = LoaderFactory.get_loader(file_path)

        docs = loader.load(file_path)

        all_documents.extend(docs)

    print(f"Loaded {len(all_documents)} documents")

    # ==========================================================
    # PHASE 2 : TEXT SPLITTING
    # ==========================================================

    splitter = TextSplitter()

    chunked_documents = splitter.split_documents(all_documents)

    print(f"Created {len(chunked_documents)} chunks")

    # ==========================================================
    # PHASE 3 : EMBEDDING MODEL INITIALIZATION
    # ==========================================================

    embedding_model = EmbeddingModel().get_model()

    # ==========================================================
    # PHASE 4 : VECTOR DATABASE CREATION
    # ==========================================================

    vector_store = ChromaVectorStore(embedding_model)

    vector_store.add_documents(chunked_documents)

    print("New documents indexed successfully.")
