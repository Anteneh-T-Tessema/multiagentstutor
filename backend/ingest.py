import os
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Configuration
KNOWLEDGE_DIR = "knowledge"
DB_DIR = "chroma_db"

def ingest_data():
    print("🚀 Starting Ingestion Pipeline...")
    
    # 1. Load Documents
    # We use a DirectoryLoader to ingest raw business knowledge (Markdown).
    print(f"Loading documents from {KNOWLEDGE_DIR}...")
    loader = DirectoryLoader(KNOWLEDGE_DIR, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader)
    documents = loader.load()

    # 2. Chunk Documents
    # Strategic Choice: RecursiveCharacterTextSplitter preserves structural context
    # by trying to split on paragraphs and sentences first, preventing 'dangling' logic.
    print("Chunking documents...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    # 3. Initialize Embeddings
    # We use local embeddings (nomic-embed-text) to ensure data privacy (HIPAA compliance).
    print("Initializing embeddings with nomic-embed-text...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # 4. Create Vector Store
    print(f"Creating ChromaDB at {DB_DIR}...")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    
    print(f"✅ Ingestion complete! {len(chunks)} chunks stored.")

if __name__ == "__main__":
    ingest_data()
