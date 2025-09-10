from langchain_community.vectorstores import FAISS
from utils.embedder import embed_documents

def get_vectorstore(documents):
    """
    Store embedded documents in a FAISS vector store.
    """
    embeddings = embed_documents(documents)
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore
