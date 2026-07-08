import streamlit.streamlit as st
import altair as alt
from snowflake.snowpark.context import get_active_session

# Session
session = get_active_session()

# Title
st.title("Retail Sales Performance Dashboard")
st.markdown("---")

# Section 1: Product Performance
st.header("Product Performance")

product_df = session.table("AGG_PRODUCT_SALES").to_pandas()
product_df["TOTAL_REVENUE"] = product_df["TOTAL_REVENUE"].round(2)
product_df["AVG_UNIT_PRICE"] = product_df["AVG_UNIT_PRICE"].round(2)
product_df = product_df.sort_values("TOTAL_REVENUE", ascending=False)

st.subheader("Total Revenue by Product")
st.bar_chart(data=product_df, x="PRODUCT", y="TOTAL_REVENUE")

st.subheader("Sales Percentage by Product")
pie_chart = alt.Chart(product_df).mark_arc().encode(
    theta=alt.Theta(field="TOTAL_REVENUE", type="quantitative"),
    color=alt.Color(field="PRODUCT", type="nominal"),
    tooltip=["PRODUCT", "TOTAL_REVENUE"]
).properties(title="Revenue Share by Product")
st.altair_chart(pie_chart, use_container_width=True)

st.subheader("Units Sold vs Revenue by Product")
st.bar_chart(data=product_df, x="PRODUCT", y=["TOTAL_UNITS_SOLD", "TOTAL_REVENUE"])

st.subheader("Product Sales Breakdown")
st.dataframe(product_df, use_container_width=True)

st.markdown("---")

# Section 2: Monthly Trends
st.header("Monthly Trends")

monthly_df = session.table("AGG_MONTHLY_SALES").to_pandas()
monthly_df["TOTAL_REVENUE"] = monthly_df["TOTAL_REVENUE"].round(2)
monthly_df["MONTH_LABEL"] = monthly_df["YEAR"].astype(str) + "-" + monthly_df["MONTH"].astype(str).str.zfill(2)
monthly_df = monthly_df.sort_values(["YEAR", "MONTH"])

st.subheader("Month over Month Revenue")
line_chart = alt.Chart(monthly_df).mark_line(point=True).encode(
    x=alt.X("MONTH_LABEL", title="Month", sort=None),
    y=alt.Y("TOTAL_REVENUE", title="Total Revenue"),
    tooltip=["MONTH_LABEL", "TOTAL_REVENUE", "TOTAL_UNITS_SOLD"]
).properties(title="Monthly Revenue Trend")
st.altair_chart(line_chart, use_container_width=True)

st.subheader("Revenue Growth Area Chart")
area_chart = alt.Chart(monthly_df).mark_area(opacity=0.8).encode(
    x=alt.X("MONTH_LABEL", title="Month", sort=None),
    y=alt.Y("TOTAL_REVENUE", title="Total Revenue"),
    tooltip=["MONTH_LABEL", "TOTAL_REVENUE"]
).properties(title="Monthly Revenue Area")
st.altair_chart(area_chart, use_container_width=True)

st.subheader("Monthly Data")
st.dataframe(monthly_df, use_container_width=True)

st.markdown("---")

# Section 3: Regional Insights
st.header("Regional Insights")

regional_df = session.table("AGG_REGIONAL_SALES").to_pandas()
regional_df["TOTAL_REVENUE"] = regional_df["TOTAL_REVENUE"].round(2)
regional_df["AVG_ORDER_VALUE"] = regional_df["AVG_ORDER_VALUE"].round(2)
regional_df = regional_df.sort_values("TOTAL_REVENUE", ascending=False)

st.subheader("Revenue by Region")
horizontal_bar = alt.Chart(regional_df).mark_bar().encode(
    x=alt.X("TOTAL_REVENUE", title="Total Revenue"),
    y=alt.Y("REGION", sort="-x", title="Region"),
    tooltip=["REGION", "TOTAL_REVENUE", "TOTAL_UNITS_SOLD"]
).properties(title="Regional Revenue Comparison")
st.altair_chart(horizontal_bar, use_container_width=True)

region_product_df = session.table("AGG_REGION_PRODUCT_SALES").to_pandas()
region_product_df["TOTAL_REVENUE"] = region_product_df["TOTAL_REVENUE"].round(2)

st.subheader("Product Sales by Region")
stacked_bar = alt.Chart(region_product_df).mark_bar().encode(
    x=alt.X("REGION", title="Region"),
    y=alt.Y("TOTAL_REVENUE", title="Total Revenue"),
    color=alt.Color("PRODUCT", title="Product"),
    tooltip=["REGION", "PRODUCT", "TOTAL_REVENUE", "TOTAL_UNITS_SOLD"]
).properties(title="Product Revenue by Region")
st.altair_chart(stacked_bar, use_container_width=True)

st.subheader("Regional Sales Breakdown")
st.dataframe(regional_df, use_container_width=True)