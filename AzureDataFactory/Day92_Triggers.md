Day 98 — Azure Data Factory: Triggers and Scheduling
Data Engineering Journey | Practical Hands-on

Today's goal: Learn how to run your ADF pipelines automatically without manually selecting Debug or Trigger Now every time.

We'll cover three important trigger types, configure a schedule trigger, and learn how to monitor automated executions.

We will continue using your existing ADLS Gen2 setup and Sales.csv.

1. What Is a Trigger in ADF?

A trigger determines when an Azure Data Factory pipeline should execute.

Without a trigger, you can manually run a pipeline whenever you need it.

With a trigger, ADF can automatically start a pipeline based on a schedule or an event.

Without a trigger
You
 |
 v
Open ADF Studio
 |
 v
Select Pipeline
 |
 v
Click Debug or Trigger Now
 |
 v
Pipeline Executes
With a trigger
         Trigger
            |
            v
     Pipeline Executes
            |
            v
      Copy Sales.csv
            |
            v
      ADLS Gen2

For example, suppose your company receives sales data every day at 6 AM.

Instead of starting the pipeline manually, you configure ADF to execute it automatically every day.

Interview answer

A trigger in Azure Data Factory defines when a pipeline should execute. It can run a pipeline on a schedule, at a specified time interval, or in response to an event such as a file arriving in Azure Storage.

2. Understand the Three Main Trigger Types

ADF supports three main types of triggers: Schedule, Tumbling Window, and Event-based.

Type 1: Schedule Trigger

A Schedule Trigger executes a pipeline at specified times.

Examples:

Every day at 6 AM.
Every hour.
Every Monday at 9 AM.
Every 15 minutes.
Architecture
Schedule Trigger
       |
       | Every day at 6 AM
       v
ADF Pipeline
       |
       v
Copy Sales.csv
       |
       v
ADLS Gen2

Real-world example: A company copies daily sales data from a source location to a data lake every morning.

Today's practical exercise will use this trigger.

Type 2: Event-Based Trigger

An Event-Based Trigger executes a pipeline when a configured event occurs.

For example, a file is uploaded to an Azure Data Lake Storage Gen2 container.

New File Arrives
       |
       v
Azure Event Grid
       |
       v
ADF Event Trigger
       |
       v
ADF Pipeline
       |
       v
Process the File

This is useful when you want to process data as it arrives rather than wait for a scheduled time.

ADF storage event triggers support Azure Data Lake Storage Gen2 and can react to events such as file creation or deletion.

Important: An existing file does not automatically trigger a pipeline simply because you configure the trigger afterward. A relevant event must occur.

Type 3: Tumbling Window Trigger

A Tumbling Window Trigger executes a pipeline over fixed, continuous, non-overlapping time intervals and maintains state for those intervals.

Example:

Window 1: 06:00–07:00
Window 2: 07:00–08:00
Window 3: 08:00–09:00

It is useful for time-based data processing when tracking individual windows, managing dependencies, or rerunning failed windows matters.

Unlike a Schedule Trigger, a Tumbling Window Trigger supports stateful window processing and backfilling previous windows.

Comparison
Feature	Schedule Trigger	Event-Based Trigger	Tumbling Window Trigger
Starts when	Scheduled time arrives	Configured event occurs	A defined time window becomes due
Example	Daily at 6 AM	New file arrives	Process each hourly window
Maintains window state	No	No	Yes
Responds to file arrival	No, not by itself	Yes, when configured for that event	No, not by itself
Best use	Regular batch jobs	Event-driven ingestion	Stateful, time-window processing

For now, focus on Schedule Triggers. You will learn event-based processing in more detail as your pipelines become more advanced.

3. Understand Trigger Now vs Debug vs Schedule

These three options serve different purposes.

Option	Purpose
Debug	Test the current draft pipeline
Trigger Now	Start an immediate, on-demand pipeline run
Schedule Trigger	Start the pipeline automatically at configured times

Example:

You have a pipeline called PL_Sales_Copy.

Debug: Test your draft configuration.

Trigger Now: Execute the pipeline immediately.

Schedule Trigger: Execute the pipeline automatically every day at a configured time.

ADF supports manual, scheduled, tumbling-window, and event-based pipeline execution.

4. Practical Exercise — Prepare Your Pipeline

We'll use your parameterized pipeline from Day 94 if you created it.

Pipeline
PL_Sales_Copy_Parameterized
Parameters
Parameter	Value for this exercise
pSourceFileName	Sales.csv
pDestinationFileName	sales_copy_day98.csv

The source is your existing file:

abfss://source@datalakegyan.dfs.core.windows.net/Sales.csv

For the destination, use a dedicated practice output so your original input file and existing Delta tables remain untouched.

If your Day 94 parameterized pipeline is not available, use your existing Copy Activity pipeline and verify its destination settings before attaching a trigger.

Safety note: A scheduled trigger can execute repeatedly. Use only a practice destination whose contents are safe to replace.

5. Practical Notebook — Create a Schedule Trigger

This is a UI-based exercise in ADF Studio.

Step 1: Open ADF Studio
Open the Azure portal.
Open your existing Data Factory.
Select Launch Studio.
Go to Author.
Open PL_Sales_Copy_Parameterized.
Step 2: Open the trigger menu

In the pipeline editor, select:

Trigger → New/Edit

Then select:

Choose trigger → + New

Select Schedule as the trigger type. These are the standard steps for creating a schedule trigger in ADF Studio.

Step 3: Configure the trigger

Use the following configuration.

Setting	Value
Name	TR_Daily_Sales_Copy_Day98
Type	Schedule
Time zone	India Standard Time
Recurrence	Daily
Start time	Choose a suitable future time
End time	Optional
Activated	Yes

Choose a start time that is still in the future after you finish configuring the trigger. Give yourself enough time to save and publish your changes.

For the first test, do not enable an unnecessarily frequent schedule. A daily schedule is easier to control.

Microsoft's documentation specifies that the trigger's time zone applies to the start time, end time, and scheduling options. The start time must also be set appropriately for the selected recurrence.

What does Daily mean?

If you select a daily recurrence at 6 AM, the pipeline will be scheduled to execute each day at that time.

The trigger will not start running merely because you save it.

Step 4: Associate the pipeline

Make sure TR_Daily_Sales_Copy_Day98 is associated with:

PL_Sales_Copy_Parameterized

If ADF displays pipeline parameters in the association dialog, use:

Parameter	Value
pSourceFileName	Sales.csv
pDestinationFileName	sales_copy_day98.csv

This tells the trigger which values to pass to the pipeline when it executes.

If you are using a non-parameterized pipeline, you can skip this parameter mapping.

Step 5: Save the trigger

Select OK and confirm the trigger configuration.

Next, select Publish All.

Important: A trigger created in the authoring interface does not begin executing until the changes are published.

Your configuration should now resemble:

TR_Daily_Sales_Copy_Day98
              |
              | Daily schedule
              v
PL_Sales_Copy_Parameterized
              |
              v
       Copy_Sales_CSV
              |
              v
       ADLS Gen2 Output
6. Practical Exercise — Monitor the Scheduled Run

After publishing, ADF will wait for the configured schedule.

Step 1: Open Monitor

In ADF Studio, select Monitor.

Step 2: Check Pipeline Runs

Open Pipeline runs and refresh the list.

When the scheduled time arrives, look for a new run corresponding to your pipeline.

Inspect its status.

Status	Meaning
Queued or In progress	The pipeline is waiting or executing
Succeeded	The pipeline execution completed successfully
Failed	The pipeline or an activity failed

The available status labels and their presentation may vary slightly.

Step 3: Inspect the trigger

Open Trigger runs and inspect the schedule trigger's execution history.

The Pipeline runs view shows pipeline executions, while the Trigger runs view helps you inspect trigger executions.

Step 4: Verify the output

If the pipeline succeeded, inspect your destination container.

Expected practice output:

destination/
    day92_test/
        sales_copy_day98.csv

Use the exact folder and filename configured in your destination dataset.

Step 5: Stop the trigger after testing

After you confirm that the scheduled run works, stop or deactivate the trigger if you do not intend to keep it running.

This prevents unnecessary recurring pipeline executions and associated costs.

If you want the pipeline to continue running daily, leave the trigger active and ensure the destination and pipeline are safe for repeated execution.

7. Event-Based Trigger — Understand the Configuration

We will not create another live trigger today, because your existing Sales.csv is already present and configuring an event trigger does not cause that existing file to be processed retroactively.

However, you should understand the configuration.

Suppose you want a pipeline to start whenever a new CSV file is uploaded to the source container.

The conceptual setup is:

Storage Account: datalakegyan
Container: source
Event: Blob created
       |
       v
Event-Based Trigger
       |
       v
ADF Pipeline

At a high level, the configuration requires you to:

Open the pipeline in ADF Studio.
Select Trigger → New/Edit.
Create a trigger of type Storage events.
Select the storage account and container.
Configure the relevant event and path filters.
Associate the trigger with a pipeline.
Publish the changes.

Storage event triggers require an appropriate Azure Storage and Event Grid configuration, including the required permissions to create the event subscription.

When is this useful?

For example, a company receives a new sales file every morning, but the upload time varies.

A Schedule Trigger might start at 6 AM even when the file has not arrived yet.

An Event-Based Trigger can respond when the file actually arrives, making it more appropriate for arrival-driven ingestion.

Remember: Schedule means when the clock says. Event-based means when the configured event occurs.

8. Important Real-World Scenarios
Scenario 1: A company needs to copy data every day at 2 AM.

Use a Schedule Trigger.

Scenario 2: A pipeline should begin processing whenever a new file arrives in ADLS Gen2.

Use an Event-Based Trigger configured for the appropriate storage event.

Scenario 3: A pipeline processes one hour of data per execution and needs to track and rerun individual windows.

Consider a Tumbling Window Trigger.

Scenario 4: Your scheduled pipeline is not executing.

Check:

Whether the trigger is activated.
Whether the changes were published.
Whether the start time and time zone are correct.
Whether the configured recurrence is appropriate.
Whether the trigger is associated with the correct pipeline.
Scenario 5: The trigger executes, but the pipeline fails.

Inspect the Pipeline runs and activity run details to identify the actual failure. The trigger may have started correctly even though an activity inside the pipeline failed.

Scenario 6: The pipeline executes twice.

Check whether multiple active triggers are associated with the same pipeline, whether you manually started an additional run, and whether the configured schedule could explain the second execution.

9. Day 98 Interview Questions and Answers

Q1. What is a trigger in ADF?

A trigger determines when an ADF pipeline executes, either according to a schedule or in response to an event.

Q2. What are the three main trigger types in ADF?

Schedule Trigger, Tumbling Window Trigger, and Event-Based Trigger.

Q3. What is the difference between Debug and Trigger Now?

Debug tests a draft pipeline. Trigger Now starts an immediate on-demand pipeline execution.

Q4. What is a Schedule Trigger?

A Schedule Trigger executes a pipeline at configured times, such as hourly, daily, or weekly.

Q5. What is an Event-Based Trigger?

An Event-Based Trigger starts a pipeline in response to a configured event, such as a file being created or deleted in supported Azure Storage.

Q6. What is a Tumbling Window Trigger?

It executes a pipeline over fixed, contiguous time windows and retains state about those windows. It is useful when window dependencies and reruns matter.

Q7. Why must you publish changes after creating a trigger?

Publishing makes the configured changes available to the published Data Factory environment. A saved but unpublished schedule trigger will not start its scheduled executions.

Q8. How do you monitor a scheduled pipeline?

Use Monitor to inspect pipeline runs and trigger runs. Check activity details to troubleshoot failures.

Q9. Can one schedule trigger execute multiple pipelines?

Yes. A trigger can reference multiple pipelines, and a pipeline can be started by multiple triggers. Tumbling Window Triggers have a one-to-one relationship with pipelines.

Q10. What happens if a scheduled pipeline fails?

The pipeline run is marked as failed, and you should investigate the failure. Retry behavior depends on the pipeline activities and retry settings; a schedule trigger does not automatically guarantee that the failed business processing will be recovered.

10. Twisted Interview Questions
Scenario 1: Your trigger is activated, but the pipeline does not run. What will you check?

I would verify that the configuration was published, that the start time and time zone are correct, that the trigger is associated with the intended pipeline, and that the next scheduled time has actually arrived.

Scenario 2: A file arrives at 8:15 AM, but your Schedule Trigger runs at 8 AM. What is the problem?

The pipeline can execute before the file arrives. If processing must start in response to file arrival, I would consider a suitable Event-Based Trigger or add validation and retry logic.

Scenario 3: A schedule trigger runs successfully, but its pipeline activity fails. Does that mean the data processing succeeded?

No. You must inspect the pipeline and activity results. Trigger execution and successful completion of the intended data-processing workflow are different things.

Scenario 4: You need to process every hourly window and reprocess a failed window. Which trigger would you consider?

A Tumbling Window Trigger, because it maintains state for fixed windows and supports window-oriented recovery scenarios.

Scenario 5: Why shouldn't you leave a learning pipeline scheduled every minute?

It can create unnecessary executions and associated costs. Start with the minimum frequency required for the exercise, monitor the results, and stop the trigger when you have finished testing.

11. Day 98 Completion Checklist
 Understand the purpose of triggers.
 Understand Schedule, Event-Based, and Tumbling Window Triggers.
 Understand the difference between Debug, Trigger Now, and Schedule Trigger.
 Created a schedule trigger or completed its configuration.
 Associated it with the intended pipeline.
 Published the trigger configuration.
 Checked Pipeline runs and Trigger runs.
 Verified the destination after a successful run.
 Stopped the trigger after testing if continued execution is not needed.
 Can explain when to use each trigger type in an interview.