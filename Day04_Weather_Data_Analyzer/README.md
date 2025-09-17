# Day 04 – Weather Data Analyzer (Pandas + CSV)

## Overview
This project analyzes weather data (temperature, humidity) from a CSV file using **Pandas**.

### Tasks implemented in the notebook
- Load CSV (`sample_weather.csv` or your own `weather.csv`)
- Inspect and handle missing values
- Find the hottest day (overall and per city)
- Compute average temperature per city
- Save summary outputs as CSV files
- Plot average temperature by city (Matplotlib)

## Files in this folder
- `weather_analysis.ipynb` — Jupyter notebook with all steps
- `sample_weather.csv` — sample dataset (contains some missing values)
- `README.md` — this file

## How to run
1. Install dependencies:
```bash
pip install pandas jupyterlab matplotlib
```

2. Place your CSV (if you have one) in this folder and name it `weather.csv` (optional). 
   If not present, the notebook will use `sample_weather.csv` or generate a `weather.csv` from it.

3. Launch JupyterLab or Jupyter Notebook:
```bash
jupyter lab
```

4. Open `weather_analysis.ipynb` and run cells.

## Outputs produced by the notebook
- `hottest_day_overall.csv` — row for the hottest day in the dataset
- `hottest_day_per_city.csv` — hottest day per city
- `avg_temp_by_city.csv` — average temperature per city

