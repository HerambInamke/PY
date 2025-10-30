import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Ensure project root is on PYTHONPATH so `rag` package is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.rag_pipeline import load_qa_chain

# Page configuration
st.set_page_config(page_title="PharmaDoc QA Assistant 💊", layout="centered")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.75rem;
        border-radius: 5px;
        border: none;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("💊 PharmaDoc QA Assistant")
st.write("Ask domain-specific questions from pharmaceutical research papers")

# Load env and cache QA chain locally (no FastAPI needed)
load_dotenv()

@st.cache_resource(show_spinner=False)
def get_qa():
    return load_qa_chain()

# Input section
st.header("📝 Enter Your Question")
query = st.text_input(
    "What would you like to know?", 
    placeholder="e.g., What are the side effects of Ibuprofen?",
    key="user_query"
)

# Ask button
if st.button("🔍 Ask", type="primary"):
    if query:
        with st.spinner("Searching through pharmaceutical documents..."):
            try:
                qa = get_qa()
                result = qa.invoke({"query": query})
                answer = result.get("result") or result.get("answer") or "No answer found."
                sources = result.get("source_documents") or []

                st.success("✅ Answer Found!")
                st.info(answer)

                if sources:
                    with st.expander("📚 Sources"):
                        for i, doc in enumerate(sources[:3], 1):
                            meta = getattr(doc, "metadata", {})
                            st.write(f"[{i}] source={meta.get('source', '<unknown>')} | page={meta.get('page', '<n/a>')}")
            except Exception as e:
                st.error(f"Error: {type(e).__name__}: {str(e)}")
    else:
        st.warning("⚠️ Please enter a question first.")

# Information section
with st.expander("ℹ️ How to use this assistant"):
    st.write("""
    1. Enter your question about pharmaceutical research
    2. Click the 'Ask' button
    3. Get AI-powered answers from medical documents
    
    **Example questions:**
    - What are the side effects of Ibuprofen?
    - Summarize FDA safety recommendations for paracetamol
    - What are drug interactions with aspirin?
    """)

# Sidebar with configuration
st.sidebar.title("⚙️ Configuration")
st.sidebar.info("Running in local Streamlit mode (no FastAPI)")
