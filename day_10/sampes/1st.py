from langchain_text_splitters import RecursiveCharacterTextSplitter

code_text = """
The Sunbeam website mentions industry-oriented training, placements, 
and admission schedules across different pages. Please check the official 
Placement and Admissions sections for detailed internship and batch information.
"""
code_splitter= RecursiveCharacterTextSplitter.from_language(language="python", 
chunk_size=1000, chunk_overlap=100)
docs = code_splitter.create_documents([code_text])