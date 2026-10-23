Day 84 — Databricks Streaming

90-Day Data Engineering Journey | Concepts + Interview Preparation

1. Concepts
1.1 What is Structured Streaming?

Structured Streaming is a Spark feature that processes data continuously or incrementally as new data becomes available.

In your notebook, you're using Structured Streaming to read data through Auto Loader and write it to Delta Lake.

1.2 How does your streaming pipeline work?
ADLS Gen2
    |
    | Parquet files
    v
Auto Loader
    |
    | Streaming DataFrame
    v
Structured Streaming
    |
    | Micro-batches
    v
Delta Lake
    |
    v
ADLS Gen2 /data
1.3 What is readStream?

readStream creates a streaming DataFrame rather than a regular batch DataFrame.

Your notebook uses Auto Loader as the source to discover and read Parquet files.

1.4 What is writeStream?

writeStream starts a streaming write operation that continuously processes available data according to the configured trigger and writes it to a destination.

In your notebook, the destination is Delta Lake.

1.5 What is a Trigger?

A trigger determines when Spark processes the data in a streaming query.

Your notebook uses a processing-time trigger of five seconds.

This requests a new micro-batch at five-second intervals, subject to the time required to process each batch.

1.6 What is a Checkpoint?

A checkpoint stores streaming progress and state information needed to resume processing.

Your streaming write uses a checkpointLocation in ADLS Gen2.

The checkpoint helps Spark track which data has been processed.

1.7 What is a Streaming Sink?

A sink is the destination where streaming results are written.

Your notebook uses Delta Lake as the sink, so processed data is written in Delta format.

1.8 What is mergeSchema?

Your notebook uses mergeSchema = true when writing to Delta.

This enables supported schema evolution during writes, allowing compatible new columns to be incorporated into the Delta table schema.

Schema evolution is not the same as automatic data-quality validation.

2. Interview Questions and Answers
Q1. What is Structured Streaming?

Structured Streaming is Spark's processing engine for incrementally processing streaming data using the DataFrame and SQL APIs.

Q2. What is the difference between read and readStream?

read creates a batch DataFrame from available data. readStream creates a streaming DataFrame that can process data incrementally as it becomes available.

Q3. What is the difference between write and writeStream?

write performs a batch write. writeStream starts a streaming write query that processes incoming data according to its configured trigger.

Q4. What is a trigger in Spark Structured Streaming?

A trigger controls when Spark starts processing available data in a streaming query.

Q5. What is the purpose of processingTime = '5 seconds'?

It requests processing in micro-batches at five-second intervals. It does not guarantee that every batch will finish within five seconds.

Q6. What is a checkpoint in streaming?

A checkpoint stores progress and state information that Spark uses to resume a streaming query and manage previously processed input.

Q7. What happens if a streaming job stops unexpectedly?

With a correctly configured and available checkpoint, the query can generally resume from its recorded progress when restarted with the same query configuration.

Q8. What is a streaming sink?

A sink is the destination where streaming results are written. In your notebook, Delta Lake is the sink.

Q9. What is the difference between a micro-batch and continuous processing?

Micro-batch processing groups incoming data into small batches. Continuous processing is a different execution mode designed for lower latency, with different support and guarantees. Your notebook uses micro-batch processing.

Q10. Does a five-second trigger mean the pipeline always has five-second end-to-end latency?

No. Data discovery, scheduling, processing time, and the workload affect end-to-end latency.

Twisted Questions

Q11. If a stream uses a checkpoint, will it automatically run again after the Databricks compute is permanently stopped?

No. A checkpoint preserves progress, but it does not independently restart a stopped query. The streaming job or notebook must be started again.

Q12. Can two streaming queries safely share the same checkpoint directory?

No. Each independent streaming query should use its own checkpoint location to prevent conflicting progress and state information.

Q13. Does mergeSchema = true guarantee that every incoming record is valid?

No. It supports schema evolution, not complete data-quality validation. Invalid values and business-rule violations still require validation.

Q14. If there are no new files, will the streaming query necessarily terminate?

No. A streaming query can remain active and wait for additional data, depending on its trigger and configuration.

Day 85 — Incremental Data Ingestion with Auto Loader

Concepts + Interview Preparation

1. Concepts
1.1 What is Incremental Data Ingestion?

Incremental ingestion processes newly available data instead of repeatedly processing the entire source dataset.

For example, suppose a company receives new Parquet files in ADLS Gen2 every day.

Rather than reloading all previously processed files, the pipeline discovers and processes new files as they arrive.

1.2 What is Auto Loader?

Auto Loader is a Databricks capability for incrementally discovering and ingesting files from cloud storage.

It supports storage systems such as Azure Data Lake Storage Gen2 and file formats such as Parquet.

Your notebook uses Auto Loader to read Parquet files from the alsource container.

1.3 What is cloudFiles?

cloudFiles is the source format used to configure Auto Loader.

It enables incremental file discovery and ingestion through Structured Streaming.

1.4 What is cloudFiles.format?

This option specifies the format of the incoming files.

Your notebook specifies Parquet, so Auto Loader interprets the incoming files as Parquet data.

1.5 What is cloudFiles.schemaLocation?

It specifies where Auto Loader stores schema information and tracks schema evolution.

This is important when new files arrive or the source schema changes.

1.6 How does Auto Loader avoid unnecessary reprocessing?

Auto Loader works with Structured Streaming checkpoints to track ingestion progress and manage the processing of discovered files.

When a query restarts with the same valid checkpoint, previously processed files generally aren't processed again as new input.

1.7 How does your pipeline work?
ADLS Gen2 / alsource
          |
          | New Parquet files
          v
      Auto Loader
          |
          | Schema tracking
          | Incremental discovery
          v
  Streaming DataFrame
          |
          | Checkpointed processing
          v
       Delta Lake
          |
          v
ADLS Gen2 / aldestination/data

Important distinction: The Auto Loader schema location stores schema information, whereas the Structured Streaming checkpoint tracks query progress and state. These serve different purposes and should use separate directories.

1.8 What is the purpose of incremental ingestion?

It helps build pipelines that process newly arriving data without repeatedly reprocessing all previous input.

This can reduce unnecessary processing and supports scalable ingestion pipelines.

2. Interview Questions and Answers
Q1. What is Auto Loader?

Auto Loader is a Databricks feature that incrementally discovers and processes new files arriving in cloud storage.

Q2. Why do we use Auto Loader instead of reading files using spark.read?

A regular spark.read operation reads data in batch mode. Auto Loader supports incremental file discovery and ingestion, making it useful when new files arrive continuously or regularly.

Q3. What is cloudFiles?

cloudFiles is the source format that configures Auto Loader in a Structured Streaming query.

Q4. What is the purpose of cloudFiles.format = 'parquet'?

It tells Auto Loader that the incoming files are in Parquet format.

Q5. What is the difference between schemaLocation and checkpointLocation?
schemaLocation	checkpointLocation
Stores schema information	Stores streaming progress and state
Supports schema evolution	Supports query recovery and progress tracking
Used by Auto Loader	Used by Structured Streaming

They should be configured separately.

Q6. Does Auto Loader automatically write data into Delta Lake?

No. Auto Loader reads the incoming data. The streaming write operation determines where and how it is stored. Your notebook writes the processed data to Delta Lake.

Q7. What happens when new Parquet files arrive in the source container?

Auto Loader can discover and process them incrementally according to the stream's configuration and available processing opportunities.

Q8. Can Auto Loader handle schema changes?

Yes. It supports schema evolution through configuration options. The behavior when a new column arrives depends on the configured schema evolution mode.

Q9. Why do we use a checkpoint with Auto Loader?

The checkpoint helps Structured Streaming track progress, allowing the pipeline to resume from recorded progress after a restart.

Q10. What is the difference between full and incremental ingestion?

Full ingestion processes the entire selected dataset. Incremental ingestion processes newly available or changed data according to the pipeline's design.

3. Twisted and Scenario-Based Questions
Q11. A new Parquet file arrives, but your pipeline doesn't process it. What would you investigate?

I would check whether the streaming query is running, whether the file is in the configured source location, whether the identity has access, and whether the checkpoint and Auto Loader configuration are correct.

Q12. If you delete the checkpoint, will Auto Loader necessarily resume from its previous position?

No. Deleting the checkpoint removes the stored progress information. Restarting without it can cause previously processed files to be processed again, depending on the stream configuration.

Q13. Why shouldn't we use the same location for schema tracking and streaming checkpoints?

They store different types of metadata. Separate paths keep schema-management information independent of the streaming query's progress and state.

Q14. Does incremental ingestion guarantee that duplicate business records will never appear?

No. Auto Loader tracks file processing, but it does not automatically guarantee uniqueness of individual business records. Duplicate records within different input files may still occur. Deduplication or other data-quality logic may be required.

Q15. What happens if a new column appears in an incoming Parquet file?

Auto Loader's schema evolution behavior depends on its configuration. It can detect and accommodate supported schema changes, but some configurations may stop the stream until it is restarted.

Q16. What is the difference between Auto Loader and COPY INTO?

Auto Loader is designed for incremental file ingestion through Structured Streaming, with checkpointing and schema evolution capabilities. COPY INTO is a SQL-based incremental ingestion command that tracks files already loaded and is useful for supported batch-oriented ingestion workflows.

Q17. Does mergeSchema = true mean Auto Loader can automatically fix incompatible data types?

No. Schema evolution can incorporate supported schema changes, but it doesn't automatically resolve every incompatible type change or invalid record.

Q18. Explain your Day 85 implementation in an interview.

"I configured Auto Loader to read Parquet files from ADLS Gen2 using the cloudFiles source. I configured schema tracking and used Structured Streaming to write the incoming data to Delta Lake, with a checkpoint to track stream progress. I also configured a five-second processing-time trigger and enabled supported schema evolution on the Delta write."

Day 84 and Day 85 — Quick Revision
Topic	Day 84: Databricks Streaming	Day 85: Incremental Ingestion
Main focus	Streaming data processing	Discovering and processing new files
Key technology	Structured Streaming	Auto Loader + Structured Streaming
Source in your implementation	Auto Loader streaming DataFrame	Parquet files in ADLS Gen2
Destination	Delta Lake	Delta Lake
Trigger	Five-second processing-time trigger	Uses the streaming query configuration
Checkpoint	Tracks streaming progress	Tracks ingestion progress
Schema handling	Delta schema evolution	Auto Loader schema tracking and supported evolution