# Data Ingestion Smoke Test

This project is a small, realistic smoke test for a beginner-friendly data engineering workflow in AWS.

The goal is **not** to build a full production pipeline yet.

The goal is to prove that the core path works:

**GitHub Codespaces → Python app → Docker image → ECR → ECS Fargate → EventBridge Scheduler → S3 Parquet → Athena**

---

## What this project does

Each time the app runs, it:

1. generates a small synthetic clickstream-style dataset
2. checks that the dataset has the columns we expect
3. writes the data to a local Parquet file
4. uploads that file to S3
5. makes the data queryable in Athena

The dataset is fake, but it is designed to feel realistic enough to practice with.

It includes:

- customer IDs
- entry pages
- page views
- product views
- conversion probability
- converted flag

The conversion logic includes randomness, but it is still influenced by the inputs so the data feels a little more like real user behavior.

---

## Why this project exists

This project is meant to help validate the basic building blocks of a data engineering workflow in AWS without jumping straight into a big system.

It answers questions like:

- Can I build and run the code in GitHub Codespaces?
- Can I organize the app like a real Python project?
- Can I package it into Docker?
- Can AWS run it as a scheduled ECS task?
- Can it write Parquet to S3?
- Can Athena query the output?

In plain English, this is a “make sure the plumbing works” project.

---

## Who this is for

This is a good starter project for someone learning how data engineering apps are often structured.

It is especially useful if you want practice with:

- Python project structure
- synthetic dataset generation
- schema checks
- Parquet files
- S3 uploads
- Docker packaging
- ECS scheduled tasks
- Athena querying

It is intentionally small enough to understand without getting overwhelmed.

---

## What is intentionally out of scope

This project is **not** trying to do everything.

It does **not** yet include:

- real source system ingestion
- advanced orchestration beyond a simple schedule
- production-grade retries and alerting
- infrastructure-as-code
- full CI/CD
- production-grade monitoring and observability

Those are all reasonable future steps, but they are not the purpose of this smoke test.

---

## Project structure

```text
clickstream-smoke-test/
├── src/
│   └── clickstream_smoke_test/
│       ├── __init__.py
│       ├── config.py
│       ├── generator.py
│       ├── schema.py
│       ├── s3_writer.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_generator.py
│   ├── test_schema.py
│   └── test_s3_writer.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```

---

## What each file is for

### `main.py`
This is the entrypoint.

It is the file you run when you want the app to do its job.

It mainly coordinates the other modules.

### `config.py`
Loads runtime settings from environment variables and `.env`.

Examples:
- AWS region
- S3 bucket
- S3 prefix
- row count
- source name
- max runtime minutes

### `generator.py`
Creates the synthetic clickstream dataset.

This is where the fake daily data is generated.

### `schema.py`
Defines what columns the dataset is supposed to have and checks that they are present.

### `s3_writer.py`
Handles:
- local Parquet writing
- S3 key creation
- S3 upload

### `utils.py`
Small helper functions, mainly around UTC timestamps and dates.

### `tests/`
Contains local tests to make sure the project behaves the way we expect.

---

## Dataset shape

Each run generates rows with these columns:

- `run_date`
- `utc_timestamp`
- `customer_id`
- `entry_page`
- `page_views`
- `product_views`
- `conversion_probability`
- `converted`
- `source`

### Notes on realism

- `Homepage` is lower intent
- `Deals` is medium intent
- `Product` is higher intent
- more page views help a little
- more product views help more
- randomness is included on purpose
- conversion probability is capped at `5%`

So the data is fake, but not just random nonsense.

---

# Full prerequisites

## 1. GitHub / Codespaces prerequisites

Before running this project, you should have:

- a GitHub repository for the project
- GitHub Codespaces enabled for your account/repo
- a Codespace opened for the repo
- Python available in the Codespace
- Docker available in the Codespace
- internet access from the Codespace to AWS

You do **not** need Docker installed on your local laptop if you are building and running everything inside Codespaces.

---

## 2. AWS account prerequisites

You should have:

- an AWS account
- access to the AWS Console
- permission to create and manage:
  - IAM users, roles, and policies
  - S3 buckets
  - ECR repositories
  - ECS clusters and task definitions
  - EventBridge Scheduler schedules
  - Athena databases and tables
  - CloudWatch log groups
  - CloudFormation stacks if ECS leaves behind failed infrastructure scaffolding

---

## 3. Region prerequisite

Pick a single AWS region and use it consistently.

Example:

```text
us-east-1
```

---

## 4. S3 prerequisite

Create a bucket for the output dataset.

Use your own bucket name, for example:

```text
<your-s3-bucket-name>
```

Inside that bucket, the dataset will eventually live under a prefix like:

```text
<your-s3-prefix>
```

Example placeholders:

```text
S3 bucket: <your-s3-bucket-name>
S3 prefix: <your-s3-prefix>
```

---

## 5. IAM prerequisite for Codespaces development

For local development from Codespaces, create a **dedicated IAM user** or equivalent development credential with tightly scoped permissions.

This development identity should have enough access to:

- write objects to the chosen S3 bucket/prefix
- authenticate to ECR
- push images to the chosen ECR repository

This is for **development only**.

Once the app runs inside ECS, it should use **task roles**, not access keys embedded in the container.

---

## 6. Codespaces secrets prerequisite

Add AWS credentials to **Codespaces secrets**, not to the repo.

Typical secrets:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`

If you are using temporary credentials, also add:

- `AWS_SESSION_TOKEN`

These secrets are used for local development in Codespaces.

---

## 7. Local `.env` prerequisite

Create a local `.env` file for **non-secret** runtime config.

Example `.env.example`:

```env
AWS_REGION=us-east-1
S3_BUCKET=<your-s3-bucket-name>
S3_PREFIX=<your-s3-prefix>
ROW_COUNT=100
SOURCE_NAME=codespaces_smoke_test
RUN_DATE=
MAX_RUNTIME_MINUTES=20
```

Important:
- `.env` should be gitignored
- real AWS credentials should **not** be placed in `.env`

---

## 8. ECR prerequisite

Create a private ECR repository for the Docker image.

Example placeholder:

```text
<account-id>.dkr.ecr.<region>.amazonaws.com/<repository-name>
```

Example shape:

```text
123456789012.dkr.ecr.us-east-1.amazonaws.com/clickstream-smoke-test
```

---

## 9. ECS IAM role prerequisites

You need **two** ECS roles.

### ECS task execution role
Used by ECS/Fargate itself to:
- pull the image from ECR
- write logs to CloudWatch

This typically uses the managed policy:

```text
AmazonECSTaskExecutionRolePolicy
```

### ECS task role
Used by the **application code inside the container** to access AWS services, especially S3.

This role should have a narrowly scoped S3 write policy for:

```text
s3://<your-s3-bucket-name>/<your-s3-prefix>/*
```

---

## 10. ECS networking prerequisite

To run the ECS task successfully, you need:

- a VPC
- subnet IDs
- security group IDs

For a simple demo setup, the ECS task can run in public subnets with:

- subnet IDs: `<subnet-id-1>,<subnet-id-2>,...`
- security group ID: `<security-group-id>`
- public IP assignment: enabled

These values are needed when:
- running the ECS task manually
- creating the EventBridge Scheduler target

---

## 11. Athena prerequisite

Athena needs:
- access to the S3 dataset location
- a database in the AWS Glue Data Catalog
- an external table definition pointing to the dataset root
- partitions loaded with `MSCK REPAIR TABLE`

Athena also needs query results configured, either through:
- Athena managed query results
- or an S3 output location for query results

---

# Local setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

# Local development workflow

## Run the tests

```bash
pytest -v
```

## Run the app directly

```bash
python main.py
```

When it runs successfully, it should:

- generate the dataset
- validate the schema
- write a local Parquet file
- upload the file to S3
- print a small preview in the terminal

---

# Docker workflow

## Build the Docker image in Codespaces

```bash
docker build -t clickstream-smoke-test .
```

## Run the container in Codespaces

```bash
docker run --rm \
  --env-file .env \
  -e AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY \
  clickstream-smoke-test
```

If you use temporary credentials, also pass:

```bash
-e AWS_SESSION_TOKEN
```

---

# AWS deployment flow

## Step 1: Build the image
Build the Docker image in Codespaces.

## Step 2: Push the image to ECR
Authenticate Docker to ECR, tag the image, and push it.

Example placeholder URI:

```text
<account-id>.dkr.ecr.<region>.amazonaws.com/<repository-name>:latest
```

## Step 3: Create the ECS roles
Create:
- an ECS task execution role
- an ECS task role with S3 write permissions

## Step 4: Create the ECS cluster
Create an ECS cluster that supports Fargate tasks.

## Step 5: Create the ECS task definition
The task definition should include:

- the ECR image URI
- CPU and memory settings
- task execution role
- task role
- environment variables
- CloudWatch logging

Example environment variable placeholders:

- `AWS_REGION=<your-region>`
- `S3_BUCKET=<your-s3-bucket-name>`
- `S3_PREFIX=<your-s3-prefix>`
- `ROW_COUNT=100`
- `SOURCE_NAME=ecs_fargate_smoke_test`

## Step 6: Run the ECS task manually once
Before scheduling anything, run the task manually and confirm:

- the task starts and stops normally
- logs appear in CloudWatch
- a Parquet file lands in S3

## Step 7: Create the EventBridge schedule
Create a recurring EventBridge Scheduler schedule targeting ECS `RunTask`.

## Step 8: Set up Athena
Create:
- a database
- an external table
- partitions
- then query the data

---

# AWS resources created for this demo

You will likely end up creating resources similar to these:

- **S3 bucket**: `<your-s3-bucket-name>`
- **S3 prefix**: `<your-s3-prefix>`
- **ECR repository**: `<repository-name>`
- **ECS cluster**: `<ecs-cluster-name>`
- **ECS task definition family**: `<task-definition-family>`
- **EventBridge schedule**: `<schedule-name>`
- **Athena database**: `<athena-database-name>`
- **Athena table**: `<athena-table-name>`
- **CloudWatch log group**: `/ecs/<your-log-group-name>`

You can use your own naming convention, but keeping names consistent makes the AWS side much easier to follow.

---

# S3 output layout

The uploaded files land in S3 using a path like this:

```text
<your-s3-prefix>/ingest_date=YYYY-MM-DD/part-<timestamp>.parquet
```

Example:

```text
synthetic_clickstream_daily/ingest_date=2026-05-05/part-2026-05-05T15-16-53.parquet
```

Important:
- the file still contains a `run_date` column
- the S3 partition folder uses `ingest_date` on purpose so Athena does not have a partition-column conflict

---

# Athena setup example

Example database creation:

```sql
CREATE DATABASE IF NOT EXISTS smoke_test;
```

Example external table:

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS clickstream_daily (
  run_date string,
  utc_timestamp string,
  customer_id int,
  entry_page string,
  page_views int,
  product_views int,
  conversion_probability double,
  converted int,
  source string
)
PARTITIONED BY (
  ingest_date string
)
STORED AS PARQUET
LOCATION 's3://<your-s3-bucket-name>/<your-s3-prefix>/';
```

Load partitions:

```sql
MSCK REPAIR TABLE clickstream_daily;
```

Check partitions:

```sql
SHOW PARTITIONS clickstream_daily;
```

Example query:

```sql
SELECT ingest_date, COUNT(*) AS row_count
FROM clickstream_daily
GROUP BY ingest_date
ORDER BY ingest_date;
```

Use partition filters when possible:

```sql
WHERE ingest_date = 'YYYY-MM-DD'
```

---

# How to verify runs

The easiest way to verify the AWS deployment is working is to check these in order:

1. **ECS Tasks**  
   Confirm a task launched and reached `STOPPED` normally.

2. **CloudWatch Logs**  
   Confirm the application output looks clean.

3. **S3**  
   Confirm a new Parquet file landed under the correct `ingest_date=...` path.

4. **Athena**  
   Confirm the new partition is queryable.

---

# Cost / safety notes

This is intentionally a very small task.

A few good habits:

- keep task count at `1`
- avoid retries unless you truly need them
- disable the schedule when you are not demoing
- use Athena partition filters
- use ECS task roles in AWS instead of putting credentials into containers

---

# Current status

Right now, this smoke test proves the following pattern works end to end:

- local development in GitHub Codespaces
- clean Python project structure with `src/` and `tests/`
- synthetic dataset generation
- schema validation
- local Parquet output
- S3 upload
- Docker packaging
- image storage in ECR
- scheduled execution with ECS Fargate and EventBridge Scheduler
- Athena querying over S3 Parquet data

---

# Plain English summary

This project is basically a dress rehearsal for a data engineering workflow in AWS.

It creates fake web activity data, saves it in a format commonly used in analytics workflows, runs as a scheduled containerized batch job in AWS, lands the data in S3, and makes it queryable with Athena.
