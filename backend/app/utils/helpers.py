import os

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
