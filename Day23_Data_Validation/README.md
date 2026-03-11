# Description

This project implements a data validation layer in a data ingestion pipeline.

When data arrives from external sources such as CSV files or APIs, it may contain errors. Examples include missing values, incorrect formats, or invalid values.

Before loading the data into the database, the pipeline validates each record.

If the record passes validation checks, it is inserted into the main table.

If the record fails validation, it is inserted into a reject table along with the reason for rejection.

This approach ensures that only clean and reliable data enters the database.



# Usage

The pipeline reads data from a CSV file and processes each record.

Validation checks include:

ensuring customer_id is not missing

verifying amount values are positive numbers

validating date format

ensuring status values belong to an allowed set

# Example valid statuses:

completed

pending

cancelled

If a record fails any validation rule, it is saved in the reject table so that data engineers can review and fix it later.