Day 95 — Azure Data Factory: Control Flow Activities
Data Engineering Journey | Practical Hands-on

Today's goal: Learn and practise four important ADF activities: Lookup, Get Metadata, If Condition, and ForEach.

We will use your existing datalakegyan storage account and Sales.csv. We will also use the parameterized datasets from Day 94 where available.

1. Understand today's architecture
            Azure Data Factory
                    |
                    v
             Get Metadata
                    |
                    v
              If Condition
               /        \
            TRUE        FALSE
              |           |
              v           v
        Lookup + Copy    Fail
              |
              v
       ADLS Gen2 Destination

We will build this validation pipeline first, then practise ForEach in a separate pipeline.

2. Lookup Activity

What is it?

Lookup retrieves data from a supported data source so the pipeline can use that data during execution. It can return a single row or multiple rows, depending on its configuration.

Common real-world use: Read a configuration table containing filenames to process.

Example configuration:

FileName	Enabled
Sales.csv	True
Customers.csv	True
Products.csv	False

ADF can retrieve this configuration and use it to determine which files should be processed.

Practical: Read the first row of Sales.csv

For today's exercise, we will use your existing CSV to understand Lookup output.

Open ADF Studio → Author.
Create a new pipeline named PL_Sales_Lookup_Demo.
Add a Lookup activity.
Rename it Lookup_Sales_First_Row.
Select the source dataset DS_Sales_Source_Dynamic from Day 94, or your existing Sales CSV dataset.
If the dataset is parameterized, set its pFileName parameter to Sales.csv.
Enable First row only.
Validate and select Debug.

Expected result: The activity output should contain a firstRow object with columns from the first data record, depending on the dataset's CSV settings.

For example, its structure may resemble:

{
  "firstRow": {
    "Item_Identifier": "...",
    "Item_Weight": "...",
    "Item_Type": "..."
  }
}

The values above are illustrative, not actual values from your file.

Remember: This demonstrates Lookup. In production pipelines, Lookup is often more useful for retrieving processing instructions or configuration records.

3. Get Metadata Activity

What is it?

Get Metadata retrieves information about a file, folder, or supported data source.

Examples include:

Whether a file exists.
File size.
Last modified time.
File structure.
Child items within a folder.

For ADLS Gen2, Get Metadata supports fields such as exists, size, lastModified, and childItems, depending on the target and field selected.

Practical: Check whether Sales.csv exists

Create a new pipeline:

PL_Sales_Control_Flow
Step 1: Add Get Metadata

Add a Get Metadata activity and rename it:

Get_Sales_Metadata

Select your source dataset.

If you use DS_Sales_Source_Dynamic, set:

Parameter	Value
pFileName	Sales.csv

In the activity's Field list, select:

exists
size
Step 2: Validate and run

Validate the pipeline and select Debug.

Inspect the activity output.

When the file exists, the output should resemble:

{
  "exists": true,
  "size": 123456
}

The file size is illustrative.

When checking a missing file, selecting exists allows Get Metadata to return exists: false instead of failing simply because that object is absent.

Interview answer

Get Metadata retrieves information about a file or other supported data source. I can use its output to validate file existence, check metadata, and control subsequent pipeline activities.

4. If Condition Activity

What is it?

If Condition evaluates a Boolean expression and executes activities in either its True or False branch. It works similarly to an if/else statement in Python.

Practical: Copy only if the file exists

Continue with PL_Sales_Control_Flow.

Step 1: Add If Condition

Place an If Condition activity after Get_Sales_Metadata.

Connect the activities so that the If Condition runs after Get Metadata succeeds.

Rename it:

If_Sales_File_Exists
Step 2: Configure the expression

In the If Condition's expression field, use:

@activity('Get_Sales_Metadata').output.exists

This expression retrieves the exists value from the Get Metadata activity.

Step 3: Configure the True branch

Inside the True branch, add a Copy Activity named:

Copy_Sales_CSV

Configure it as follows.

Source:

Dataset: DS_Sales_Source_Dynamic
pFileName: @pipeline().parameters.pSourceFileName

Sink:

Dataset: DS_Sales_Destination_Dynamic
pFileName: @pipeline().parameters.pDestinationFileName

Use the Day 94 parameters if you created them. Otherwise, configure the activity with your existing source and destination datasets.

For a safe test, use these file values:

Source:
source/Sales.csv

Destination:
destination/day92_test/sales_copy_day95.csv

The dedicated destination filename helps protect your existing output.

Step 4: Configure the False branch

Add a Fail activity inside the False branch.

Use:

Activity name: Fail_Source_File_Missing
Error code: SOURCE_FILE_NOT_FOUND
Message: Source file was not found.
Final pipeline
Get_Sales_Metadata
         |
         v
 If_Sales_File_Exists
       /       \
    TRUE       FALSE
      |           |
      v           v
  Copy Sales     Fail
How it works

If the file exists:

Get Metadata → exists = true → Copy Activity

If the file does not exist:

Get Metadata → exists = false → Fail Activity

This prevents the pipeline from attempting the copy when the file is missing.

Important: Get Metadata must have exists selected in the field list for this pattern to work as expected. Otherwise, a missing object can cause the metadata activity itself to fail.

5. ForEach Activity

What is it?

ForEach repeats the activities inside it for every item in an array. It is useful when processing multiple files with the same pipeline logic.

For example:

Files:
[
  "Sales.csv",
  "Customers.csv",
  "Products.csv"
]
          |
          v
       ForEach
          |
          +--- Copy Sales.csv
          +--- Copy Customers.csv
          +--- Copy Products.csv

Each item can be passed to a parameterized dataset.

Practical: Copy files using ForEach

We will use a separate pipeline so your validation pipeline remains simple.

Step 1: Create a pipeline

Create:

PL_Sales_ForEach_Demo

Select the pipeline canvas and open its Parameters tab.

Add this parameter:

Name	Type	Default value
pFileNames	Array	["Sales.csv"]

For now, use only your existing Sales file. Add other filenames only after those files actually exist in the source container.

Step 2: Add ForEach

Add a ForEach activity and rename it:

ForEach_Sales_File

In the Settings → Items field, use:

@pipeline().parameters.pFileNames

Set Sequential to enabled for this simple exercise.

Step 3: Add Copy Activity inside ForEach

Open the ForEach activity's inner Activities editor and add a Copy Activity.

Name it:

Copy_Current_File

Configure the source:

Field	Value
Dataset	DS_Sales_Source_Dynamic
pFileName	@item()

Configure the sink:

Field	Value
Dataset	DS_Sales_Destination_Dynamic
pFileName	@concat('foreach_', item())

The destination dataset should continue to use the day92_test directory from Day 94.

Step 4: Validate and run

Debug the pipeline.

Because the default array contains one item, it should execute one iteration.

Expected destination:

destination/day92_test/foreach_Sales.csv
What happens if the array contains three files?

Suppose your source container contains:

Sales.csv
Customers.csv
Products.csv

The parameter could then be:

[
  "Sales.csv",
  "Customers.csv",
  "Products.csv"
]

ForEach runs the inner activities once per item, passing the current filename through @item().

Important: Do not add those extra filenames to your actual pipeline unless the corresponding files exist. The three-file example illustrates the pattern; today's hands-on test uses Sales.csv only.

6. Quick Revision: Four Activities
Activity	Purpose	Example
Lookup	Retrieve data to use in a pipeline	Read a configuration record
Get Metadata	Retrieve file or data-source metadata	Check whether Sales.csv exists
If Condition	Choose a branch based on a Boolean expression	Copy only if the source exists
ForEach	Repeat activities for items in an array	Process a list of filenames
Remember these expressions

Get file existence:

@activity('Get_Sales_Metadata').output.exists

Access a pipeline parameter:

@pipeline().parameters.pSourceFileName

Loop over the filename array:

@pipeline().parameters.pFileNames

Access the current ForEach item:

@item()
7. Day 95 Interview Questions

Q1. What is Lookup in ADF?

Lookup retrieves data from a supported source so it can be used by subsequent pipeline activities.

Q2. What is Get Metadata?

It retrieves information such as a file's existence, size, modification time, or folder contents.

Q3. What is If Condition?

It evaluates an expression and executes the True or False branch based on the result.

Q4. What is ForEach?

It executes a set of activities repeatedly for the items in an array.

Q5. What is the difference between Lookup and Get Metadata?

Lookup retrieves data records or values. Get Metadata retrieves information about a data object, such as its size or whether it exists.

Q6. How can you check whether a file exists before copying it?

Use Get Metadata with exists selected, then evaluate its output using If Condition before running Copy Activity.

Q7. How can you process 100 files using a reusable pipeline?

Use a ForEach activity with a list of file names and pass each filename into parameterized source and destination datasets.

Q8. What does @item() do?

It returns the current item being processed by the ForEach loop.

Q9. Can ForEach run iterations in parallel?

Yes. ADF supports sequential and parallel execution. Parallel execution must be configured carefully to avoid conflicting writes.

Q10. Why might Get Metadata fail even though the storage connection works?

The configured path may be wrong, the file might not exist, or the identity may not have the required permissions. Selecting exists allows the pipeline to handle a missing object as a Boolean result.

8. Twisted Interview Scenarios
Scenario 1: Your file is missing. How do you prevent Copy Activity from running?

Use Get Metadata to retrieve exists, followed by If Condition. Run Copy Activity only in the True branch and handle the False branch appropriately.

Scenario 2: You have 500 filenames. Should you create 500 pipelines?

Not necessarily. Use a reusable pipeline and iterate over the filenames with ForEach, passing each filename into parameterized datasets.

Scenario 3: Get Metadata succeeds, but Copy Activity fails. Why?

File existence does not guarantee that the source can be read or that the destination can be written. Investigate authentication, permissions, configuration, and the Copy Activity error.

Scenario 4: Why might parallel ForEach iterations cause problems?

Parallel iterations can conflict when they write to the same destination. Shared pipeline variables can also produce unexpected results when modified concurrently. Use suitable destinations and control execution where necessary.

Scenario 5: When would you use Lookup followed by ForEach?

When Lookup retrieves multiple configuration records, such as a list of tables or filenames, and ForEach needs to process each returned record individually.

9. Day 95 Completion Checklist
 Created and tested a Lookup activity.
 Used Get Metadata to inspect Sales.csv.
 Checked file existence using exists.
 Created an If Condition using the metadata output.
 Added Copy Activity to the True branch.
 Added Fail Activity to the False branch.
 Created a ForEach pipeline with an array parameter.
 Used @item() to pass a filename dynamically. 
 Verified the run results where execution succeeded.
 Can explain when to use each of the four activities. 