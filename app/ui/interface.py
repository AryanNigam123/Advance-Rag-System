import streamlit as st
import uuid
from pathlib import Path

def render_upload_ui():
    st.title("Multi-Document RAG System")

    uploaded_files = st.file_uploader(
        "Upload one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    def is_valid_pdf(file):
        return (
            file is not None
            and file.name.lower().endswith(".pdf")
            and file.size > 0
        )

    BASE_UPLOAD_DIR = Path("data/uploads")
    BASE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    def create_session_directory():
        session_id = str(uuid.uuid4())
        session_path = BASE_UPLOAD_DIR / session_id
        session_path.mkdir(parents=True, exist_ok=True)
        return session_id, session_path

    def save_uploaded_files(files, session_path):
        saved_files = []
        for file in files:
            file_path = session_path / file.name
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            saved_files.append(file_path)
        return saved_files

    uploaded_documents = []

    if uploaded_files:
        valid_files = [f for f in uploaded_files if is_valid_pdf(f)]

        if valid_files:
            session_id, session_path = create_session_directory()
            saved_file_paths = save_uploaded_files(valid_files, session_path)

            for path in saved_file_paths:
                uploaded_documents.append({
                    "session_id": session_id,
                    "file_name": path.name,
                    "file_path": str(path)
                })

            st.success("Files uploaded successfully!")
            for doc in uploaded_documents:
                st.write(f"📄 {doc['file_name']}")

        else:
            st.warning("No valid PDF files to upload.")

    return uploaded_documents
