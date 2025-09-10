# RAG Agent

A Retrieval-Augmented Generation (RAG) agent that can answer questions based on local PDF documents and web search when needed.

## Features

- 📄 **PDF Document Processing**: Load and process PDF documents from a reference directory
- 🔍 **Semantic Search**: Use embeddings to find relevant document chunks
- 🤖 **AI-Powered Responses**: Generate contextual answers using LLM
- 🌐 **Web Search Fallback**: Search the web when local documents don't contain relevant information
- 📝 **Text Compression**: Compress and summarize retrieved information

## Project Structure

```
rag_agent/
├── app.py                 # Main application entry point
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── utils/                # Utility modules
│   ├── pdf_loader.py     # PDF document loading
│   ├── chunker.py        # Document chunking
│   ├── embedder.py       # Text embedding
│   ├── vectorstore.py    # Vector database operations
│   ├── retriever.py      # Document retrieval
│   └── compressor.py     # Text compression/summarization
└── reference_pdfs/       # Directory for PDF documents
```

## Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rag_agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the project root with the following variables:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_BASE_URL=your_openai_base_url
   OPENAI_MODEL=google/gemini-2.0-flash-001
   ```

6. **Add PDF documents**
   Place your PDF documents in the `reference_pdfs/` directory.

## Usage

1. **Run the application**
   ```bash
   python app.py
   ```

2. **Ask questions**
   The application will:
   - Load and process your PDF documents
   - Create embeddings and store them in a vector database
   - Allow you to ask questions interactively
   - Search local documents first, then web if needed

3. **Exit the application**
   Type `exit` when prompted for a query.

## Configuration

You can customize the application by modifying `config.py` or setting environment variables:

- `TOP_K`: Number of document chunks to retrieve (default: 5)
- `CHUNK_SIZE`: Size of document chunks (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `EMBED_MODEL`: Embedding model to use (default: sentence-transformers/all-MiniLM-L6-v2)

## Dependencies

- `langchain`: Framework for building LLM applications
- `langchain-community`: Community integrations for LangChain
- `sentence-transformers`: Text embedding models
- `faiss-cpu`: Vector similarity search
- `pypdf`: PDF processing
- `python-dotenv`: Environment variable management

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with LangChain framework
- Uses sentence-transformers for embeddings
- FAISS for efficient vector similarity search
