# career-automation-ai

Job Hunter AI is a sophisticated career automation system designed to streamline your job search. It leverages Large Language Models (LLMs) and Vector Databases (RAG) to tailor your resume perfectly for every job application.

## 🚀 Key Features

-   **Resume Indexing (RAG)**: Automatically processes and indexes your resumes into ChromaDB for context-aware tailoring.
-   **Intelligent Tailoring**: Uses AI (OpenAI/Groq) to rewrite your resume based on a specific Job Description (JD).
-   **Side-by-Side Comparison**: Visually compare your original resume with the AI-tailored version.
-   **Dynamic ATS Scoring**: Get a high-precision compatibility score based on semantic matching.
-   **Professional Exports**:
    -   **PDF**: Clean layout with automatic text wrapping and standard margins.
    -   **DOCX**: Fully editable Word document with highlighted sections.
-   **Job Scraper**: Integrated tool to fetch job details directly from URLs (LinkedIn, etc.).

## 🛠 Tech Stack

-   **Backend**: FastAPI, Uvicorn, Python 3.11+
-   **Frontend**: Vanilla HTML5, CSS3 (Rich UI), JavaScript
-   **AI/LLM**: Groq (Llama 3)
-   **Vector Database**: ChromaDB
-   **Task Queue**: Celery (Filesystem broker for Windows compatibility)
-   **PDF Engine**: ReportLab (Platypus framework)
-   **Doc Engine**: Python-docx

## 🏁 Getting Started

### 1. Prerequisites
-   Python 3.11 or higher
-   PowerShell (on Windows)

### 2. Installation
Clone the repository and install dependencies:
```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_api_key_here
CHROMA_PATH=./vector_db
WORKSPACE_ROOT="D:/Job Hunter"
```

## 🏃 Running the Application

The system requires four components to be running simultaneously:

1.  **ChromaDB**:
    ```powershell
    chroma run --path ./vector_db --port 8001
    ```
2.  **FastAPI Backend**:
    ```powershell
    uvicorn backend.main:app --reload --port 8000
    ```
3.  **Celery Worker** (for background tasks):
    ```powershell
    $env:CELERY_BROKER_URL="filesystem://"; $env:PYTHONPATH="."; celery -A backend.app.core.celery_app worker --loglevel=info -P solo
    ```
4.  **Frontend**:
    ```powershell
    python -m http.server 3000
    ```

Access the dashboard at: **[http://localhost:3000/frontend/index.html](http://localhost:3000/frontend/index.html)**

## 📖 Usage Guide

1.  **Index Resume**: Upload your master resume and authenticate.
2.  **Find Job**: Paste a LinkedIn/Job URL into the analyzer.
3.  **Tailor**: Click "Analyze & Tailor" to start the AI process.
4.  **Review**: Check the side-by-side view and ATS score.
5.  **Export**: Download your optimized PDF or DOCX file.

---

