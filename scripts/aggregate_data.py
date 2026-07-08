from snowflake.snowpark.functions import col, month, year, sum, avg
from database_scripts.pipeline import load_raw_data
from database_files.snowflake_session import SnowflakeSession
from database_scripts.transform_data import transform_data


def aggregate_product_sales(session):
    """Aggregate total revenue and units sold per product."""
    try:
        print("\nAggregating product sales...")

        df = session.table("TRANSFORMED_SALES")

        # Aggregate by product
        product_agg = df.group_by("PRODUCT").agg(
            sum(col("UNITS_SOLD")).alias("TOTAL_UNITS_SOLD"),
            sum(col("TOTAL_SALES")).alias("TOTAL_REVENUE"),
            avg(col("UNIT_PRICE")).alias("AVG_UNIT_PRICE")
        )
        # Write to AGG_PRODUCT_SALES
        product_agg.write.mode("overwrite").save_as_table("AGG_PRODUCT_SALES")
        print("AGG_PRODUCT_SALES written")

        # Verify and preview using Snowpark DataFrame style
        session.table("AGG_PRODUCT_SALES").limit(5).show()

    except Exception as e:
        print(f"Product aggregation failed: {e}")
        raise


def aggregate_regional_sales(session):
    """Aggregate total revenue and units sold per region."""
    try:
        print("\nAggregating regional sales...")

        df = session.table("TRANSFORMED_SALES")
        # Aggregate by region
        regional_agg = df.group_by("REGION").agg(
            sum(col("UNITS_SOLD")).alias("TOTAL_UNITS_SOLD"),
            sum(col("TOTAL_SALES")).alias("TOTAL_REVENUE"),
            avg(col("TOTAL_SALES")).alias("AVG_ORDER_VALUE")
        )
        # Write to AGG_REGIONAL_SALES
        regional_agg.write.mode("overwrite").save_as_table("AGG_REGIONAL_SALES")
        print("AGG_REGIONAL_SALES written")
        # Verify and preview using Snowpark DataFrame style
        session.table("AGG_REGIONAL_SALES").limit(5).show()

    except Exception as e:
        print(f"Regional aggregation failed: {e}")
        raise


def aggregate_monthly_sales(session):
    """Aggregate total revenue and units sold per month and year."""
    try:
        print("\nAggregating monthly sales...")

        df = session.table("TRANSFORMED_SALES")
        # Aggregate by year and month
        monthly_agg = df.group_by("YEAR", "MONTH").agg(
            sum(col("UNITS_SOLD")).alias("TOTAL_UNITS_SOLD"),
            sum(col("TOTAL_SALES")).alias("TOTAL_REVENUE")
        )
        # Write to AGG_MONTHLY_SALES
        monthly_agg.write.mode("overwrite").save_as_table("AGG_MONTHLY_SALES")
        print("AGG_MONTHLY_SALES written")
        # Verify and preview using Snowpark DataFrame style
        session.table("AGG_MONTHLY_SALES").sort(col("YEAR"), col("MONTH")).limit(5).show()

    except Exception as e:
        print(f"Monthly aggregation failed: {e}")
        raise
def aggregate_region_product_sales(session):
    """Aggregate revenue and units sold by region and product."""
    try:
        print("\nAggregating region product sales...")

        df = session.table("TRANSFORMED_SALES")

        region_product_agg = df.group_by("REGION", "PRODUCT").agg(
            sum(col("UNITS_SOLD")).alias("TOTAL_UNITS_SOLD"),
            sum(col("TOTAL_SALES")).alias("TOTAL_REVENUE")
        )

        region_product_agg.write.mode("overwrite").save_as_table("AGG_REGION_PRODUCT_SALES")
        print("AGG_REGION_PRODUCT_SALES written")

        session.table("AGG_REGION_PRODUCT_SALES").limit(5).show()

    except Exception as e:
        print(f"Region product aggregation failed: {e}")
        raise

if __name__ == "__main__":
    sf = SnowflakeSession()
    session = sf.get_session()
    aggregate_product_sales(session)
    aggregate_regional_sales(session)
    aggregate_monthly_sales(session)
    aggregate_region_product_sales(session)
    sf.close_session(session)