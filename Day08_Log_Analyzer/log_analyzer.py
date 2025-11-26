import re
import pandas as pd
from pathlib import Path

# Path to log file
LOG_FILE = Path("logs/file_log.txt")

# Regex pattern to extract timestamp, level, file, folder
pattern = r"^(.*?) \| (\w+) \| Moved (.*?) → (.*)$"