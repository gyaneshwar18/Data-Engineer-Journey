import os
from pathlib import Path
import shutil
import logging
from datetime import datetime

# ---------- SETTINGS ----------
BASE_DIR = Path("sample_files")
TARGET_DIR = Path("organized_files")
LOG_FILE = Path("logs/file_log.txt")

# ---------- LOGGING CONFIG ----------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
