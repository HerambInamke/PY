import sys
import os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag.rag_pipeline import load_qa_chain

app = FastAPI()

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load QA chain (lazily, so startup still works if env/index not ready)
qa = None

def get_qa():
    global qa
    if qa is None:
        qa = load_qa_chain()
    return qa

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def health_check():
    return {"status": "healthy", "message": "PharmaDoc QA API is running"}

@app.post("/ask")
def ask_question(request: QueryRequest):
    """Process a question and return an answer using RAG."""
    try:
        result = get_qa().invoke({"query": request.question})
        answer = result.get("result", "No answer found.")
        return {"answer": answer, "status": "success"}
    except StopIteration:
        return {
            "answer": None,
            "status": "error",
            "error": "Model returned no text. Try a different HF model or provider."
        }
    except Exception as e:
        # Include more context to help diagnose issues from the UI
        return {
            "answer": None,
            "status": "error",
            "error": f"{type(e).__name__}: {str(e)}"
        }
