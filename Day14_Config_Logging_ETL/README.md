# Configurable ETL Pipeline with Logging

## 📌 Objective
Upgrade the class-based ETL pipeline by adding structured logging and external configuration.  
This makes the pipeline production-style, configurable, and observable — similar to real-world data engineering jobs.

This project demonstrates how to separate configuration from code and how to track pipeline execution using logs.

---

## 🧠 Concepts Covered

- Config-driven pipelines (JSON config file)
- Structured logging using Python logging module
- OOP ETL pipeline design
- Extract–Transform–Load stages
- Exception handling with logging
- Runtime configuration
- Pipeline observability

---

## ⚙️ Features Implemented

✅ External config file (config.json)  
✅ Structured logging to file  
✅ Configurable input/output paths  
✅ Logged ETL stages  
✅ Error logging with stack trace  
✅ OOP pipeline class  
✅ Production-style run method  

---



## 📄 config.json

Contains runtime configuration instead of hardcoding values.






## 📝 Log Output

After running, check:

    logs/etl.log

Example entries:

    INFO | Pipeline started
    INFO | Extract stage started
    INFO | Loaded 5 rows
    INFO | Transform stage started
    INFO | Aggregation complete
    INFO | Load stage started
    INFO | Saved output to output.csv
    INFO | Pipeline completed successfully

---

## 📊 Output (output.csv)

name,avg_marks  
Aryan,80.0  
Riya,89.0  
Sneha,92.0  

---

## 🏗️ Why This Matters in Data Engineering

Production pipelines must be:

- Configurable (no hard-coded paths)
- Observable (logs for every run)
- Maintainable (modular design)
- Debuggable
