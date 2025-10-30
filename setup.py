"""
Setup script for PharmaDoc QA Assistant
Run this script to set up the project and build the vector database
"""
import os
import sys

def check_env_file():
    """Check if .env file exists and has API key."""
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("📝 Creating .env.example file...")
        print("✅ Please copy .env.example to .env and add your Google Gemini API key")
        return False
    
    with open('.env', 'r') as f:
        if 'GOOGLE_API_KEY' not in f.read():
            print("⚠️  Warning: GOOGLE_API_KEY not found in .env file")
            return False
    
    print("✅ .env file found with API key")
    return True

def main():
    print("🚀 PharmaDoc QA Assistant - Setup")
    print("=" * 50)
    
    # Check for .env file
    if not check_env_file():
        print("\n⚠️  Setup incomplete. Please add your Google Gemini API key first.")
        return
    
    # Check if requirements are installed
    print("\n📦 Installing requirements...")
    os.system(f"{sys.executable} -m pip install -r requirements.txt")
    
    # Build vectorstore
    print("\n🔨 Building vector database...")
    os.system(f"{sys.executable} rag/rag_pipeline.py")
    
    print("\n✅ Setup complete!")
    print("\n📖 Next steps:")
    print("1. Run: uvicorn app.backend:app --reload")
    print("2. Run (in another terminal): streamlit run app/frontend.py")

if __name__ == "__main__":
    main()
