import logging

from earning_api.core.config import settings


def setup_logging():
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()])
    logging.getLogger("uvicorn").setLevel(
        logging.WARNING)  # Reduce uvicorn noise
