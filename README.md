# Data Ingestion Smoke Test

This project is a small, realistic smoke test for a beginner-friendly data engineering workflow in AWS.

The goal is **not** to build a full production pipeline yet.

The goal is to prove that the core path works:

**GitHub Codespaces → Python app → Parquet file → AWS S3**

---

## What this project does

Each time you run the app, it:

1. generates a small synthetic clickstream-style dataset
2. checks that the dataset has the columns we expect
3. writes the data to a local Parquet file
4. uploads that file to S3

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
- Can I generate structured data?
- Can I write that data to Parquet?
- Can I upload the result to S3?
- Can I do all of that in a way that later fits Docker and AWS workflows?

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
- AWS-friendly app design

It is intentionally small enough to understand without getting overwhelmed.

---

## What is intentionally out of scope

This project is **not** trying to do everything.

It does **not** yet include:

- real source system ingestion
- production orchestration
- container deployment
- scheduling
- data catalog setup
- Athena table creation
- full infrastructure-as-code
- production-grade logging/monitoring

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
├── .env.example
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
