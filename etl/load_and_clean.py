import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_documents(folder_path="data/sample_papers"):
    """Load PDF and text documents from the specified folder."""
    documents = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif file.endswith(".txt"):
            loader = TextLoader(file_path)
            documents.extend(loader.load())
    return documents

def clean_and_split(docs):
    """Split documents into smaller chunks for better retrieval."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    return splitter.split_documents(docs)

if __name__ == "__main__":
    docs = load_documents()
    chunks = clean_and_split(docs)
    print(f"Loaded {len(chunks)} text chunks from {len(docs)} docs")
