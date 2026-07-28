import os
import shutil
import streamlit as st

from embeddings.embedding_model import EmbeddingModel
from vector_store.retriever import Retriever
from model.chat_model import ChatModel
from prompts.rag_prompt import rag_prompt

from langchain_core.output_parsers import StrOutputParser

from index_doc import index_documents
from config import UPLOAD_FOLDER

from utils.file_hash import get_file_hash
from utils.index_tracker import (
    load_indexed_files,
    save_indexed_files
)

# Folder where uploaded documents will be stored.
# These files will later be indexed into the vector database.

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================
# Configure the Streamlit application.
# This is executed once when the app starts.

st.set_page_config(
    page_title="Enterprise RAG",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Enterprise Document Assistant")

# ==========================================================
# SIDEBAR : DOCUMENT UPLOAD & INDEXING
# ==========================================================
# Allows users to upload enterprise documents.
# When "Index Documents" is clicked:
#   1. Save uploaded files locally.
#   2. Run the indexing pipeline.
#      (Load → Split → Embed → Store in ChromaDB)

st.sidebar.header("Upload Documents")

uploaded_files = st.sidebar.file_uploader(
    "Choose PDF/DOCX/TXT/CSV files",
    type=["pdf", "docx", "txt", "csv"],
    accept_multiple_files=True
)

if st.sidebar.button("Index Documents"):

    if uploaded_files:

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Files that actually need indexing
        saved_files = []

        # Existing indexed hashes
        indexed_files = load_indexed_files()

        # Store only hashes of successfully indexed files
        new_hashes = {}

        # --------------------------------------------------
        # Save uploaded files and check duplicates
        # --------------------------------------------------

        for uploaded_file in uploaded_files:

            save_path = os.path.join(
                UPLOAD_FOLDER,
                uploaded_file.name
            )

            # Save uploaded file
            with open(save_path, "wb") as f:
                shutil.copyfileobj(uploaded_file, f)

            # Generate SHA-256 hash
            file_hash = get_file_hash(save_path)

            # Skip duplicate documents
            if file_hash in indexed_files:

                st.sidebar.warning(
                    f"{uploaded_file.name} is already indexed."
                )

                continue

            # Queue file for indexing
            saved_files.append(save_path)

            # Store hash temporarily
            new_hashes[file_hash] = {
                "filename": uploaded_file.name
            }

        # --------------------------------------------------
        # Index new documents
        # --------------------------------------------------

        if saved_files:

            try:

                with st.spinner("Indexing documents..."):

                    index_documents(saved_files)

                # Update JSON only after successful indexing
                indexed_files.update(new_hashes)

                save_indexed_files(indexed_files)

                st.sidebar.success(
                    f"{len(saved_files)} new document(s) indexed successfully!"
                )

            except Exception as e:

                st.sidebar.error(
                    f"Indexing failed.\n{str(e)}"
                )

        else:

            st.sidebar.info(
                "No new documents to index."
            )
# ==========================================================
# LOAD RAG COMPONENTS
# ==========================================================
# Initialize all components required for question answering.
#
# Embedding Model
#      ↓
# Retriever
#      ↓
# Chat Model
#      ↓
# LCEL Chain (Prompt → Model → Output Parser)

embedding_model = EmbeddingModel().get_model()

retriever = Retriever(embedding_model)

chat_model = ChatModel().get_model()

# Create the complete LangChain pipeline using LCEL.
# User Input
#      ↓
# Chat Prompt
#      ↓
# Chat Model
#      ↓
# String Output

chain = (
    rag_prompt
    | chat_model
    | StrOutputParser()
)

# ==========================================================
# CHAT HISTORY
# ==========================================================
# Store conversation history inside Streamlit session state.
# This prevents previous messages from disappearing every time
# the page refreshes.

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation.

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# USER QUESTION
# ==========================================================
# Accept a natural language question from the user.
# This acts as the entry point of the RAG pipeline.

query = st.chat_input("Ask a question about your documents")

if query:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(query)

    # ======================================================
    # PHASE 5 : RETRIEVAL
    # ======================================================
    # Convert the user's question into an embedding.
    # Perform semantic similarity search.
    # Retrieve the Top-K most relevant chunks.

    with st.spinner("Searching documents..."):

        results = retriever.retrieve(query, k=3)

        # ==================================================
        # PHASE 6 : PROMPT ENGINEERING
        # ==================================================
        # Combine retrieved chunks into a single context.
        # This context is inserted into the ChatPromptTemplate.

        context = "\n\n".join(
            [doc.page_content for doc in results]
        )

        # ==================================================
        # PHASE 7 : GENERATION
        # ==================================================
        # Execute the LCEL chain.
        #
        # Context + Question
        #        ↓
        # ChatPromptTemplate
        #        ↓
        # Chat Model
        #        ↓
        # StrOutputParser
        #        ↓
        # Final Answer

        answer = chain.invoke(
            {
                "context": context,
                "question": query
            }
        )

    # ======================================================
    # DISPLAY AI RESPONSE
    # ======================================================
    # Show the generated answer to the user.

    with st.chat_message("assistant"):

        st.markdown(answer)

        # ==================================================
        # SOURCE CITATIONS
        # ==================================================
        # Display the retrieved document chunks that were
        # used by the LLM while generating the answer.
        # This improves transparency and helps users verify
        # where the information came from.

        with st.expander("Sources"):

            for i, doc in enumerate(results):

                st.markdown(f"### Source {i+1}")

                st.write(
                    f"**File:** {doc.metadata['source']}"
                )

                st.write(
                    f"**Page:** {doc.metadata.get('page')}"
                )

                st.write(doc.page_content)

                st.divider()

    # Save assistant response for future interactions.

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )