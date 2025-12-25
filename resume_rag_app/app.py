import streamlit as st
import os
from typing import List

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

st.set_page_config(page_title="Resume Shortlisting using RAG", layout="wide")

RESUME_DIR = "resumes"
DB_DIR = "data/chroma_db"

os.makedirs(RESUME_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"}
)

db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

llm = ChatOpenAI(
    model="meta-llama-3.1-8b-instruct",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    temperature=0.1
)


def load_full_resume_text(path: str) -> str:
    loader = PyPDFLoader(path)
    docs = loader.load()
    return "\n".join([d.page_content for d in docs])[:3000]


def score_and_justify_resume(jd: str, resume_text: str):
    prompt = f"""
You are an HR evaluator.

Return the result in this exact format:

Score: <number from 0 to 100>
Decision: Shortlist or Reject
Reason: <one short sentence>

Job Description:
{jd}

Resume:
{resume_text}
"""

    chain = PromptTemplate.from_template("{input}") | llm
    output = chain.invoke({"input": prompt}).content

    score = 0
    decision = "Reject"
    reason = ""

    for line in output.splitlines():
        if "Score" in line:
            score = int("".join(filter(str.isdigit, line)) or 0)
        elif "Decision" in line:
            decision = line.split(":", 1)[-1].strip()
        elif "Reason" in line:
            reason = line.split(":", 1)[-1].strip()

    return score, decision, reason


def delete_embeddings_for_resume(filename: str):
    db._collection.delete(where={"source": filename})
    db.persist()


def add_resume(path):
    loader = PyPDFLoader(path)
    docs = loader.load()

    for d in docs:
        d.metadata["source"] = os.path.basename(path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    parts = splitter.split_documents(docs)

    db.add_documents(parts)
    db.persist()


def delete_resume_file_and_embeddings(filename: str):
    path = os.path.join(RESUME_DIR, filename)

    if os.path.exists(path):
        os.remove(path)

    delete_embeddings_for_resume(filename)


def get_resumes():
    return [f for f in os.listdir(RESUME_DIR) if f.endswith(".pdf")]


st.sidebar.title("Resume Manager")
action = st.sidebar.radio("Action", ["Upload", "List", "Update", "Delete", "Shortlist"])


if action == "Upload":
    st.header("Upload Resumes")
    files = st.file_uploader("Upload PDF", type="pdf", accept_multiple_files=True)

    if files:
        for f in files:
            path = os.path.join(RESUME_DIR, f.name)
            with open(path, "wb") as out:
                out.write(f.read())
            add_resume(path)
        st.success("Uploaded and indexed")


elif action == "Update":
    st.header("Update Existing Resume")

    resumes = get_resumes()
    selected = st.selectbox("Select resume to update", resumes)

    new_file = st.file_uploader("Upload updated PDF", type="pdf")

    if st.button("Update") and selected and new_file:
        path = os.path.join(RESUME_DIR, selected)

        delete_embeddings_for_resume(selected)

        with open(path, "wb") as out:
            out.write(new_file.read())

        add_resume(path)

        st.success(f"{selected} updated successfully!")


elif action == "Delete":
    st.header("Delete Resume")

    resumes = get_resumes()
    selected = st.selectbox("Select resume to delete", resumes)

    if st.button("Delete") and selected:
        delete_resume_file_and_embeddings(selected)
        st.success(f"{selected} deleted successfully!")


elif action == "List":
    st.header("Stored Resumes")
    for r in get_resumes():
        st.write("•", r)


elif action == "Shortlist":
    st.header("Rank & Justify Resumes")

    jd = st.text_area("Paste Job Description")

    if st.button("Rank") and jd:
        resumes = get_resumes()

        if not resumes:
            st.warning("No resumes uploaded.")
        else:
            ranked = []

            with st.spinner("Evaluating resumes..."):
                for r in resumes:
                    path = os.path.join(RESUME_DIR, r)
                    text = load_full_resume_text(path)
                    score, decision, reason = score_and_justify_resume(jd, text)
                    ranked.append((r, score, decision, reason))

            ranked.sort(key=lambda x: x[1], reverse=True)

            st.subheader("🏆 Ranked Resumes")

            for i, (name, score, decision, reason) in enumerate(ranked, 1):
                st.markdown(f"**{i}. {name} — {score}/100 — {decision}**")
                st.caption(f"Reason: {reason}")


st.title("Resume Shortlisting using RAG")
st.caption("Grounded, private, explainable resume screening using RAG.")
