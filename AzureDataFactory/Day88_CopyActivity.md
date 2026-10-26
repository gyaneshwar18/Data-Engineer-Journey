Day 92 — Azure Data Factory: Linked Services and Datasets
Data Engineering Journey | Practical Lesson

Today's goal: Connect Azure Data Factory to your existing ADLS Gen2 storage and define the source and destination datasets. We will prepare everything needed for the Copy Activity exercise on Day 93.

We'll use your existing configuration:

Setting	Your setup
Storage account	datalakegyan
Source container	source
Source file	Sales.csv
Destination container	destination
Destination folder for practice	day92_test

Today's workflow:

Azure Data Factory
        |
        v
   Linked Service
        |
        v
   ADLS Gen2 Account
        |
        +---------------------+
        |                     |
        v                     v
 Source Dataset        Destination Dataset
        |                     |
        v                     v
 source/Sales.csv      destination/day92_test/sales_copy.csv

By the end of today's lesson, you should have one linked service and two datasets configured. We will copy the actual data on Day 93.

1. Understand Linked Services

A Linked Service defines the connection information Azure Data Factory needs to access a data store or compute service. It includes connection details and authentication configuration.

For example, you want ADF to access your storage account:

Storage Account: datalakegyan
Endpoint: https://datalakegyan.dfs.core.windows.net

ADF needs a connection to this storage account.

You create a linked service named:

LS_ADLS_Gen2

Here, LS is simply a naming convention for Linked Service.

Why do we need it?

Without a configured connection, ADF cannot use its storage connector to access your files.

Interview answer

A linked service defines the connection and authentication details needed for Azure Data Factory to connect to a data store or compute service.

2. Understand Datasets

A Dataset identifies the data that an ADF activity will use as its input or output. It references a data store through a linked service and specifies details such as the file location and format.

For example, your source file is:

Container: source
File: Sales.csv
Format: CSV
Header: Yes

We will create a dataset named:

DS_Sales_Source

The destination dataset will be:

DS_Sales_Destination

Its planned output will be:

Container: destination
Folder: day92_test
File: sales_copy.csv
Format: CSV
Header: Yes
Remember the difference
Component	Purpose	Example
Linked Service	Defines the connection	Connect to datalakegyan
Dataset	Identifies the file and format	source/Sales.csv
Activity	Performs the operation	Copy the CSV file
Pipeline	Groups and orchestrates activities	Sales ingestion workflow

Important: A dataset does not copy data by itself. The Copy Activity on Day 93 will perform the copy.

3. Understand Authentication Before Connecting

Your Databricks environment already has a managed identity configuration. However, Azure Data Factory has its own identity. Its permissions do not automatically come from your Databricks Access Connector.

For our learning exercise, we'll use the system-assigned managed identity of your Data Factory. Managed identity authentication lets ADF access supported Azure services without requiring you to store a storage account key in the linked service.

Step 1: Find your Data Factory identity
Open the Azure portal.
Search for Data factories.
Open your Data Factory.
Open its Properties or Managed identity section, depending on the portal interface.
Check whether its system-assigned managed identity is enabled.

If it isn't enabled, enable it and save the change.

Your Data Factory now has its own identity in Microsoft Entra ID.

Step 2: Give that identity access to ADLS Gen2

ADF needs permission to read the source file and write to the destination.

Open your storage account:

datalakegyan
    |
    v
Containers
    |
    +-- source
    |
    +-- destination
Source permissions
Open the source container.
Open Access Control (IAM).
Select Add → Add role assignment.
Choose Storage Blob Data Reader.
Select your Data Factory's system-assigned managed identity.
Complete the role assignment.
Destination permissions

Repeat these steps for the destination container, but select:

Storage Blob Data Contributor

This role permits the identity to read and write data in the assigned scope. Assigning permissions at the individual container scope limits access more narrowly than assigning them across the entire storage account.

Your permissions should look like this:

Container	Identity	Role
source	Data Factory managed identity	Storage Blob Data Reader
destination	Data Factory managed identity	Storage Blob Data Contributor

Do not change your existing Databricks permissions. These assignments are for ADF.

4. Practical Notebook 1 — Create the ADLS Gen2 Linked Service

This is a UI configuration exercise, not a Python notebook.

Step 1: Open ADF Studio

Open your Data Factory in the Azure portal and select Launch Studio.

Step 2: Open Manage

In ADF Studio, select Manage, then locate Linked services.

Select:

+ New
Step 3: Select the connector

Search for:

Azure Data Lake Storage Gen2

Select the connector and continue.

Step 4: Configure the linked service

Use these settings:

Field	Value
Name	LS_ADLS_Gen2
Authentication type	System-assigned managed identity
URL	https://datalakegyan.dfs.core.windows.net
Integration Runtime	Azure AutoResolveIntegrationRuntime, or the default Azure IR

The exact UI labels may differ slightly.

Why use the storage account URL rather than the full file path?

The linked service connects to the storage account. The datasets will identify the specific containers, folders, and files.

The ADLS Gen2 connector supports managed identity authentication and the account URL format used above.

Step 5: Test the connection

Select Test connection if available.

If it succeeds, create the linked service.

If it fails, check the authentication type, managed identity permissions, storage networking restrictions, and the connection details.

Some configurations allow you to test a specific file path rather than the entire storage account.

Expected result

You should see:

LS_ADLS_Gen2
Status: Created

The precise status display varies by interface.

5. Practical Notebook 2 — Create the Source Dataset

Now we will tell ADF which file to read.

Step 1: Open Author

In ADF Studio:

Select Author.
Select the + button.
Select Dataset.
Step 2: Choose the format

Search for and select:

Azure Data Lake Storage Gen2

Choose the DelimitedText format because your input file is a CSV file.

Select Continue.

Step 3: Configure the dataset

Use these values:

Field	Value
Name	DS_Sales_Source
Linked service	LS_ADLS_Gen2
File system	source
Directory	Leave blank
File	Sales.csv
First row as header	Checked

Depending on the interface, the container field may be called File system.

The CSV dataset format and file location are defined separately from the linked service connection.

Step 4: Verify the path

Your source dataset should identify:

abfss://source@datalakegyan.dfs.core.windows.net/Sales.csv

This is the same existing Sales file you have been using in Databricks.

Step 5: Save

Select OK or Finish, as presented by the interface.

If ADF offers an import-schema option, you can import the CSV schema to inspect the columns. For today's exercise, this is optional.

Expected result
Dataset: DS_Sales_Source

Linked Service: LS_ADLS_Gen2
Container: source
File: Sales.csv
Format: DelimitedText
First row as header: Yes

Do not select any overwrite option or run a copy operation today. We are only defining the source dataset.

6. Practical Notebook 3 — Create the Destination Dataset

The destination dataset describes where the copied CSV will be written.

We will use a separate practice folder so we do not overwrite your existing files.

Step 1: Create another dataset

Go to:

Author → + → Dataset

Choose:

Azure Data Lake Storage Gen2
    |
    v
DelimitedText
Step 2: Configure the dataset

Enter these values:

Field	Value
Name	DS_Sales_Destination
Linked service	LS_ADLS_Gen2
File system	destination
Directory	day92_test
File	sales_copy.csv
First row as header	Checked

Save the dataset.

Depending on your ADF configuration, the destination directory may be created by a later copy operation if it doesn't exist.

Expected result
Dataset: DS_Sales_Destination

Linked Service: LS_ADLS_Gen2
Container: destination
Directory: day92_test
File: sales_copy.csv
Format: DelimitedText
First row as header: Yes

The planned destination path is:

abfss://destination@datalakegyan.dfs.core.windows.net/day92_test/sales_copy.csv

The file will not exist just because you created the dataset. It will be written when we configure and run Copy Activity.

7. Check Your ADF Configuration

At this point, your configuration should contain three objects:

ADF Studio
    |
    +-- Linked Services
    |      |
    |      +-- LS_ADLS_Gen2
    |
    +-- Datasets
           |
           +-- DS_Sales_Source
           |
           +-- DS_Sales_Destination

Check each one.

Check	Expected result
Linked service exists	LS_ADLS_Gen2
Source dataset exists	DS_Sales_Source
Destination dataset exists	DS_Sales_Destination
Source file configured	source/Sales.csv
Destination configured	destination/day92_test/sales_copy.csv
Source access	Reader permission for ADF identity
Destination access	Contributor permission for ADF identity

You can also open the datasets to confirm that they reference the correct linked service.

If your account does not permit you to create role assignments, you may need an Azure administrator to grant the permissions.

8. Common Errors and Solutions
Error 1: Authentication failed

Possible cause: The linked service uses a managed identity that does not have the necessary storage access.

Solution: Verify that you selected the correct Data Factory identity and assigned the required data-plane roles to it.

Remember, your Databricks managed identity and ADF's system-assigned identity are not automatically interchangeable.

Error 2: The linked service connection test fails

Possible causes:

Incorrect storage account URL.
Incorrect authentication selection.
Missing permissions.
Storage account firewall or network restrictions.

Solution: Check the URL, identity, permissions, and networking configuration. If a normal connection test fails, testing against a specific permitted path may help isolate the issue.

Error 3: The source file cannot be found

Possible cause: The dataset points to the wrong container or filename.

Solution: Verify the following:

Container: source
File: Sales.csv

The filename must match the actual object in storage.

Error 4: ADF can read the source but cannot write to the destination

Possible cause: The managed identity has read access but lacks destination write permissions.

Solution: Check that it has Storage Blob Data Contributor at the intended destination scope.

Error 5: The destination file doesn't exist

Possible cause: Only the dataset was created.

Solution: This is expected. Day 92 defines the destination; Day 93 will create and execute the Copy Activity.

9. Day 92 Interview Questions
Q1. What is a linked service in ADF?

A linked service defines connection and authentication information for a data store or compute service.

Q2. What is a dataset in ADF?

A dataset identifies the data that an activity uses, such as a CSV file, table, folder, or other supported data resource.

Q3. Can multiple datasets use the same linked service?

Yes. For example, source and destination datasets can both use LS_ADLS_Gen2 when they access the same storage account.

Q4. Why are we using one linked service for both datasets?

Both the source and destination containers belong to the same storage account. Reusing the connection reduces duplicate configuration.

The same linked service can be reused while datasets specify different containers and paths.

Q5. What is managed identity?

Managed identity gives an Azure service an identity that can authenticate to supported services without requiring you to store its credentials in your application or linked service.

Q6. Does ADF automatically inherit Databricks permissions?

No. ADF and Databricks identities have separate permissions unless an identity is explicitly shared and appropriately configured. In today's exercise, we grant access to ADF's identity.

Q7. What is the difference between a dataset and Copy Activity?

A dataset describes the data location and format. Copy Activity performs the data movement.

Q8. Why do we select the DelimitedText format?

Because Sales.csv contains comma-separated text records that ADF should interpret using the CSV format.

Q9. What happens if the source dataset points to the wrong file?

The activity may fail because the file cannot be found, or it may process the wrong file if the configured path exists. Always verify the path before execution.

Q10. Is creating a destination dataset enough to create the destination file?

No. Creating the dataset only defines the destination configuration. A data movement activity must write the file.

10. Twisted Interview Scenarios
Scenario 1: The source and destination are in different storage accounts. Can you use the same linked service?

Not ordinarily for the same source-to-sink configuration. Each account generally needs its own appropriate connection, so you would create separate linked services and reference them through the respective datasets.

Scenario 2: The source and destination are in different containers but the same storage account. Do you need two linked services?

Not necessarily. One storage account linked service can be reused by both datasets, provided its authentication and permissions allow the intended operations.

Scenario 3: The linked service test succeeds, but Copy Activity fails.

A successful connection test does not validate every part of the pipeline. Inspect the activity error, source and sink paths, data permissions, file format, and the configuration of the actual operation.

Scenario 4: Why give the identity Reader access to the source and Contributor access to the destination?

It follows the principle of least privilege: give the identity the permissions needed for each operation, rather than unrestricted access everywhere.

Scenario 5: Why not hardcode the complete file path directly into every pipeline?

Reusable linked services and datasets make configurations easier to maintain. Later, parameters can make the same pipeline work with different files, folders, or environments.

11. Day 92 Completion Checklist

Before moving to Day 93, verify:

 LS_ADLS_Gen2 exists.
 The linked service uses the correct authentication method.
 ADF's identity has appropriate source and destination permissions.
 DS_Sales_Source points to source/Sales.csv.
 DS_Sales_Destination points to destination/day92_test/sales_copy.csv.
 Both datasets use the correct linked service.
 You understand why a dataset does not copy data.
 You can explain linked services, datasets, and managed identity in an interview.