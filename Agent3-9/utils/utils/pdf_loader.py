import os
from langchain_community.document_loaders import PyPDFLoader

def load_all_pdfs(pdf_folder):
    documents = []
    if not os.path.exists(pdf_folder):
        print(f"Folder '{pdf_folder}' not found.")
        return documents

    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(pdf_folder, filename)
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            documents.extend(docs)
    return documents
