from backend.app.celery_worker import celery_app
from backend.app.parsers.pdf_parser import PDFParser
from backend.app.rag.retriever import rag_retriever
from backend.app.services.resume_service import ResumeService
import asyncio

@celery_app.task(name="process_resume_background")
def process_resume_background(file_path: str, filename: str):
    # 1. Parse PDF
    text = PDFParser.extract_text(file_path)
    
    # 2. Add to RAG (Vector DB)
    rag_retriever.add_resume(filename, text, {"filename": filename})
    
    return {"status": "completed", "filename": filename}

@celery_app.task(name="analyze_job_background")
def analyze_job_background(resume_content: str, job_description: str):
    # This is a wrapper for the async service logic
    loop = asyncio.get_event_loop()
    tailored = loop.run_until_complete(
        ResumeService.analyze_and_tailor(resume_content, job_description)
    )
    score = ResumeService.calculate_ats_score(resume_content, job_description)
    
    return {
        "tailored_resume": tailored,
        "ats_score": score
    }
