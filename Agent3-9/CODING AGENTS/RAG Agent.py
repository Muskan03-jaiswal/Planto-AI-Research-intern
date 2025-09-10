from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader

# Load and embed documents
loader = TextLoader("your_docs.txt")
docs = loader.load()
db = FAISS.from_documents(docs, OpenAIEmbeddings())

# Create RAG agent
rag_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=db.as_retriever()
)

# Ask a question
query = "What is the main idea of the document?"
response = rag_chain.run(query)
print("RAG Agent Response:", response)
s