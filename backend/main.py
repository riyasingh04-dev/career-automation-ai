from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.resume_routes import router as resume_router
from backend.app.core.security import get_current_user
import uvicorn

app = FastAPI(
    title="Job Hunter AI - Production",
    description="Enterprise-grade AI Job Automation System",
    version="2.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# Include Routers with Auth
app.include_router(resume_router, dependencies=[Depends(get_current_user)])

@app.get("/")
async def root():
    return {"message": "Job Hunter AI Production API", "status": "online"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
