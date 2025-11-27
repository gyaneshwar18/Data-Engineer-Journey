import re
import pandas as pd
from pathlib import Path

# Path to log file
LOG_FILE = Path("logs/file_log.txt")

# Regex pattern to extract timestamp, level, file, folder
pattern = r"^(.*?) \| (\w+) \| Moved (.*?) → (.*)$"

data = []

with open(LOG_FILE, "r") as f:
    for line in f:
        match = re.match(pattern, line.strip())
        if match:
            timestamp, level, filename, folder = match.groups()
            data.append([timestamp, level, filename, folder])

# Create DataFrame
df = pd.DataFrame(data, columns=["timestamp", "level", "filename", "folder"])

print("Extracted Log Data:")
print(df, "\n")