import eventlet
eventlet.monkey_patch()

from celery import Celery
import os

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")

# Fallback to filesystem if configured
if CELERY_BROKER_URL.startswith("filesystem://"):
    # Ensure directories exist with absolute paths
    BROKER_FOLDER = os.path.abspath(os.path.join(os.getcwd(), "broker"))
    for folder in ["out", "processed", "results"]:
        os.makedirs(os.path.join(BROKER_FOLDER, folder), exist_ok=True)
    
    # Celery expects result_backend path to be a URI-like string
    # For Windows, we ensure forward slashes and correct prefix
    results_path = os.path.join(BROKER_FOLDER, "results").replace("\\", "/")
    if not results_path.startswith("/"):
        results_path = "/" + results_path
    
    celery_app = Celery(
        "job_hunter_tasks",
        include=["backend.app.tasks.resume_tasks"]
    )
    celery_app.conf.update(
        broker_url="filesystem://",
        broker_transport_options={
            "data_folder_in": os.path.join(BROKER_FOLDER, "out"),
            "data_folder_out": os.path.join(BROKER_FOLDER, "out"),
            "data_folder_processed": os.path.join(BROKER_FOLDER, "processed"),
        },
        result_backend="file://" + results_path,
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
    )
else:
    celery_app = Celery(
        "job_hunter_tasks",
        broker=CELERY_BROKER_URL,
        backend=CELERY_RESULT_BACKEND,
        include=["backend.app.tasks.resume_tasks"]
    )
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
    )
