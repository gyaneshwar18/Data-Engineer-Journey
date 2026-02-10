import requests
import time 
import logging
from pathlib import Path

# Config

URL="https://httpbin.org/json"
MAX_RETRIES=3
TIMEOUT=5

DOWNLOAD_DIR=Path("downloads")
LOG_DIR=Path("logs")

DOWNLOAD_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "downloader.log", 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Robust downloader function
def download_with_retry(url, retries=MAX_RETRIES):
    for attempt in range(1, retries + 1):
        try:
            print(f"Attempt {attempt}...")
           
            r=requests.get(url, timeout=TIMEOUT)
            r.raise_for_status()  # Check if the request was successful
            
            logging.info(f"Successfully downloaded: {url}")
            return r.content
        
        except requests.exceptions.Timeout:
            logging.warning(f"Timeout occurred for {url} on attempt {attempt}")
            print("Timeout occurred. Retrying...")

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred for {url}: {e}")
            break

        except requests.exceptions.RequestException as e:
            logging.error(f"Request error occurred for {url}: {e}")
    
    
        time.sleep(2) # Wait before retrying
    logging.critical(f"Failed to download {url} after {retries} attempts")
    return None


def save_file(content):
    file_path = DOWNLOAD_DIR / "data.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Saved to {file_path}")

def main():
    logging.info("Starting downloader...")
    data = download_with_retry(URL)  
    if data:
        save_file(data.decode('utf-8'))
    else:
        print("Failed to download content after multiple attempts.")
    
    logging.info("Downloader finished.")

if __name__ == "__main__":
    main()