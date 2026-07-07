"""Shared logging setup for pipeline stages."""
import os
import logging


def configure_pipeline_logging(log_dir="logs", log_file="pipeline_audit.log"):
    """Ensure the log directory exists and configure shared audit logging."""
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_dir, log_file),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
