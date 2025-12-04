import json
import pandas as pd
from pathlib import Path

JSON_FILE = Path("sample_data.json")

def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def json_to_dataframe(json_data):
    # Flatten nested JSON using pandas
    df = pd.json_normalize(json_data["students"])
    return df

def save_to_csv(df, filename="output.csv"):
    df.to_csv(filename, index=False)
    print(f"✅ CSV saved as {filename}")