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

# ---------- FUNCTION DEFINITIONS ----------
def organize_files():
    """Organize files by extension into folders"""
    if not TARGET_DIR.exists():
        TARGET_DIR.mkdir(parents=True)

    for file in BASE_DIR.iterdir():
        if file.is_file():
            ext = file.suffix.replace('.', '')
            folder = TARGET_DIR / ext.upper()
            folder.mkdir(exist_ok=True)

            destination = folder / file.name
            shutil.move(str(file), str(destination))
            logging.info(f"Moved {file.name} → {folder}")
