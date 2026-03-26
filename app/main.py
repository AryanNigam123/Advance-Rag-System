import sys
from pathlib import Path

# --------------------------------------------------
# Fix Python path
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# --------------------------------------------------
# Imports
# --------------------------------------------------
import streamlit as st
from app.ui.interface import render_upload_ui
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.parser import extract_text_by_page
from app.ingestion.metadata import attach_metadata
from app.preprocessing.cleaner import clean_text
from app.preprocessing.chunker import chunk_text
from app.embeddings.embedder import EmbeddingGenerator
from app.vectorstore.faiss_store import FAISSVectorStore
from app.vectorstore.retriever import SemanticRetriever
from app.llm.prompt import build_prompt
from app.llm.generator import AnswerGenerator


# --------------------------------------------------
# Session state initialization (CRITICAL)
# --------------------------------------------------
if "embedded_chunks" not in st.session_state:
    st.session_state.embedded_chunks = []

# --------------------------------------------------
# Phase 3: Ingestion function
# --------------------------------------------------
def ingest_single_pdf(file_info: dict):
    doc = load_pdf(file_info["file_path"])
    pages = extract_text_by_page(doc)

    return attach_metadata(
        pages=pages,
        session_id=file_info["session_id"],
        source_pdf=file_info["file_name"]
    )

# --------------------------------------------------
# Phase 2: Render UI
# --------------------------------------------------
uploaded_documents = render_upload_ui()

# --------------------------------------------------
# Initialize pipeline variables
# --------------------------------------------------
all_pages = []
all_chunks = []

# --------------------------------------------------
# Phase 3: PDF ingestion
# --------------------------------------------------
if uploaded_documents:
    for file_info in uploaded_documents:
        all_pages.extend(ingest_single_pdf(file_info))

    st.divider()
    st.write("### Uploaded Documents")
    st.write("Total pages extracted:", len(all_pages))
    st.json(all_pages[0])

# --------------------------------------------------
# Phase 4: Cleaning & Chunking
# --------------------------------------------------
if all_pages:
    for page in all_pages:
        page["text"] = clean_text(page["text"])
        all_chunks.extend(chunk_text(page))

    st.divider()
    st.write("### Chunked Documents")
    st.write("Total chunks created:", len(all_chunks))
    st.json(all_chunks[0])

# --------------------------------------------------
# Phase 5: Embedding Generation
# --------------------------------------------------
if all_chunks:
    with st.spinner("Generating embeddings (first run may take a minute)..."):
        embedder = EmbeddingGenerator()
        st.session_state.embedded_chunks = embedder.embed_chunks(all_chunks)

    st.divider()
    st.write("### Embedded Documents")
    st.write(
        "Total embeddings created:",
        len(st.session_state.embedded_chunks)
    )
    st.write(
        "Embedding vector shape:",
        st.session_state.embedded_chunks[0]["embedding"].shape
    )
    st.json(st.session_state.embedded_chunks[0]["metadata"])

# --------------------------------------------------
# Phase 6: FAISS Vector Store & Semantic Retrieval
# --------------------------------------------------
if st.session_state.embedded_chunks:
    vector_dim = st.session_state.embedded_chunks[0]["embedding"].shape[0]

    vector_store = FAISSVectorStore(vector_dim)
    vector_store.add_embeddings(st.session_state.embedded_chunks)

    st.divider()
    st.write("### Vector Store")
    st.write("Total vectors indexed:", vector_store.index.ntotal)

    query = st.text_input("Ask a question about the document")

    if query:
        retriever = SemanticRetriever(vector_store, top_k=3)
        results = retriever.retrieve(query)

        st.write("### Retrieved Chunks")
        for res in results:
            st.write(
                f"📄 {res['metadata']['source_pdf']} | "
                f"Page {res['metadata']['page_number']}"
            )

       # ---------------- PHASE 7 ----------------
        prompt = build_prompt(query, results)

        with st.spinner("Generating answer using LLaMA 3.1..."):
            generator = AnswerGenerator()
            answer = generator.generate(prompt)

        st.divider()
        st.write("### Final Answer")
        st.write(answer)

# -------------------------------
# Source Attribution
# -------------------------------
        sources = set()

        for chunk in results:
            pdf_name = chunk["metadata"]["source_pdf"]
            page_number = chunk["metadata"]["page_number"]
            sources.add((pdf_name, page_number))

        st.write("### Sources")
        for pdf, page in sources:
            st.write(f"- 📄 {pdf} (Page {page})")