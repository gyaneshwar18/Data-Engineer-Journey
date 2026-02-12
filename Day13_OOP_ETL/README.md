# Day 13 — OOP ETL Pipeline (Class-Based Data Job)

## 📌 Objective
Build a class-based ETL (Extract–Transform–Load) pipeline using Python and Pandas.  
Instead of writing loose scripts, this project structures the data workflow using Object-Oriented Programming (OOP), similar to how production data pipelines are designed.

---

## 🧠 Concepts Covered

- Python Classes & OOP
- __init__ constructor
- Instance variables
- Method-based pipeline stages
- ETL design pattern
- Pandas aggregation
- CSV ingestion and export
- Modular pipeline structure

---

## ⚙️ ETL Stages Implemented

### 1️⃣ Extract
- Read CSV file using Pandas
- Load into DataFrame

### 2️⃣ Transform
- Convert marks column to numeric
- Handle invalid values
- Group by student name
- Compute average marks

### 3️⃣ Load
- Save transformed output to CSV

### 4️⃣ Run
- Orchestrates extract → transform → load sequence

---

## 📂 Project Structure

Day13_OOP_ETL/
│
├── etl_pipeline.py
├── input.csv
├── output.csv
└── README.md

---

## 📄 Sample Input (input.csv)

name,marks
Riya,88
Aryan,75
Sneha,92
Riya,90
Aryan,85

---

## ▶️ How to Run

Install dependency:

    pip install pandas

Run pipeline:

    python etl_pipeline.py

---

## 📊 Sample Output (output.csv)

name,avg_marks
Aryan,80.0
Riya,89.0
Sneha,92.0

---

## 🏗️ Why OOP for Data Pipelines?

Using classes makes pipelines:

- Reusable
- Configurable
- Testable
- Modular
- Production-friendly

Each ETL stage is a method:
- extract()
- transform()
- load()b 
- run()

This mirrors real-world pipeline frameworks like Airflow operators and ETL job classes.

---

## 💬 Interview Explanation (Short Version)

This project demonstrates a class-based ETL pipeline where extract, transform, and load are implemented as methods. The pipeline is configurable via constructor parameters and executed through a run() orchestrator method, following production ETL design patterns.

---

## 🚀 Next Step

Day 14 → Logging + Configurable Pipelines  
(Add logging, config files, and environment separation to make this production-grade.)
