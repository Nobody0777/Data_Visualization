import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore

# Set up the Streamlit page
st.title("Data Visualization")
st.sidebar.header("Upload and Navigation")

# File upload
uploaded_file = st.sidebar.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Load the dataset
    data = pd.read_excel(uploaded_file)
    st.sidebar.success("File uploaded successfully!")
    st.write("### Dataset Overview")
    st.dataframe(data.head())

    # Navigation options
    options = st.sidebar.selectbox("Select Visualization", [
        "Distribution of a Column",
        "Top-N Categories by Aggregated Value",
        "Heatmap of Numerical Data",
        "Outlier Detection",
        "Box Plot Comparison",
        "Time Series Analysis",
        "Stacked Bar Chart"
    ])

    # Task 1: Distribution of a Column
    if options == "Distribution of a Column":
        st.header("Distribution of a Column")
        column = st.selectbox("Select Column for Distribution", data.columns)
        if data[column].dtype in ['int64', 'float64', 'object']:
            fig, ax = plt.subplots(figsize=(8, 6))
            if data[column].dtype == 'object':
                sns.countplot(data=data, x=column, palette='coolwarm', ax=ax)
            else:
                sns.histplot(data=data, x=column, kde=True, color='blue', ax=ax)
            ax.set_title(f'Distribution of {column}')
            st.pyplot(fig)
        else:
            st.error("Selected column is not suitable for distribution visualization.")

    # Task 2: Top-N Categories by Aggregated Value
    elif options == "Top-N Categories by Aggregated Value":
        st.header("Top-N Categories by Aggregated Value")
        category_column = st.selectbox("Select Category Column", data.columns)
        numeric_column = st.selectbox("Select Numeric Column", data.columns)
        n = st.slider("Select Top-N Categories", 1, 20, 5)
        if data[category_column].dtype == 'object' and data[numeric_column].dtype in ['int64', 'float64']:
            grouped_data = data.groupby(category_column)[numeric_column].sum().reset_index()
            top_n = grouped_data.sort_values(by=numeric_column, ascending=False).head(n)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(data=top_n, x=numeric_column, y=category_column, palette='viridis', ax=ax)
            ax.set_title(f'Top-{n} {category_column} by {numeric_column}')
            st.pyplot(fig)
        else:
            st.error("Ensure you select a categorical column and a numeric column.")

    # Task 3: Heatmap of Numerical Data
    elif options == "Heatmap of Numerical Data":
        st.header("Heatmap of Numerical Data")
        numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_columns) > 1:
            heatmap_data = data[numeric_columns].corr()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', ax=ax)
            ax.set_title("Correlation Heatmap")
            st.pyplot(fig)
        else:
            st.error("Dataset does not have enough numerical columns for a heatmap.")

    # Task 4: Outlier Detection
    elif options == "Outlier Detection":
        st.header("Outlier Detection")
        numeric_column = st.selectbox("Select Numeric Column for Outlier Detection", data.select_dtypes(include=['int64', 'float64']).columns)
        threshold = st.slider("Select Z-Score Threshold", 1.0, 5.0, 3.0)
        data['Z_Score'] = zscore(data[numeric_column])
        outliers = data[data['Z_Score'].abs() > threshold]
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=data, x=data.index, y=numeric_column, label='Data', color='blue', ax=ax)
        sns.scatterplot(data=outliers, x=outliers.index, y=numeric_column, label='Outliers', color='red', ax=ax)
        ax.set_title(f'Outlier Detection in {numeric_column}')
        ax.legend()
        st.pyplot(fig)

    # Task 5: Box Plot Comparison
    elif options == "Box Plot Comparison":
        st.header("Box Plot Comparison")
        category_column = st.selectbox("Select Categorical Column", data.columns)
        numeric_column = st.selectbox("Select Numeric Column", data.columns)
        if data[category_column].dtype == 'object' and data[numeric_column].dtype in ['int64', 'float64']:
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.boxplot(data=data, x=category_column, y=numeric_column, palette='Set2', ax=ax)
            ax.set_title(f'Box Plot of {numeric_column} by {category_column}')
            st.pyplot(fig)
        else:
            st.error("Ensure you select a categorical column and a numeric column.")

    # Task 6: Time Series Analysis
    elif options == "Time Series Analysis":
        st.header("Time Series Analysis")
        if 'Time' in data.columns:
            data['Time'] = pd.to_datetime(data['Time'])
            time_column = st.selectbox("Select Time Column", ['Time'])
            value_column = st.selectbox("Select Value Column", data.select_dtypes(include=['int64', 'float64']).columns)
            time_data = data.groupby(data[time_column].dt.to_period('M'))[value_column].sum().reset_index()
            time_data[time_column] = time_data[time_column].dt.to_timestamp()
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.lineplot(data=time_data, x=time_column, y=value_column, ax=ax, marker='o')
            ax.set_title(f'Time Series Analysis of {value_column}')
            st.pyplot(fig)
        else:
            st.error("The dataset does not have a time column.")

    # Task 7: Stacked Bar Chart
    elif options == "Stacked Bar Chart":
        st.header("Stacked Bar Chart")
        category_column = st.selectbox("Select Categorical Column", data.columns)
        numeric_columns = st.multiselect("Select Numeric Columns", data.select_dtypes(include=['int64', 'float64']).columns)
        if len(numeric_columns) > 1 and category_column:
            grouped_data = data.groupby(category_column)[numeric_columns].sum()
            fig, ax = plt.subplots(figsize=(12, 8))
            grouped_data.plot(kind='bar', stacked=True, ax=ax, colormap='coolwarm')
            ax.set_title(f'Stacked Bar Chart of {", ".join(numeric_columns)} by {category_column}')
            st.pyplot(fig)
        else:
            st.error("Ensure you select one categorical column and multiple numeric columns.")

else:
    st.warning("Please upload an Excel file to begin.")
