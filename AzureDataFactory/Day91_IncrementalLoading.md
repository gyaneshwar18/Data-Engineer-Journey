Day 97 — Azure Data Factory: Incremental Loading
Data Engineering Journey | Practical Hands-on

Today's goal: Learn how to process only new or changed data instead of repeatedly copying everything.

We will cover two important approaches:

File-level incremental loading: Copy only new or modified files from ADLS Gen2.
Row-level incremental loading: Copy only new or updated rows from a database using a watermark.

For your hands-on exercise, we will use your existing Sales.csv file and ADLS Gen2 configuration.

1. What Is Incremental Loading?

Suppose a company has a sales table containing 10 lakh records.

Every day, 5,000 new records arrive.

Full loading

Every run copies all 10 lakh records again.

Day 1: Copy 10 lakh records
Day 2: Copy 10 lakh records
Day 3: Copy 10 lakh records

This can waste time and resources.

Incremental loading

Instead, copy only the new or changed records.

Day 1: Copy initial 10 lakh records
Day 2: Copy only 5,000 new records
Day 3: Copy only 3,000 new records

Incremental loading is commonly used in data pipelines to avoid reloading the entire dataset each time. The exact approach depends on whether your source is a database table or a collection of files.

Interview answer

Incremental loading is a data ingestion technique that processes only new or changed data since the previous successful load, rather than repeatedly processing the entire dataset.

2. Two Types of Incremental Loading

Understanding this distinction is important.

Type 1: File-level incremental loading

Suppose your ADLS Gen2 source contains:

source/
    Sales_Jan.csv
    Sales_Feb.csv
    Sales_Mar.csv

You have already copied the January and February files.

When a new file arrives, you want to copy only that file.

ADLS Gen2 Source
       |
       v
Identify new or modified files
       |
       v
Copy only qualifying files
       |
       v
ADLS Gen2 Destination

ADF can filter files by their last-modified timestamp. The filter uses a start time inclusive and an end time exclusive, allowing consecutive time windows to be used without overlap.

Important: If a 5 GB file changes, file-level incremental loading may copy that entire changed file. It does not automatically identify only the new rows inside it.

Type 2: Row-level incremental loading

Suppose a database contains:

Sale_ID	Amount	LastModifiedTime
101	500	2026-10-26 10:00
102	700	2026-10-26 11:00
103	900	2026-10-27 09:00

If the last successful load processed records through 2026-10-26 11:00, the next run selects only records beyond that watermark, up to a newly calculated upper boundary.

Database Table
      |
      v
Find previously processed watermark
      |
      v
Find new watermark
      |
      v
Select records between both watermarks
      |
      v
Copy only qualifying rows
      |
      v
Update watermark after success

ADF supports this pattern using Lookup activities, Copy Activity, and a persistent store for the watermark value.

3. Understand the Watermark

A watermark records how far the previous incremental load progressed.

A watermark can be based on a suitable increasing ID or a reliable modification timestamp.

Example:

Previous watermark: 1000
New watermark:     1500

The pipeline selects records in this range:

SELECT *
FROM sales_source
WHERE Sale_ID > 1000
  AND Sale_ID <= 1500;

This selects records with IDs from 1001 through 1500, assuming the ID is a suitable incremental column.

For updates, a modification timestamp is usually more appropriate than an ID that only increases when rows are inserted.

Important rules
Read the previous watermark.
Calculate the new watermark.
Copy data between the two boundaries.
Update the saved watermark only after the copy succeeds.
Ensure the watermark column reliably identifies the changes you need to capture.

If the watermark is advanced before the copy completes, records can be skipped.

A watermark-based solution also needs to consider duplicate timestamps, late-arriving data, and how deletes are detected.

Remember: An ID-based watermark generally detects new inserts, not updates to existing rows. A reliable modification timestamp can detect inserts and updates when the source updates that timestamp. Ordinary watermark filtering does not automatically detect deleted rows.

4. Your Existing Sales.csv: What Can We Do?

Your current source is:

Storage account: datalakegyan
Source container: source
File: Sales.csv

Your Sales dataset contains fields such as:

Item_Identifier
Item_Weight
Item_Fat_Content
Item_Visibility
Item_Type
Item_MRP
Outlet_Identifier
Outlet_Establishment_Year
Outlet_Size
Outlet_Location_Type
Outlet_Type
Item_Outlet_Sales

The schema you've shared does not include a reliable LastModifiedTime column for individual sales records.

Therefore, we cannot implement the standard database watermark method directly on this CSV using a timestamp column that doesn't exist.

For today's hands-on exercise, we will practise file-level incremental loading using the file's last-modified timestamp. We will not modify your original file or your existing Delta tables.

5. Practical Notebook 1 — Check the Source File's Last-Modified Time

We will use ADF Studio and your existing ADLS Gen2 connection.

Step 1: Open the Azure portal

Open your storage account:

datalakegyan
    |
    v
Containers
    |
    v
source
    |
    v
Sales.csv
Step 2: Inspect the file

Open the file's properties or details and locate its Last modified timestamp.

Record the timestamp. The filter values used by ADF must be in UTC.

For example, suppose the file's last-modified time is:

2026-10-15T08:30:00Z

This is an illustrative value. Use the actual timestamp displayed for your file.

Step 3: Choose the first test window

Choose a start time earlier than the file's last-modified time and an end time later than it.

For the illustrative timestamp above:

LastModified_From = 2026-10-01T00:00:00Z
LastModified_To   = 2026-11-01T00:00:00Z

This window includes the example timestamp.

Your actual dates will depend on your file's properties.

Expected result: You know the timestamp range needed to select the existing Sales.csv file.

6. Practical Notebook 2 — Create a File-Level Incremental Pipeline

ADF provides a solution template called Copy new files only by LastModifiedDate. It is designed to copy new or changed files based on their modification timestamps.

We will use that template rather than building a complicated incremental framework from scratch.

Step 1: Open ADF Studio

Go to:

Author → + → Pipeline → Template Gallery

Look for:

Copy new files only by LastModifiedDate

Select the template and continue.

Step 2: Configure the source

Use your existing ADLS Gen2 storage connection where supported.

Configure the source to point to your source container.

Setting	Value
Storage account	datalakegyan
Container	source
Directory	Root of the container
File to process	Sales.csv is currently the existing file

The template works with a file-based source and can use modification time to filter qualifying files.

If the generated template uses a folder and wildcard filter, keep the filter scoped to the intended source directory rather than a broader storage location.

Step 3: Configure the destination

Use your existing destination container.

For today's practice, use a separate folder:

destination/day97_incremental/

This protects your existing files and the output from earlier lessons.

Step 4: Configure the timestamp parameters

The Microsoft template defines parameters including:

Parameter	Purpose
LastModified_From	Earliest permitted last-modified timestamp
LastModified_To	Exclusive upper boundary for the timestamp window
Source folder parameters	Identify where the source files are located
Destination folder parameters	Identify where the copied files should be written

Set the source and destination folder parameters according to your actual template fields.

Set the time window using the values you recorded in Practical Notebook 1.

Step 5: Validate the pipeline

Select Validate or Validate All.

Correct any errors in the linked services, dataset references, or parameter configuration.

Step 6: Debug the pipeline

Select Debug.

Inspect the run details and check whether the file was selected by the timestamp filter.

If the execution succeeds, the expected destination structure is:

destination/
    day97_incremental/
        Sales.csv

The template's actual destination filename and folder behavior depend on its generated configuration, so verify the result in ADF and ADLS rather than assuming it matches the example exactly.

Safety note: Before rerunning the same time window, inspect the destination and the sink's write behavior. Do not overwrite valuable files.

7. How Do We Make File-Level Loading Incremental Across Multiple Runs?

The first run demonstrates selecting a file by its modification timestamp. To avoid repeatedly copying the same file, the pipeline also needs a consistent strategy for tracking the time window already processed.

Example:

First run
LastModified_From = 2026-10-01T00:00:00Z
LastModified_To   = 2026-10-02T00:00:00Z

Files whose last-modified timestamps fall inside the window are selected.

Second run

After the first run succeeds, the next window begins at the previous upper boundary:

LastModified_From = 2026-10-02T00:00:00Z
LastModified_To   = 2026-10-03T00:00:00Z

Because the start boundary is inclusive and the end boundary is exclusive, adjacent windows can cover consecutive periods without overlapping.

For an automated production solution, persist the successful window boundary or derive it from a reliable schedule. Only advance the saved state after the relevant copy operation succeeds.

Remember: The filter selects files based on their last-modified timestamps. It does not prove that a file has never been processed before unless the pipeline also maintains appropriate state or uses a reliable time-window strategy.

Microsoft notes that filtering files by last-modified time can still require scanning source files, so scanning extremely large directories may be inefficient. Where possible, time-partitioned folders or filenames can make incremental file discovery more efficient.

8. How Does Database Watermark Loading Work?

This is the other major pattern you must know for Data Engineering interviews.

Suppose your source is a SQL database table with a reliable LastModifiedTime column.

The pipeline can use these activities:

Lookup_Old_Watermark
          |
          v
Lookup_New_Watermark
          |
          v
Copy_Incremental_Rows
          |
          v
Update_Watermark

The actual pipeline must ensure that the Copy Activity executes only when the watermark lookups succeed, and the watermark is updated only after copying succeeds.

Step 1: Get the old watermark

A control table stores the previously processed value.

Example:

Old watermark = 2026-10-26 11:00:00
Step 2: Get the new watermark

A Lookup activity calculates the current maximum timestamp from the source table.

Example query:

SELECT MAX(LastModifiedTime) AS NewWatermark
FROM dbo.SalesSource;

Example result:

New watermark = 2026-10-28 09:00:00
Step 3: Copy rows between the watermarks

The source query uses both boundaries:

SELECT *
FROM dbo.SalesSource
WHERE LastModifiedTime > '2026-10-26 11:00:00'
  AND LastModifiedTime <= '2026-10-28 09:00:00';

These timestamps are illustrative. In ADF, the actual query would use dynamic expressions that retrieve the old and new values from the Lookup activity outputs.

Step 4: Update the watermark

After the copy succeeds, update the saved watermark to:

2026-10-28 09:00:00

The next run starts from that saved value.

This is the watermark-based incremental loading pattern documented by Microsoft for database-to-storage data pipelines.

Important distinction

The SQL example above assumes a relational database source. It is not a query you can run directly against your current plain Sales.csv file using the ADLS Gen2 CSV dataset.

9. Day 97 Interview Questions and Answers
Q1. What is incremental loading?

Incremental loading processes new or changed data since the previous successful load instead of repeatedly reloading the entire dataset.

Q2. What is a watermark?

A watermark stores the point up to which data has been processed, often using an increasing ID or modification timestamp.

Q3. What is the difference between full loading and incremental loading?

Full loading processes the entire selected dataset. Incremental loading processes only the new or changed portion identified by the selected strategy.

Q4. How does ADF implement watermark-based loading?

A typical pipeline retrieves the old watermark, calculates the new watermark, copies rows between them, and updates the stored watermark only after a successful copy.

Q5. Can we use an ID as a watermark?

Yes, if the ID increases reliably for new records. An ID alone usually cannot detect updates to existing records.

Q6. Can a modification timestamp detect updates?

It can detect updates when the source reliably changes the timestamp whenever a record is updated. The pipeline must still handle edge cases such as duplicate timestamps and late-arriving changes.

Q7. Can ADF load only newly modified files?

Yes. ADF supports filtering files by their last-modified timestamp. This selects qualifying files, not individual rows within each file.

Q8. Why must the watermark be updated after a successful copy?

If the watermark advances before copying finishes, the next run may skip data that was never successfully copied.

Q9. Does watermark-based loading detect deleted records?

Not automatically. A deleted row may no longer exist for the query to retrieve. Detecting deletes generally requires additional change-tracking information, tombstones, or a suitable CDC mechanism.

Q10. Why can incremental loading still be slow when only a few files change?

If the pipeline scans a very large directory to find the files whose modification timestamps meet the filter, the scanning work can still be expensive. Organizing files in time-partitioned folders may be more efficient.

10. Twisted Interview Scenarios
Scenario 1: The Copy Activity fails, but the watermark has already been updated. What is the problem?

The pipeline could lose data because the next run starts from a watermark that includes records that were not successfully copied. The watermark should advance only after the copy succeeds.

Scenario 2: A record is updated, but its ID does not change. Will an ID watermark detect it?

Not necessarily. The record may fall below the saved ID watermark and never be selected again. A reliably updated modification timestamp or another change-detection mechanism is needed.

Scenario 3: A new file arrives in the source container, but the pipeline does not copy it. What would you check?

I would inspect the source path, timestamp filter boundaries and UTC values, linked service permissions, and the file's actual last-modified timestamp.

Scenario 4: Your source is one large CSV file that gets updated daily. Can file-level incremental loading copy only the new rows?

Not by filtering on the file's last-modified timestamp alone. That filter identifies the changed file, not which rows changed. You would need row-level change information, a reliable watermark column, or a processing solution that can detect the changed records.

Scenario 5: Should you use an ID watermark or a modification timestamp?

An increasing ID is suitable for detecting new inserts when IDs reliably increase. A modification timestamp is generally better when both inserts and updates must be detected, provided the timestamp is reliable and appropriately maintained.

11. Day 97 Completion Checklist
 Understand full loading versus incremental loading.
 Understand the difference between file-level and row-level incremental loading.
 Understand a watermark and how it is used.
 Inspected the last-modified timestamp of your existing Sales.csv.
 Explored the ADF file-level incremental-copy template.
 Used a separate practice destination.
 Validated the time-filter configuration.
 Debugged the pipeline if your environment permitted it.
 Verified the execution result.
 Understand why your existing CSV does not support the standard row-level timestamp watermark method directly.
 Can explain why the watermark should be updated only after successful copying.
