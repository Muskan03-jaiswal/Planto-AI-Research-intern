from langchain_community.embeddings import HuggingFaceEmbeddings

def embed_documents(documents):
    """
    Create embeddings for documents using a free Hugging Face model.
    """
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
