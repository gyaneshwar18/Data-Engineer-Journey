# Day 68 — Databricks Fundamentals

## 1. What is Databricks?

Databricks is a cloud-based data and AI platform built around Apache Spark.

It provides a managed environment where we can:

- Write and run PySpark/SQL code
- Process large datasets
- Create notebooks
- Run Spark workloads
- Work with Delta Lake
- Build data pipelines
- Schedule and monitor jobs

### Simple definition

> Databricks is a cloud platform that provides a managed environment for running Apache Spark and building data engineering pipelines.

---

# 2. Why do we need Databricks?

Apache Spark is a powerful distributed data processing engine, but setting up and managing Spark manually can require:

- Java
- Spark
- Cluster configuration
- Worker machines
- Networking
- Resource management

Databricks provides a managed environment around Spark.

### Without Databricks

```text
Developer
    ↓
Install Java
    ↓
Install Spark
    ↓
Configure Spark
    ↓
Configure Cluster
    ↓
Manage Resources
    ↓
Run Spark