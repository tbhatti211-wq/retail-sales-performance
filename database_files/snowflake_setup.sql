-- Retail Sales Pipeline: S3 integration, external stage, and warehouse configuration
-- Author: Talib Hussain

-- ── Database setup ────────────────────────────────────────────────────────────

USE ROLE ACCOUNTADMIN;
CREATE OR REPLACE DATABASE retail_sales_performance;
USE DATABASE retail_sales_performance;
CREATE OR REPLACE SCHEMA performances;
USE SCHEMA performances;

-- ── Step 1: Create storage integration ───────────────────────────────────────

CREATE OR REPLACE STORAGE INTEGRATION s3_retail_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'use-your-iam-role-arn-here'
  STORAGE_ALLOWED_LOCATIONS = ('s3://s3-retail-performance/');

-- Step 2: Run DESC to get IAM User ARN and External ID
-- Paste both values into your AWS IAM role trust policy before proceeding
DESC INTEGRATION s3_retail_integration;

-- ── Step 3: Create external stage ────────────────────────────────────────────

CREATE OR REPLACE STAGE retail_sales_stage
  STORAGE_INTEGRATION = s3_retail_integration
  URL = 's3://s3-retail-performance/'
  FILE_FORMAT = (
    TYPE = 'CSV'
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
  );

-- ── Step 4: Verify connection ─────────────────────────────────────────────────

LIST @retail_sales_stage;

-- ── Step 5: Warehouse cost control ───────────────────────────────────────────

ALTER WAREHOUSE COMPUTE_WH SET AUTO_SUSPEND = 60;

CREATE OR REPLACE RESOURCE MONITOR retail_monitor
  WITH CREDIT_QUOTA = 5
  FREQUENCY = MONTHLY
  START_TIMESTAMP = IMMEDIATELY
  TRIGGERS
    ON 75 PERCENT DO NOTIFY
    ON 100 PERCENT DO SUSPEND_IMMEDIATE;

ALTER WAREHOUSE COMPUTE_WH SET RESOURCE_MONITOR = retail_monitor;