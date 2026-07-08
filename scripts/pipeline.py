import json
from snowflake.snowpark import Session
from database_files.snowflake_session import SnowflakeSession



def load_raw_data(session, storage_stage="@retail_sales_stage/sales.csv"):
    """Load raw data from S3 stage into RAW_SALES table."""
    try:
        print("\nLoading raw data from S3 stage...")

        session.sql(f"""
            COPY INTO RAW_SALES
            FROM {storage_stage}
            FILE_FORMAT = (
                TYPE = 'CSV'
                FIELD_OPTIONALLY_ENCLOSED_BY = '"'
                SKIP_HEADER = 1
                DATE_FORMAT = 'YYYY-MM-DD'
                NULL_IF = ('', 'NULL', 'null')
                EMPTY_FIELD_AS_NULL = TRUE
            )
            ON_ERROR = 'CONTINUE'
        """).collect()
        print("Data copied from stage to RAW_SALES")

        count = session.sql("SELECT COUNT(*) AS ROW_COUNT FROM RAW_SALES").collect()
        print(f"Total rows loaded: {count[0]['ROW_COUNT']}")

        print("\nSample data preview:")
        session.sql("SELECT * FROM RAW_SALES LIMIT 5").show()

    except Exception as e:
        print(f"Raw data load failed: {e}")
        raise


if __name__ == "__main__":
    session = SnowflakeSession().get_session()
    load_raw_data(session)
    SnowflakeSession().close_session(session)