"""Installation and Setup Script"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Run a shell command"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Failed: {description}")
        return False
    print(f"✅ Completed: {description}")
    return True

def main():
    """Main setup function"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║         ResearchGraph AI - Setup Script                     ║
    ║    Scientific Paper Summarization & Citation Linking        ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    os.makedirs(".cache", exist_ok=True)
    print("✅ Created necessary directories")
    
    # Install Python dependencies
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    ):
        return False
    
    # Download spaCy model
    if not run_command(
        f"{sys.executable} -m spacy download en_core_web_sm",
        "Downloading spaCy English model"
    ):
        print("⚠️  spaCy model download failed (non-critical)")
    
    # Download NLTK data
    print("\n🔄 Downloading NLTK data...")
    import nltk
    nltk.download('punkt', quiet=True)
    print("✅ NLTK data ready")
    
    # Setup environment file
    if not os.path.exists(".env"):
        print("\n📝 Creating .env file from template...")
        subprocess.run("cp .env.example .env", shell=True)
        print("⚠️  Please edit .env with your configuration")
    
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                  Setup Complete! ✅                          ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  To run the application:                                     ║
    ║  $ streamlit run app.py                                      ║
    ║                                                              ║
    ║  The app will be available at: http://localhost:8501        ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    main()
