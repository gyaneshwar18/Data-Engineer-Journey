import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
from config import API_KEY, CITY

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True) 

URL="https://api.openweathermap.org/data/2.5/weather"

def fetch_weather():
    params={
        "q": CITY,  
        "appid": API_KEY,
        "units": "metric"}
    response=requests.get(URL, params=params)
    response.raise_for_status()
    return response.json()

def transform_weather(data): 
    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "weather": data["weather"][0]["description"],
        "timestamp": datetime.utcnow()
    }

def save_to_csv(record):
    df=pd.DataFrame([record])
    output_file=OUTPUT_DIR / "weather_data.csv"
    
    df.to_csv(output_file, index=False)
   
def main():
    print("🌍 Fetching weather data...")
    data = fetch_weather()

    print("🔄 Transforming data...")
    record = transform_weather(data)

    print("💾 Saving to CSV...")
    save_to_csv(record)

if __name__ == "__main__":
    main()