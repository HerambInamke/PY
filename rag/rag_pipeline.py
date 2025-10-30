import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from etl.load_and_clean import load_documents, clean_and_split

def build_vectorstore():
    """Build and save the FAISS vectorstore from documents."""
    docs = load_documents()
    chunks = clean_and_split(docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("faiss_index")
    print("✅ FAISS index created and saved locally.")

def load_qa_chain():
    """Load the pre-built vectorstore and return a QA chain."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    index_dir = "faiss_index"

    if not os.path.isdir(index_dir):
        build_vectorstore()

    vectorstore = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Initialize Groq LLM (no Hugging Face Hub dependency)
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")

    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0,
        groq_api_key=groq_api_key,
    )

    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    return qa

if __name__ == "__main__":
    build_vectorstore()