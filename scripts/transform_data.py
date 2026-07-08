from snowflake.snowpark.functions import col, month, year
from database_files.snowflake_session import SnowflakeSession

def transform_data(session):
    """Transform raw data and load into TRANSFORMED_SALES table."""
    try:
        print("\nTransforming data...")

        # Read from RAW_SALES
        df = session.table("RAW_SALES")

        # Extract MONTH and YEAR from DATE
        df = df.with_column("MONTH", month(col("DATE")))
        df = df.with_column("YEAR", year(col("DATE")))

        # Rename SALES to TOTAL_SALES
        df = df.with_column_renamed("SALES", "TOTAL_SALES")

        # Select final column order
        df = df.select(
            col("DATE"),
            col("MONTH"),
            col("YEAR"),
            col("PRODUCT"),
            col("REGION"),
            col("UNITS_SOLD"),
            col("UNIT_PRICE"),
            col("TOTAL_SALES")
        )

        # Write to TRANSFORMED_SALES
        df.write.mode("overwrite").save_as_table("TRANSFORMED_SALES")
        print("   Data written to TRANSFORMED_SALES")

        # Verify and preview using Snowpark DataFrame style
        transform = session.table("TRANSFORMED_SALES")
        print(f"Total rows transformed: {transform.count()}")

        print("\nSample transformed data:")
        transform.limit(5).show()

    except Exception as e:
        print(f"Transform failed: {e}")
        raise

if __name__ == "__main__":
    session = SnowflakeSession().get_session()
    transform_data(session)
    SnowflakeSession().close_session(session)