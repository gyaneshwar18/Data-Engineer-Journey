1. Understand Parameters

A parameter is an input value passed to a pipeline, dataset, or other supported ADF component.

Suppose you have 100 CSV files to copy.

Without parameters, you might create separate pipelines for different file names:

Pipeline 1 → Sales.csv
Pipeline 2 → Customers.csv
Pipeline 3 → Products.csv

With parameters, you can reuse the same pipeline:

                  One Pipeline
                       |
              File Name Parameter
                       |
              +--------+--------+
              |        |        |
              v        v        v
           Sales.csv Customers.csv Products.csv

You change the input value instead of building a completely new pipeline for every file.

Parameters are read-only during a pipeline run. You supply their values when starting the pipeline or through a trigger or parent pipeline.

Example

Parameter name:

pSourceFileName

Parameter value:

Sales.csv

ADF expression:

@pipeline().parameters.pSourceFileName

This expression retrieves the parameter value.

2. Understand Variables

A variable stores a value that can be changed while the pipeline runs.

For example:

Variable: vMessage

Initial value: Not started

During execution:
Copying Sales.csv

Variables are useful for storing and updating temporary values within a pipeline.

ADF provides a Set Variable activity to change a variable's value.

Example expression:

@concat('Copying file: ', pipeline().parameters.pSourceFileName)

If pSourceFileName is Sales.csv, the resulting string is:

Copying file: Sales.csv

Variables differ from parameters because variables can change during execution, whereas pipeline parameters are read-only.

Parameters vs Variables
Feature	Parameter	Variable
Purpose	Accept input	Store a temporary value
Value can change during the run?	No	Yes
Set at pipeline level?	Yes	Yes
Example	Input filename	Processing message
Typical use	Reusable pipelines	Runtime state or temporary values

Remember: Parameter = input. Variable = changeable runtime value.

Notebook 1 — Create a Parameterized Pipeline

We will create a new pipeline so your working Day 93 pipeline remains unchanged.

Step 1: Open ADF Studio

Open your Data Factory in the Azure portal and select Launch Studio.

Go to:

Author → + → Pipeline

Name the pipeline:

PL_Sales_Copy_Parameterized
Step 2: Create pipeline parameters

Click an empty area on the pipeline canvas so the pipeline's properties appear.

Open the Parameters tab and add these parameters:

Name	Type	Default value
pSourceFileName	String	Sales.csv
pDestinationFileName	String	sales_copy_day94.csv

The destination filename is intentionally different from the Day 93 output to help protect your existing practice file.

Step 3: Understand the expressions

To retrieve the source filename:

@pipeline().parameters.pSourceFileName

To retrieve the destination filename:

@pipeline().parameters.pDestinationFileName

These expressions return the values supplied to the pipeline.

Expected result: Your pipeline has two parameters.

Notebook 2 — Parameterize the Datasets

A pipeline parameter alone does not automatically change a dataset's file path. We must connect the parameter to the dataset configuration.

To avoid modifying your working Day 93 datasets, create two new datasets.

Step 1: Create the source dataset

Create a new ADLS Gen2 DelimitedText dataset.

Use:

Setting	Value
Name	DS_Sales_Source_Dynamic
Linked service	LS_ADLS_Gen2
Container	source
Directory	Leave blank
Initial file	Sales.csv
First row as header	Checked
Add a dataset parameter

Open the dataset's Parameters tab.

Create:

Name	Type	Default value
pFileName	String	Sales.csv

Next, open the dataset's Connection settings.

For the file name property, select Add dynamic content and use:

@dataset().pFileName

The dataset now uses its pFileName parameter to determine which file to read.

Step 2: Create the destination dataset

Create another ADLS Gen2 DelimitedText dataset.

Use:

Setting	Value
Name	DS_Sales_Destination_Dynamic
Linked service	LS_ADLS_Gen2
Container	destination
Directory	day92_test
Initial file	sales_copy_day94.csv
First row as header	Checked

Add this dataset parameter:

Name	Type	Default value
pFileName	String	sales_copy_day94.csv

In the file name property, use:

@dataset().pFileName

Important: The expressions above belong in the dataset's file name property. You will pass values into the dataset parameters from the pipeline in the next step.

Expected result

You now have two new datasets:

DS_Sales_Source_Dynamic
DS_Sales_Destination_Dynamic

Both datasets can accept different filenames without requiring you to create a different dataset for every CSV file.

ADF supports parameterizing dataset properties and passing pipeline parameter values into datasets.

Notebook 3 — Connect the Parameters to Copy Activity

Now we will make the parameterized pipeline perform the copy.

Step 1: Add Copy Activity

Open PL_Sales_Copy_Parameterized.

Add Copy data to the pipeline canvas and rename the activity:

Copy_Sales_CSV
Step 2: Configure the source

Open the Copy Activity's Source tab.

Select:

DS_Sales_Source_Dynamic

Under the dataset parameters, pass this value:

Dataset parameter	Value
pFileName	@pipeline().parameters.pSourceFileName

Use Add dynamic content if necessary to enter the expression.

Step 3: Configure the sink

Open the Sink tab.

Select:

DS_Sales_Destination_Dynamic

Pass this dataset parameter value:

Dataset parameter	Value
pFileName	@pipeline().parameters.pDestinationFileName
Step 4: Validate the pipeline

Select Validate or Validate All.

Correct any configuration errors before proceeding.

Your pipeline should now behave like this:

Pipeline: PL_Sales_Copy_Parameterized
                 |
                 v
          pSourceFileName
                 |
                 v
       DS_Sales_Source_Dynamic
                 |
                 v
           Copy Activity
                 |
                 v
     DS_Sales_Destination_Dynamic
                 ^
                 |
        pDestinationFileName
Example values
pSourceFileName      = Sales.csv
pDestinationFileName = sales_copy_day94.csv

The resulting source is:

source/Sales.csv

The resulting destination is:

destination/day92_test/sales_copy_day94.csv
Notebook 4 — Use a Variable

Now we will add a simple variable to understand how variables work.

Step 1: Create a pipeline variable

Select the pipeline canvas and open the Variables tab.

Add:

Setting	Value
Name	vRunMessage
Type	String
Default value	Not started
Step 2: Add Set Variable

Find the Set Variable activity.

Add it to the pipeline and rename it:

Set_Run_Message

In its settings, configure:

Field	Value
Variable name	vRunMessage
Value	Use the expression below
@concat('Preparing to copy ', pipeline().parameters.pSourceFileName)

For the default source filename, the value becomes:

Preparing to copy Sales.csv
Step 3: Connect the activities

Connect the activities in this order:

Set_Run_Message
       |
       | On success
       v
Copy_Sales_CSV

This ensures the variable is set before the copy activity runs.

Important: This variable is only an illustration of a runtime value. It does not prove the copy succeeded. We use activity execution results to determine whether the copy actually completed.

Step 4: Validate and save

Validate the pipeline.

If validation succeeds, save the current draft. We will test it in the next section.

Notebook 5 — Test with Different Parameter Values
Step 1: Run Debug

Select Debug.

When ADF asks for pipeline parameter values, use:

Parameter	Test value
pSourceFileName	Sales.csv
pDestinationFileName	sales_copy_day94.csv

Run the pipeline.

Step 2: Verify execution

Inspect the pipeline and activity execution results.

If the run succeeds, verify this destination in ADLS Gen2:

destination/day92_test/sales_copy_day94.csv

Do not assume success until you have checked the run result and destination.

Step 3: Try another destination filename

You can run the same pipeline again using a different destination filename:

pSourceFileName      = Sales.csv
pDestinationFileName = sales_copy_test2.csv

This time, the expected output path is:

destination/day92_test/sales_copy_test2.csv

The source remains unchanged.

Before running again, ensure that the new destination filename does not already contain important data.

What did you achieve?

You have used one pipeline with different parameter values instead of creating separate pipelines for different output filenames.

Note: These examples copy the same source data to different filenames. Parameterization makes a pipeline reusable; it does not itself implement incremental loading or process only new rows.

Day 94 — Interview Questions
Q1. What is a parameter in Azure Data Factory?

A parameter is an input value that controls pipeline or dataset behavior. It allows reusable pipelines to operate with different inputs.

Q2. What is a variable in ADF?

A variable stores a value that can be changed during pipeline execution using activities such as Set Variable.

Q3. What is the difference between parameters and variables?

Parameters are read-only inputs during a pipeline run. Variables can be modified while the pipeline executes.

Q4. How do you access a pipeline parameter?

Use:

@pipeline().parameters.parameterName
Q5. How do you access a variable?

Use:

@variables('variableName')
Q6. How do you make a dataset reusable?

Parameterize its properties, such as the filename or folder path, and pass different values to those parameters from the pipeline.

Q7. Why use parameters instead of creating many pipelines?

Parameters reduce duplication and make pipelines easier to maintain and reuse.

Q8. Can a pipeline parameter change after execution starts?

No. Pipeline parameters are read-only during that run. Variables can be modified during execution.

Q9. Can an ADF variable be modified inside a ForEach loop?

Yes, but take care with parallel iterations. ADF variables are pipeline-scoped and are not thread-safe, so modifying the same variable during parallel iterations can cause unexpected results.

Q10. Does parameterization automatically implement incremental loading?

No. Parameterization allows reusable configuration. Incremental loading requires logic to identify and process only new or changed data.

Twisted Interview Scenarios

Scenario 1: You need to copy 50 different CSV files. Would you build 50 pipelines?

Not necessarily. I would build a reusable, parameterized pipeline and supply the appropriate source and destination paths for each file.

Scenario 2: Your pipeline parameter is Sales.csv, but the activity cannot find the file. What would you check?

I would verify the pipeline parameter value, the mapping from the pipeline parameter to the dataset parameter, the dataset's dynamic file name expression, and the storage path.

Scenario 3: Your pipeline parameter says sales_copy.csv, but the sink writes to a different filename. What might be wrong?

The sink dataset may not be receiving the pipeline parameter correctly, or its file name property might still be hardcoded.

Scenario 4: The pipeline fails after Set Variable succeeds. Does that mean the copy succeeded?

No. The variable activity and Copy Activity are separate activities. I would inspect the Copy Activity's status and error details.

Scenario 5: Two parallel ForEach iterations update the same variable. What is the risk?

Because pipeline variables are shared at the pipeline level and are not thread-safe, concurrent updates may produce unexpected values. Use a design that avoids shared mutable state or use sequential execution when appropriate.

Day 94 Completion Checklist
 Created PL_Sales_Copy_Parameterized.
 Added pSourceFileName and pDestinationFileName.
 Created the two parameterized datasets.
 Passed pipeline parameters into dataset parameters.
 Configured the Copy Activity.
 Created vRunMessage.
 Added and configured Set Variable.
 Validated the pipeline.
 Debugged the pipeline if your configuration allows it.
 Verified the output file if execution succeeded.
 Can explain parameters, variables, and dynamic content in an interview.