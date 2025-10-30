import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure imports from project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

from etl.load_and_clean import load_documents, clean_and_split


def build_vectorstore(index_dir: str = "faiss_index") -> None:
    """Build and save a FAISS vector store using local HF embeddings."""
    docs = load_documents()
    chunks = clean_and_split(docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(index_dir)
    print(f"✅ FAISS index created at: {index_dir}")


def get_retriever(index_dir: str = "faiss_index"):
    """Return a retriever from a FAISS vector store, building it if needed."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if not os.path.isdir(index_dir):
        build_vectorstore(index_dir)
    vectorstore = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
    return vectorstore.as_retriever(search_kwargs={"k": 3})


def build_groq_qa_chain():
    """Create a RetrievalQA chain using Groq LLM (llama3-8b-8192)."""
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")

    retriever = get_retriever()

    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0,
        groq_api_key=groq_api_key,
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
    )
    return qa


if __name__ == "__main__":
    # Simple demo run
    qa = build_groq_qa_chain()
    question = os.getenv(
        "GROQ_DEMO_QUESTION",
        "What are the side effects of Ibuprofen?",
    )
    result = qa.invoke({"query": question})

    print("\n🧠 Question:", question)
    print("\n💬 Answer:\n", result.get("result", "<no result>"))

    sources = result.get("source_documents", []) or []
    print("\n📚 Retrieved Source Documents (top 3):")
    for i, doc in enumerate(sources[:3], 1):
        meta = doc.metadata if hasattr(doc, "metadata") else {}
        print(f"[{i}] source={meta.get('source', '<unknown>')} | page={meta.get('page', '<n/a>')}")

