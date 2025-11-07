import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Ensure project root is on PYTHONPATH so `rag` package is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.rag_pipeline import load_qa_chain

# Page configuration
st.set_page_config(
    page_title="PharmaDoc QA Assistant",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern, clean CSS with aesthetic colors and whitespace
st.markdown("""
    <style>
    /* Global Styles */
    .main {
        padding: 4rem 3rem 3rem 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Remove default Streamlit styling */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom container styling */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    
    /* Title Styling */
    h1 {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    /* Subtitle */
    .subtitle {
        font-size: 1.2rem;
        color: #64748b;
        margin-bottom: 3rem;
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Section Headers */
    h2, h3 {
        color: #1e293b;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Input Styling */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 1rem 1.25rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background-color: #ffffff;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    /* Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        border: none;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(102, 126, 234, 0.3);
        margin-top: 1.5rem;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Answer Card */
    .answer-card {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    /* Success Message */
    .stSuccess {
        background-color: #ecfdf5;
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1.5rem 0;
    }
    
    /* Info Box */
    .stInfo {
        background-color: #f0f9ff;
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        line-height: 1.8;
        color: #1e293b;
    }
    
    /* Error Message */
    .stError {
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1.5rem 0;
    }
    
    /* Warning Message */
    .stWarning {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1.5rem 0;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-weight: 600;
        color: #475569;
    }
    
    .streamlit-expanderContent {
        padding: 1.5rem;
        background-color: #ffffff;
        border-radius: 0 0 8px 8px;
    }
    
    /* Source Cards */
    .source-item {
        background: #f8fafc;
        border-left: 3px solid #667eea;
        padding: 1rem 1.5rem;
        margin: 0.75rem 0;
        border-radius: 8px;
        font-size: 0.95rem;
        color: #475569;
    }
    
    /* Spinner */
    .stSpinner>div {
        border-top-color: #667eea;
    }
    
    /* Sidebar */
    .css-1d391kg {
        padding-top: 3rem;
    }
    
    /* Custom spacing */
    .spacer {
        height: 2rem;
    }
    
    /* Example questions styling */
    .example-questions {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .example-item {
        background: white;
        padding: 0.75rem 1.25rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        color: #475569;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .example-item:hover {
        border-color: #667eea;
        background: #f8fafc;
        transform: translateX(4px);
    }
    </style>
""", unsafe_allow_html=True)

# Load env and cache QA chain locally
load_dotenv()

@st.cache_resource(show_spinner=False)
def get_qa():
    return load_qa_chain()

# Header Section with gradient title
st.markdown("""
    <div style="margin-bottom: 3rem;">
        <h1>PharmaDoc QA Assistant</h1>
        <p class="subtitle">
            Ask intelligent questions and get accurate answers from pharmaceutical research documents
        </p>
    </div>
""", unsafe_allow_html=True)

# Main Content Area
col1, col2, col3 = st.columns([1, 8, 1])

with col2:
    # Question Input Section
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    
    query = st.text_input(
        "",
        placeholder="What would you like to know about pharmaceutical research?",
        key="user_query",
        label_visibility="collapsed"
    )
    
    # Ask Button
    ask_button = st.button("Ask Question →", type="primary", use_container_width=True)
    
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    
    # Process Query
    if ask_button:
        if query:
            with st.spinner("🔍 Searching through pharmaceutical documents..."):
                try:
                    qa = get_qa()
                    result = qa.invoke({"query": query})
                    answer = result.get("result") or result.get("answer") or "No answer found."
                    sources = result.get("source_documents") or []
                    
                    # Answer Display
                    st.markdown("""
                        <div class="answer-card">
                            <h3 style="color: #667eea; margin-top: 0; margin-bottom: 1rem;">Answer</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div style="
                            background: white;
                            padding: 2rem;
                            border-radius: 12px;
                            border: 1px solid #e2e8f0;
                            line-height: 1.8;
                            color: #1e293b;
                            font-size: 1.05rem;
                            margin-bottom: 2rem;
                        ">
                            {answer}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Sources Section
                    if sources:
                        with st.expander("📚 View Source Documents", expanded=False):
                            st.markdown("""
                                <div style="margin-top: 1rem;">
                            """, unsafe_allow_html=True)
                            for i, doc in enumerate(sources[:3], 1):
                                meta = getattr(doc, "metadata", {})
                                source = meta.get('source', '<unknown>')
                                page = meta.get('page', '<n/a>')
                                # Extract filename from path
                                if isinstance(source, str) and '/' in source:
                                    source = source.split('/')[-1]
                                elif isinstance(source, str) and '\\' in source:
                                    source = source.split('\\')[-1]
                                
                                st.markdown(f"""
                                    <div class="source-item">
                                        <strong>Source {i}:</strong> {source}<br>
                                        <span style="color: #94a3b8; font-size: 0.9rem;">Page: {page}</span>
                                    </div>
                                """, unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error: {type(e).__name__}: {str(e)}")
        else:
            st.warning("⚠️ Please enter a question before asking.")
    
    # Example Questions Section
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    
    with st.expander("💡 Example Questions", expanded=False):
        st.markdown("""
            <div style="padding: 1rem 0;">
                <p style="color: #64748b; margin-bottom: 1.5rem;">
                    Try asking these questions to get started:
                </p>
        """, unsafe_allow_html=True)
        
        examples = [
            "What are the side effects of Ibuprofen?",
            "Summarize FDA safety recommendations for paracetamol",
            "What are drug interactions with aspirin?",
            "What is the recommended dosage for Ibuprofen?",
            "What are the contraindications for NSAIDs?"
        ]
        
        for example in examples:
            if st.button(example, key=f"example_{example}", use_container_width=True):
                st.session_state.user_query = example
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Help Section
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    
    with st.expander("ℹ️ How to Use", expanded=False):
        st.markdown("""
            <div style="line-height: 1.8; color: #475569;">
                <p><strong>1. Enter your question</strong><br>
                Type your question about pharmaceutical research in the input field above.</p>
                
                <p><strong>2. Click 'Ask Question'</strong><br>
                The system will search through indexed pharmaceutical documents to find relevant information.</p>
                
                <p><strong>3. Review the answer</strong><br>
                Read the AI-powered answer and check the source documents for verification.</p>
                
                <p style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #e2e8f0;">
                    <strong>Note:</strong> Answers are generated using Retrieval-Augmented Generation (RAG) technology,
                    which combines large language models with document search for accurate, source-backed responses.
                </p>
            </div>
        """, unsafe_allow_html=True)

# Sidebar (Collapsed by default, can be expanded)
with st.sidebar:
    st.markdown("""
        <div style="padding: 2rem 0;">
            <h3 style="color: #667eea; margin-bottom: 1rem;">⚙️ Settings</h3>
            <p style="color: #64748b; font-size: 0.9rem; line-height: 1.6;">
                Running in local Streamlit mode
            </p>
        </div>
    """, unsafe_allow_html=True)
