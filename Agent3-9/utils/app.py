import os
import sys

# Always add the current file's directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.pdf_loader import load_all_pdfs
from utils.chunker import chunk_documents
from utils.embedder import embed_documents
from utils.vectorstore import get_vectorstore
from utils.retriever import get_retriever
from utils.compressor import compress_text

# Main function
def main():
    print("📄 Loading reference PDFs...")
    docs = load_all_pdfs("reference_pdfs")
    
    print("🔹 Splitting documents into chunks...")
    chunks = chunk_documents(docs)
    
    print("💾 Embedding and storing in Chroma/FAISS...")
    vectorstore = get_vectorstore(chunks)
    
    print("✅ Ready! Type your query below.\n")
    
    while True:
        query = input("Enter your query (or 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break
        
        retriever = get_retriever(vectorstore)
        results = retriever.get_relevant_documents(query)
        
        if results:
            print("\n🔍 Retrieved from local PDFs, summarizing...\n")
            summary = compress_text(results, query)
            print(summary)
        else:
            print("\n🌐 No relevant result found in local PDFs. Searching the web...\n")

if __name__ == "__main__":
    main()
