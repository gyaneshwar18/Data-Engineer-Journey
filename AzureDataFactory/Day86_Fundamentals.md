1. What is Azure Data Factory?

Azure Data Factory (ADF) is a cloud-based data integration service used to move data between systems and orchestrate data workflows.

For example, suppose a company receives sales data every day.

Sales.csv
    |
    v
Azure Data Factory
    |
    v
Azure Data Lake Storage
    |
    v
Azure Databricks
    |
    v
Delta Lake
    |
    v
Reports / Analytics

ADF can orchestrate the workflow, move data, schedule execution, and monitor pipeline runs.

Databricks can then process and transform the data.

Simple interview answer

Azure Data Factory is a cloud-based data integration and orchestration service. It helps build, schedule, and monitor data pipelines that move and transform data between different systems.

2. Why do we need ADF?

Imagine a company receives 100 CSV files every day.

Without an orchestration service, someone might need to:

Run scripts manually.
Copy files between storage locations.
Start data processing.
Check whether processing succeeded.
Rerun failed tasks.

ADF helps automate these steps.

Main benefits:

Automates data movement.
Schedules pipeline execution.
Coordinates multiple activities.
Supports parameterized and reusable pipelines.
Provides execution monitoring and failure information.
Integrates with Azure services and other supported data systems.

Real-world example: ADF copies daily sales files into ADLS Gen2 and then triggers a Databricks notebook to process them.

3. Understand the five core ADF components

These are essential for both practical work and interviews.

3.1 Pipeline

A pipeline is a logical group of activities that performs a data workflow.

Example:

Sales Pipeline
      |
      v
Copy Sales.csv
      |
      v
Run Databricks Notebook
      |
      v
Validate Results

A pipeline coordinates the steps and their execution order.

Remember: A pipeline is the overall workflow.

3.2 Activity

An activity is an individual task inside a pipeline.

Examples:

Activity	Purpose
Copy Activity	Copies data from a source to a destination.
Lookup	Retrieves information from a supported data source.
Get Metadata	Retrieves metadata such as file properties.
ForEach	Iterates over a collection of items.
If Condition	Executes different paths based on a condition.
Databricks Notebook activity	Runs a Databricks notebook.

Remember: An activity is a task performed by the pipeline.

3.3 Linked Service

A linked service defines connection information for a data store or compute service.

Examples:

Azure Data Lake Storage Gen2 connection.
Azure SQL Database connection.
Azure Databricks connection.

Think of it as the connection configuration ADF uses to reach another service.

It can contain authentication and connection details, so credentials must be handled securely.

3.4 Dataset

A dataset identifies the data you want to work with inside a supported data store.

For example:

Storage account: datalakegyan
Container: source
File: Sales.csv
Format: CSV

This describes the source data ADF should read.

A destination dataset might describe a CSV file in another container.

A dataset does not itself copy the data; an activity such as Copy Activity performs the operation.

3.5 Integration Runtime (IR)

An Integration Runtime is the infrastructure ADF uses to perform data movement and, depending on its type and configuration, dispatch activities or execute supported data transformation tasks.

The main types are:

Type	Main purpose
Azure Integration Runtime	Cloud-based data movement and supported activity execution.
Self-hosted Integration Runtime	Connects ADF to data sources in private networks or environments that require a self-managed runtime.
Azure-SSIS Integration Runtime	Runs supported SQL Server Integration Services (SSIS) packages in Azure.

For our initial cloud-based ADLS exercises, Azure Integration Runtime is the main one to understand.

Interview tip: Integration Runtime is not the same thing as a linked service. A linked service defines the connection; the Integration Runtime provides the execution infrastructure.

4. Understand how the components work together

Consider copying Sales.csv from one ADLS Gen2 container to another.

                    PIPELINE
                       |
                       v
                 COPY ACTIVITY
                  /         \
                 v           v
          SOURCE DATASET   SINK DATASET
                 |           |
                 v           v
          SOURCE LINKED    SINK LINKED
             SERVICE         SERVICE
                 |           |
                 v           v
            ADLS SOURCE   ADLS DESTINATION
                  \         /
                   INTEGRATION
                     RUNTIME

This is a conceptual view; the exact configuration depends on the source, sink, and activity.

Example configuration
Component	Example
Pipeline	PL_Sales_Copy
Activity	Copy_Sales_CSV
Source linked service	Connection to ADLS Gen2
Source dataset	DS_Sales_Source
Sink dataset	DS_Sales_Destination
Integration Runtime	Azure Integration Runtime
One-line memory trick
Pipeline = workflow
Activity = task
Linked service = connection
Dataset = data being referenced
Integration Runtime = execution infrastructure
5. Day 91 practical — Open Azure Data Factory

Today, we will explore the service and understand its interface. We won't create unnecessary resources or change your existing storage data.

Step 1: Open Azure

Go to the official Azure portal.

Sign in to your Azure account.

Step 2: Find Data Factory
Search for Data factories.
Open the service.
Check whether you already have a Data Factory resource.

If you have one, open it.

If you don't have one, you can create one if your subscription permits it. Creating Azure resources may incur charges, so check the pricing and subscription details first.

Official documentation: Azure Data Factory documentation

Step 3: Launch ADF Studio

Open your Data Factory and select Launch Studio.

You should see the authoring environment.

Depending on the current interface, you may see areas for:

Author
Monitor
Manage
Author

Used to create and edit pipelines, datasets, linked services, and related resources.

Monitor

Used to inspect pipeline runs, activity runs, execution status, and failures.

Manage

Used to configure or manage items such as linked services, Integration Runtimes, and other factory settings.

Step 4: Explore without changing anything

Look for the following areas:

Pipelines
Datasets
Linked services
Integration Runtimes
Monitor

Don't create credentials or change permissions just for today's lesson.

Expected result: You understand where ADF pipelines are created, where connections are configured, and where executions are monitored.

6. How ADF fits with your existing Databricks setup

You have already worked with ADLS Gen2 and Databricks.

Your existing source file is:

Storage account: datalakegyan
Container: source
File: Sales.csv

Its path is:

abfss://source@datalakegyan.dfs.core.windows.net/Sales.csv

For the upcoming ADF lessons, the conceptual workflow is:

ADLS Gen2
   |
   | Sales.csv
   v
Azure Data Factory
   |
   | Copy Activity
   v
ADLS Gen2 destination
   |
   v
Azure Databricks
   |
   | PySpark transformations
   v
Delta Lake

We will reuse this dataset rather than introduce another one.

Important distinction: ADF and Databricks have different responsibilities. ADF orchestrates and moves data; Databricks processes data using Spark. ADF can also orchestrate Databricks notebook execution.

For the initial exercises, we will avoid overwriting your existing sales.csv or Delta table. We can choose a separate destination path when building the copy pipeline.

7. Day 91 interview questions and answers
Q1. What is Azure Data Factory?

Azure Data Factory is a cloud-based data integration and orchestration service used to build, schedule, and monitor data pipelines.

Q2. What is a pipeline in ADF?

A pipeline is a logical grouping of activities that together perform a data integration workflow.

Q3. What is an activity?

An activity is an individual operation within a pipeline, such as copying data, retrieving metadata, or executing a Databricks notebook.

Q4. What is a linked service?

A linked service defines connection information for a data store or compute service that ADF needs to access.

Q5. What is a dataset?

A dataset represents the structure or location of the data that an activity uses, such as a particular CSV file in ADLS Gen2.

Q6. What is Integration Runtime?

Integration Runtime provides the execution infrastructure used by ADF for supported data movement and activity execution.

Q7. What is the difference between a linked service and a dataset?

A linked service defines how to connect to a system. A dataset identifies which data to use within that system.

Q8. What is the difference between a pipeline and an activity?

A pipeline is the overall workflow, while an activity is an individual task within that workflow.

Q9. How does ADF work with Databricks?

ADF can orchestrate a Databricks notebook as part of a pipeline. ADF manages workflow execution, while Databricks performs the configured processing.

Q10. What is the purpose of the Monitor section?

It helps you inspect pipeline runs and activity execution, identify failures, and troubleshoot problems.

8. Twisted and real-world interview questions

These questions test whether you understand how the components work together.

Scenario 1: ADF cannot access the source file. What would you check?

Answer:

Verify the source file path.
Check the linked service configuration.
Verify authentication and storage permissions.
Check whether the configured Integration Runtime can reach the source.
Inspect the activity error in Monitor.
Scenario 2: The pipeline runs successfully, but the destination file is missing. What would you investigate?

Answer:

Check the Copy Activity's source and sink configuration, destination path, activity execution details, and whether the expected file or output structure matches the configured sink.

A successful pipeline run alone does not guarantee that the data landed where you expected.

Scenario 3: Why not put all connection details directly inside every activity?

Answer:

Linked services and datasets promote reuse and easier maintenance. Connection configuration can be managed separately from individual pipeline activities.

Scenario 4: You have 100 files to process. Should you create 100 pipelines?

Answer:

Not necessarily. A parameterized pipeline combined with a suitable looping pattern, such as ForEach, can process multiple files using reusable configuration.

We will practice this on Days 95–96.

Scenario 5: ADF moves the data, but the transformation fails. What would you do?

Answer:

Inspect the failed activity and its error details. If the failed step is a Databricks notebook, troubleshoot the notebook, data, permissions, or compute configuration. Fix the cause and rerun the appropriate workflow while considering whether earlier steps are safe to repeat.

9. Day 91 completion checklist

Before moving to Day 92, check whether you can explain each item without looking at the lesson.

 Define Azure Data Factory.
 Explain why companies use ADF.
 Explain pipelines and activities.
 Explain linked services and datasets.
 Explain Integration Runtime and its main types.
 Identify Author, Monitor, and Manage in ADF Studio.
 Explain how ADF and Databricks work together.
 Answer the interview questions above.