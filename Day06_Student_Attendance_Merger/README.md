# Day 06 – Student + Attendance Data Merger (ETL with Pandas)

## Objective
Combine student grades with attendance records to compute a performance score.

### Steps
1. Load both CSVs (grades + attendance)
2. Group by student to get average marks
3. Merge datasets on 'name'
4. Handle missing values
5. Compute weighted performance score (70% marks + 30% attendance)
6. Identify top performers
7. Save final merged CSV

### Run Commands
pip install pandas
python merge_etl.ipynb

### Output File
merged_cleaned_dataset.csv
