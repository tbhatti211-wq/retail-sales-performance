import json
from snowflake.snowpark import Session

from database_files.snowflake_session import SnowflakeSession

session = SnowflakeSession().get_session()
def create_tables(session):
    """Create raw, transformed, and aggregated tables in Snowflake."""
    try:
        print("\nCreating tables...")

        # --- RAW TABLE (exact columns from CSV) ---
        session.sql("""
            CREATE OR REPLACE TABLE RAW_SALES (
                DATE             DATE,
                PRODUCT          STRING,
                REGION           STRING,
                UNITS_SOLD       INTEGER,
                UNIT_PRICE       FLOAT,
                SALES            FLOAT
            )
        """).collect()
        print("   RAW_SALES created")

        # --- TRANSFORMED TABLE (adds generated + derived columns) ---
        session.sql("""
            CREATE OR REPLACE TABLE TRANSFORMED_SALES (
                DATE             DATE,
                MONTH            INTEGER,
                YEAR             INTEGER,
                PRODUCT          STRING,
                REGION           STRING,
                UNITS_SOLD       INTEGER,
                UNIT_PRICE       FLOAT,
                TOTAL_SALES      FLOAT
            )
        """).collect()
        print("   TRANSFORMED_SALES created")

        # --- AGGREGATED TABLES ---
        session.sql("""
            CREATE OR REPLACE TABLE AGG_PRODUCT_SALES (
                PRODUCT          STRING,
                TOTAL_UNITS_SOLD INTEGER,
                TOTAL_REVENUE    FLOAT,
                AVG_UNIT_PRICE   FLOAT
            )
        """).collect()
        print("   AGG_PRODUCT_SALES created")

        session.sql("""
            CREATE OR REPLACE TABLE AGG_REGIONAL_SALES (
                REGION           STRING,
                TOTAL_UNITS_SOLD INTEGER,
                TOTAL_REVENUE    FLOAT,
                AVG_ORDER_VALUE  FLOAT
            )
        """).collect()
        print("   AGG_REGIONAL_SALES created")

        session.sql("""
            CREATE OR REPLACE TABLE AGG_MONTHLY_SALES (
                YEAR             INTEGER,
                MONTH            INTEGER,
                TOTAL_UNITS_SOLD INTEGER,
                TOTAL_REVENUE    FLOAT
            )
        """).collect()
        print("   AGG_MONTHLY_SALES created")

        session.sql("""
            CREATE OR REPLACE TABLE AGG_REGION_PRODUCT_SALES (
                REGION           STRING,
                PRODUCT          STRING,
                TOTAL_UNITS_SOLD INTEGER,
                TOTAL_REVENUE    FLOAT
                )        
                """).collect()
        print("   AGG_REGION_PRODUCT_SALES created")  
          
        print("\nAll tables created successfully!")

    except Exception as e:
        print(f"Table creation failed: {e}")
        raise


if __name__ == "__main__":
    create_tables(session)
    SnowflakeSession().close_session(session)