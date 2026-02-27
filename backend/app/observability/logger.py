import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    log_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    log_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(log_handler)
    
    return logger

# Enterprise metrics placeholder
class MetricsTracker:
    @staticmethod
    def track_request(endpoint: str, status: int):
        # Implementation for Prometheus/Grafana metrics
        pass

app_logger = setup_logger("job_hunter_ai")
