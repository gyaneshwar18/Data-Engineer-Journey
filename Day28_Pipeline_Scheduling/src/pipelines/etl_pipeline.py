import sys
import os

# Fix import paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.logger import get_logger

logger = get_logger()

def extract():
    logger.info("Extract started")
    data = ["order1", "order2", "order3"]
    return data

def transform(data):
    logger.info("Transform started")
    return [d.upper() for d in data]

def load(data):
    logger.info("Load started")
    print("Loaded Data:", data)

def run_pipeline():
    try:
        logger.info("Pipeline STARTED")

        data = extract()
        data = transform(data)
        load(data)

        logger.info("Pipeline COMPLETED")

    except Exception as e:
        logger.error(f"Pipeline FAILED: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()