from typing import List
from langchain.schema import Document
from config import TOP_K

def get_retriever(vectorstore, k=4):
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": k})

