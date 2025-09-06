# Day 03 – CSV Sales Data Analyzer

## Project Overview
This project demonstrates how to use **Pandas** to analyze sales data stored in a CSV file.

### Tasks Implemented
1. Load the CSV file using Pandas.
2. Calculate **total sales** across all products.
3. Group sales data by product and find the **best-selling product**.
4. Sort the results to display products by sales volume.

### Files
- `sales_analyzer.ipynb` → Jupyter Notebook with analysis steps.
- `sample_sales.csv` → Sample dataset for testing.
- `README.md` → Project documentation.

### How to Run
1. Open the notebook in **JupyterLab** or **VS Code with Jupyter extension**.
2. Run all cells in `sales_analyzer.ipynb`.
3. Review the outputs for total and product-wise sales analysis.

### Example Output
```
Total Sales: 500

Sales by Product (Descending):
Apple     300
Banana    150
Orange     50
Name: sales, dtype: int64
```

### Next Steps
- Expand analysis with more metrics (average, min, max sales).
- Visualize results using **Matplotlib/Seaborn** charts.
