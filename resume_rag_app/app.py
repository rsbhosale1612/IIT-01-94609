import streamlit as st
import os
from typing import List
from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

st.set_page_config(page_title="Resume Shortlisting", layout="wide")

THRESHOLD = 0.6
RESUME_DIR = "resumes"
DB_DIR = "data/chroma_db"

os.makedirs(RESUME_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)


class SimpleEmbeddings(Embeddings):
    def __init__(self, name):
        self.model = SentenceTransformer(name, device="cpu")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text: str) -> List[float]:
        return self.model.encode(text, convert_to_numpy=True).tolist()


embeddings = SimpleEmbeddings("sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)


def get_resumes():
    return [f for f in os.listdir(RESUME_DIR) if f.endswith(".pdf")]


def add_resume(path):
    loader = PyPDFLoader(path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    parts = splitter.split_documents(docs)

    db.add_documents(parts)
    db.persist()


st.sidebar.title("Resume Manager")

action = st.sidebar.radio("Action", [
    "Upload",
    "List",
    "Update",
    "Delete",
    "Shortlist"
])


if action == "Upload":
    st.header("Upload Resumes")
    files = st.file_uploader("Select PDF files", type="pdf", accept_multiple_files=True)

    if files:
        for f in files:
            path = os.path.join(RESUME_DIR, f.name)
            with open(path, "wb") as out:
                out.write(f.read())
            add_resume(path)

        st.success("Uploaded and indexed successfully")


elif action == "List":
    st.header("Stored Resumes")

    res = get_resumes()
    if res:
        for r in res:
            st.write("-", r)
    else:
        st.info("No resumes found")


elif action == "Update":
    st.header("Update Resume")

    res = get_resumes()
    name = st.selectbox("Choose resume", res)

    new_file = st.file_uploader("Upload new PDF", type="pdf")

    if st.button("Update") and name and new_file:
        path = os.path.join(RESUME_DIR, name)
        with open(path, "wb") as out:
            out.write(new_file.read())
        add_resume(path)
        st.success("Updated successfully")


elif action == "Delete":
    st.header("Delete Resume")

    res = get_resumes()
    name = st.selectbox("Choose resume", res)

    if st.button("Delete") and name:
        os.remove(os.path.join(RESUME_DIR, name))
        st.success("Deleted")


elif action == "Shortlist":
    st.header("Shortlist Resumes")

    jd = st.text_area("Paste job description")

    if st.button("Search") and jd:
        jd_words = set([w.lower() for w in jd.split() if len(w) > 2])

        results = db.similarity_search_with_score(jd, k=20)

        ranked = []

        for doc, score in results:
            text = doc.page_content.lower()
            matched = [w for w in jd_words if w in text]
            match_count = len(matched)

            if match_count > 0:
                ranked.append((doc, match_count, matched))

        ranked.sort(key=lambda x: x[1], reverse=True)

        if not ranked:
            st.warning("No matching resumes found")
        else:
            used = set()
            for i, (doc, count, matched) in enumerate(ranked, 1):
                txt = doc.page_content.strip()

                key = txt[:100]
                if key in used:
                    continue
                used.add(key)

                pct = round((count / len(jd_words)) * 100, 2)

                st.markdown(f"### Match {i} — Score: {pct}%")
                st.write(f"**Matched Fields:** {', '.join(matched[:10])}")
                st.write(txt[:800])



st.title("Resume Shortlisting using RAG")
st.caption("Use the sidebar to upload, manage and shortlist resumes.")
