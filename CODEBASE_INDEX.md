# 📚 Codebase Index

This document provides a comprehensive index of all modules, functions, and classes in the PharmaDoc QA Assistant codebase.

## 📁 Directory Structure

```
PY/
├── app/                    # Application layer (Backend API & Frontend UI)
├── etl/                    # Extract, Transform, Load (Document processing)
├── rag/                    # Retrieval-Augmented Generation pipeline
├── data/                   # Sample pharmaceutical documents
└── faiss_index/            # Generated vector database (runtime)
```

---

## 🎯 Module: `app/`

### `app/backend.py`
FastAPI backend server providing REST API endpoints for QA functionality.

#### Classes
- **`QueryRequest`** (Pydantic BaseModel)
  - **Fields:**
    - `question: str` - User's question to be answered

#### Functions
- **`get_qa()`**
  - **Purpose**: Lazy loader for QA chain (singleton pattern)
  - **Returns**: RetrievalQA chain instance
  - **Note**: Initializes on first call, caches for subsequent calls

#### API Endpoints
- **`GET /`**
  - **Purpose**: Health check endpoint
  - **Returns**: `{"status": "healthy", "message": "PharmaDoc QA API is running"}`
  
- **`POST /ask`**
  - **Purpose**: Process a question and return an answer
  - **Request Body**: `QueryRequest` (JSON with `question` field)
  - **Returns**: 
    ```json
    {
      "answer": "string",
      "status": "success" | "error",
      "error": "string" (if status is error)
    }
    ```
  - **Error Handling**: Catches `StopIteration`, general exceptions

#### Configuration
- CORS enabled for all origins (for Streamlit integration)
- Lazy QA chain loading (allows startup without index/env)

---

### `app/frontend.py`
Streamlit-based web interface for interactive question-answering.

#### Functions
- **`get_qa()`** (cached with `@st.cache_resource`)
  - **Purpose**: Load and cache QA chain for Streamlit session
  - **Returns**: RetrievalQA chain instance
  - **Caching**: Persists across Streamlit reruns

#### UI Components
- **Page Title**: "PharmaDoc QA Assistant 💊"
- **Input Section**: Text input for user questions
- **Ask Button**: Triggers QA query
- **Answer Display**: Shows answer with success indicator
- **Sources Section**: Expandable section showing source documents (top 3)
- **Help Section**: Expandable "How to use" guide
- **Sidebar**: Configuration information

#### Features
- Custom CSS styling (green theme)
- Error handling with user-friendly messages
- Source document metadata display (source file, page number)
- Loading spinner during query processing

---

## 🔄 Module: `etl/`

### `etl/load_and_clean.py`
Document loading and preprocessing functionality.

#### Functions
- **`load_documents(folder_path="data/sample_papers")`**
  - **Purpose**: Load PDF and text documents from specified directory
  - **Parameters:**
    - `folder_path` (str): Path to directory containing documents
  - **Returns**: List of LangChain Document objects
  - **Supported Formats**: `.pdf` (via PyPDFLoader), `.txt` (via TextLoader)
  - **Process**: Iterates through files, loads each with appropriate loader

- **`clean_and_split(docs)`**
  - **Purpose**: Split documents into smaller chunks for better retrieval
  - **Parameters:**
    - `docs`: List of LangChain Document objects
  - **Returns**: List of split Document chunks
  - **Configuration:**
    - Chunk size: 800 characters
    - Chunk overlap: 100 characters
  - **Splitter**: `RecursiveCharacterTextSplitter`

#### Usage Example
```python
docs = load_documents("data/sample_papers")
chunks = clean_and_split(docs)
```

---

## 🤖 Module: `rag/`

### `rag/rag_pipeline.py`
Main RAG pipeline implementation using Groq LLM and FAISS vector store.

#### Functions
- **`build_vectorstore()`**
  - **Purpose**: Build and save FAISS vectorstore from documents
  - **Process:**
    1. Loads documents via `load_documents()`
    2. Splits documents via `clean_and_split()`
    3. Creates embeddings using HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
    4. Builds FAISS index from document chunks
    5. Saves index to `faiss_index/` directory
  - **Output**: Prints success message when complete
  - **Side Effects**: Creates/saves `faiss_index/` directory

- **`load_qa_chain()`**
  - **Purpose**: Load pre-built vectorstore and return QA chain
  - **Process:**
    1. Loads or builds FAISS index
    2. Creates retriever with `k=3` (top 3 documents)
    3. Initializes Groq LLM (`llama-3.1-8b-instant`)
    4. Creates RetrievalQA chain
  - **Returns**: RetrievalQA chain instance
  - **Configuration:**
    - Embedding model: `sentence-transformers/all-MiniLM-L6-v2`
    - LLM: Groq `llama-3.1-8b-instant`
    - Temperature: 0 (deterministic)
    - Retrieval k: 3 documents
    - Return source documents: True
  - **Environment Variables Required**: `GROQ_API_KEY`
  - **Error Handling**: Raises `ValueError` if `GROQ_API_KEY` not found

#### Entry Point
When run as script: `python rag/rag_pipeline.py` → builds vectorstore

---

### `rag/rag_groq_pipeline.py`
Alternative/Extended Groq RAG pipeline implementation with additional utilities.

#### Functions
- **`build_vectorstore(index_dir: str = "faiss_index") -> None`**
  - **Purpose**: Build and save FAISS vector store (configurable directory)
  - **Parameters:**
    - `index_dir` (str): Directory to save FAISS index (default: "faiss_index")
  - **Returns**: None
  - **Process**: Same as `rag_pipeline.build_vectorstore()` but with configurable path
  - **Output**: Prints success message with index location

- **`get_retriever(index_dir: str = "faiss_index")`**
  - **Purpose**: Get retriever from FAISS vector store, building if needed
  - **Parameters:**
    - `index_dir` (str): Directory containing FAISS index (default: "faiss_index")
  - **Returns**: FAISS retriever instance
  - **Process:**
    1. Checks if index exists
    2. Builds index if missing
    3. Loads index and returns retriever
  - **Configuration**: `k=3` documents retrieved

- **`build_groq_qa_chain()`**
  - **Purpose**: Create RetrievalQA chain using Groq LLM
  - **Returns**: RetrievalQA chain instance
  - **Process:**
    1. Gets retriever via `get_retriever()`
    2. Initializes Groq LLM
    3. Creates RetrievalQA chain with source documents
  - **Configuration**: Same as `rag_pipeline.load_qa_chain()`
  - **Environment Variables Required**: `GROQ_API_KEY`

#### Entry Point
When run as script: `python rag/rag_groq_pipeline.py`
- Creates QA chain
- Runs demo question (from `GROQ_DEMO_QUESTION` env var or default)
- Prints question, answer, and source documents

---

## 🛠️ Module: Root Level

### `setup.py`
Setup script for project initialization and vector database building.

#### Functions
- **`check_env_file()`**
  - **Purpose**: Validate `.env` file existence and API key presence
  - **Returns**: `bool` - True if valid, False otherwise
  - **Checks:**
    - `.env` file exists
    - `GOOGLE_API_KEY` in file (note: outdated, should check `GROQ_API_KEY`)
  - **Side Effects**: Creates `.env.example` if `.env` missing

- **`main()`**
  - **Purpose**: Main setup orchestration
  - **Process:**
    1. Checks environment file
    2. Installs requirements
    3. Builds vector database
  - **Output**: Step-by-step progress messages
  - **Next Steps**: Prints instructions for running backend and frontend

---

## 📊 Data Flow

```
User Question
    ↓
[Streamlit Frontend] or [FastAPI Backend]
    ↓
load_qa_chain()
    ↓
[RetrievalQA Chain]
    ↓
    ├─→ [FAISS Retriever] → [Top 3 Documents]
    └─→ [Groq LLM] → [Generated Answer]
    ↓
Answer + Source Documents
    ↓
[User Interface]
```

## 🔑 Key Dependencies

### External Libraries
- **LangChain**: RAG pipeline orchestration
- **FAISS**: Vector similarity search
- **Groq**: LLM inference
- **HuggingFace**: Text embeddings
- **FastAPI**: REST API framework
- **Streamlit**: Web UI framework

### Internal Dependencies
```
app/backend.py → rag/rag_pipeline.py → etl/load_and_clean.py
app/frontend.py → rag/rag_pipeline.py → etl/load_and_clean.py
rag/rag_pipeline.py → etl/load_and_clean.py
rag/rag_groq_pipeline.py → etl/load_and_clean.py
```

## 🔐 Environment Variables

| Variable | Required | Purpose | Module |
|----------|----------|---------|--------|
| `GROQ_API_KEY` | Yes | Groq LLM API authentication | `rag/rag_pipeline.py`, `rag/rag_groq_pipeline.py` |
| `GROQ_DEMO_QUESTION` | No | Demo question for `rag_groq_pipeline.py` | `rag/rag_groq_pipeline.py` |
| `HUGGINGFACEHUB_API_TOKEN` | Optional | For private HuggingFace models | Not currently used |

## 📝 Configuration Defaults

### Document Processing
- **Chunk Size**: 800 characters
- **Chunk Overlap**: 100 characters
- **Supported Formats**: PDF (.pdf), Text (.txt)

### Vector Store
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Index Directory**: `faiss_index/`
- **Retrieval k**: 3 documents

### LLM Configuration
- **Model**: `llama-3.1-8b-instant` (Groq)
- **Temperature**: 0 (deterministic)
- **Return Source Documents**: True

## 🚀 Entry Points

1. **Setup**: `python setup.py`
2. **Build Index**: `python rag/rag_pipeline.py` or `python rag/rag_groq_pipeline.py`
3. **Backend API**: `uvicorn app.backend:app --reload`
4. **Frontend UI**: `streamlit run app/frontend.py`

## 🔍 Search & Navigation Tips

### Finding Functions
- **Document Loading**: `etl/load_and_clean.py`
- **Vector Store Building**: `rag/rag_pipeline.py::build_vectorstore()`
- **QA Chain Creation**: `rag/rag_pipeline.py::load_qa_chain()`
- **API Endpoints**: `app/backend.py`
- **UI Components**: `app/frontend.py`

### Common Modifications
- **Change Chunk Size**: `etl/load_and_clean.py::clean_and_split()`
- **Change Retrieval k**: `rag/rag_pipeline.py::load_qa_chain()` (retriever `search_kwargs`)
- **Change LLM Model**: `rag/rag_pipeline.py::load_qa_chain()` (ChatGroq `model_name`)
- **Change Embedding Model**: `rag/rag_pipeline.py::build_vectorstore()` (HuggingFaceEmbeddings `model_name`)

---

**Last Updated**: [Auto-generated index]
**Maintained By**: Development Team

