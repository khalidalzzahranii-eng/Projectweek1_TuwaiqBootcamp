
# Import necessary libraries
import streamlit as st  # Streamlit library for dashboard UI
import pandas as pd      # Pandas for data manipulation
import matplotlib.pyplot as plt  # Matplotlib for plotting charts
from matplotlib.ticker import StrMethodFormatter  # For formatting y-axis numbers
import numpy as np       # Numpy for numerical operations

# Page settings
st.set_page_config(
    page_title="Adidas Dashboard",  # Title of the web page
    layout="wide"                   # Wide layout to use full screen width
)

# Apply custom CSS styling for dark theme
st.markdown("""
<style>
body { background-color: #0A0A0A; color: #E0E1DD; }
.sidebar .sidebar-content { background-color: #0D1B2A; color: #E0E1DD; }
</style>
""", unsafe_allow_html=True)

# Load dataset
df = pd.read_csv("cleaned_data_sales.csv")

# Sidebar: Filters and dataset information
st.sidebar.header("Filters & Dataset Info")

# Show a brief description of the dataset
st.sidebar.markdown("Dataset Description")
st.sidebar.markdown("""
This dataset contains Adidas sales data including:
- Product, Units Sold
- Total Sales, Operating Profit
- Sales Method (Online / In-Store/Outlet)
- Region
""")
st.sidebar.markdown("Filters")

# Sidebar filter options
regions = ["All"] + sorted(df["Region"].unique())
methods = ["All"] + sorted(df["Sales Method"].unique())
years = ["All"] + sorted(df["Year"].unique())

# Sidebar select boxes for filtering
selected_region = st.sidebar.selectbox("Select Region", regions)
selected_method = st.sidebar.selectbox("Select Sales Method", methods)
selected_year = st.sidebar.selectbox("Select Year", years)

# Apply filters without modifying the original dataframe
filtered_df = df.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]
if selected_method != "All":
    filtered_df = filtered_df[filtered_df["Sales Method"] == selected_method]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]

# Page header: Logo and title
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("/content/adidas.png", width=120)  # Display logo
with col_title:
    st.title("Adidas Sales Dashboard")  # Dashboard title

# KPI Metrics
top_product_name = filtered_df.groupby("Product")["Units Sold"].sum().idxmax()  # Find top product
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${filtered_df['Total Sales'].sum():,.0f}")  # Total sales
col2.metric("Total Profit", f"${filtered_df['Operating Profit'].sum():,.0f}")  # Total profit
col3.metric("Total Units Sold", f"{filtered_df['Units Sold'].sum():,}")  # Total units sold
col4.markdown(f"""
Top Product:
<div style='font-size:20px; line-height:1.2; white-space: pre-wrap; word-wrap: break-word;'>{top_product_name}</div>
""", unsafe_allow_html=True)  # Display top product with text wrapping

# Define chart colors
chart_colors = ['#1E3A8A', '#2563EB', '#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE', '#E0F2FE']

# First row: Overview charts
row1_col1, row1_col2 = st.columns(2)

# Monthly Sales Line Chart
with row1_col1:
    # Title with bigger font
    st.markdown("""
    <span style='font-size:24px; font-weight:bold; color:#FFFFFF'>
    Monthly Sales (by Year & Month)
    </span>
    """, unsafe_allow_html=True)

    # Convert 'Invoice Date' column to datetime type
    filtered_df['Invoice Date'] = pd.to_datetime(filtered_df['Invoice Date'])
    # Create 'YearMonth' column for grouping (e.g., Jan 2020)
    filtered_df['YearMonth'] = filtered_df['Invoice Date'].dt.strftime('%b %Y')

    # Aggregate total sales per 'YearMonth'
    monthly_sales = filtered_df.groupby('YearMonth')['Total Sales'].sum().reset_index()
    # Convert 'YearMonth' to datetime for proper sorting
    monthly_sales['Date'] = pd.to_datetime(monthly_sales['YearMonth'])
    monthly_sales = monthly_sales.sort_values('Date')

    # Create the matplotlib figure and axis
    fig, ax = plt.subplots()
    # Set figure and axis backgrounds to transparent
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")

    # Plot line chart with marker points
    ax.plot(monthly_sales['YearMonth'], monthly_sales['Total Sales'], color=chart_colors[2], linewidth=4, marker='o')

    # Set axis labels with white color
    ax.set_xlabel("Month-Year", color="#FFFFFF")
    ax.set_ylabel("Total Sales ($)", color="#FFFFFF")

    # Format y-axis numbers with commas for readability
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    # Customize tick labels
    plt.xticks(rotation=45, ha="right", fontsize=10, color="#FFFFFF")
    plt.yticks(fontsize=10, color="#FFFFFF")

    # Remove chart borders
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Display the figure in Streamlit
    st.pyplot(fig)


# Profit by Region Bar Chart
with row1_col2:
    # Title with bigger font
    st.markdown("""
    <span style='font-size:24px; font-weight:bold; color:#FFFFFF'>
    Profit by Region
    </span>
    """, unsafe_allow_html=True)

    # Group the filtered data by 'Region' and sum the 'Operating Profit' for each region
    profit_region = filtered_df.groupby('Region')['Operating Profit'].sum()

    # Create a matplotlib figure and axis for the bar chart
    fig, ax = plt.subplots()
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")

    # Select bar colors from chart_colors
    bar_colors = chart_colors[:len(profit_region)]
    # Create the bar chart
    ax.bar(profit_region.index, profit_region.values, color=bar_colors, edgecolor='none')

    # Set axis labels and title
    ax.set_xlabel("Region", color="#FFFFFF")
    ax.set_ylabel("Profit ($)", color="#FFFFFF")

    # Format y-axis numbers with commas
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

    # Customize tick labels
    ax.tick_params(axis='x', colors="#FFFFFF", labelsize=12)
    ax.tick_params(axis='y', colors="#FFFFFF", labelsize=12)

    # Remove chart borders
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Display the figure in Streamlit
    st.pyplot(fig)


# Second row: Detailed charts
row2_col1, row2_col2 = st.columns(2)

# Top Products by Units Sold
with row2_col1:
    # Title with bigger font
    st.markdown("""
    <span style='font-size:24px; font-weight:bold; color:#FFFFFF'>
    Top Products by Units Sold
    </span>
    """, unsafe_allow_html=True)

    # Group the filtered DataFrame by 'Product' and sum the 'Units Sold' for each product
    # Then sort descending and take the top 10
    top_products = filtered_df.groupby("Product")["Units Sold"].sum().sort_values(ascending=False).head(10)

    # Create a matplotlib figure and axis for the horizontal bar chart
    fig, ax = plt.subplots(figsize=(9, 10))
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")

    # Select bar colors
    bar_colors = chart_colors[:len(top_products)]
    # Draw horizontal bars (reversed for largest on top)
    ax.barh(top_products.index[::-1], top_products.values[::-1], color=bar_colors, edgecolor='none')

    # Set axis labels and customize font size
    ax.set_xlabel("Units Sold", color="#FFFFFF", fontsize=12)
    ax.set_ylabel("Product", color="#FFFFFF", fontsize=14)
    ax.tick_params(axis='x', colors="#FFFFFF", labelsize=12)
    ax.tick_params(axis='y', colors="#FFFFFF", labelsize=12)

    # Remove chart borders
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Display the figure in Streamlit
    st.pyplot(fig)


# Profit by Sales Method Pie Chart
with row2_col2:
    # Title with bigger font
    st.markdown("""
    <span style='font-size:24px; font-weight:bold; color:#FFFFFF'>
    Profit by Sales Method
    </span>
    """, unsafe_allow_html=True)

    # Group the filtered data by 'Sales Method' and sum the 'Operating Profit'
    profit_method = filtered_df.groupby('Sales Method')['Operating Profit'].sum()

    # Create a matplotlib figure and axis for the pie chart
    fig, ax = plt.subplots()
    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")

    # Select colors for each slice
    pie_colors = chart_colors[:len(profit_method)]

    # Draw pie chart with labels and percentages
    ax.pie(profit_method.values, labels=profit_method.index, autopct='%1.1f%%', startangle=90, colors=pie_colors,
           textprops={'color': "#FFFFFF"})
    ax.axis('equal')  # Keep the pie chart circular

    # Remove chart borders
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Display the figure in Streamlit
    st.pyplot(fig)


# Summary statistics
st.markdown("""
<span style='font-size:22px; font-weight:bold; color:#FFFFFF'>
Summary Statistics
</span>
""", unsafe_allow_html=True)
st.write(filtered_df.describe())  # Show descriptive statistics

# Data table preview
st.markdown("""
<span style='font-size:22px; font-weight:bold; color:#FFFFFF'>
Data Preview
</span>
""", unsafe_allow_html=True)
st.dataframe(filtered_df.head(10))  # Show interactive table
