import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

def read_csv_or_excel(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Only CSV and Excel (XLSX/XLS) files are supported.")

def change_datatypes(df, column_datatypes):
    return df.astype(column_datatypes)

def optimize_memory_usage(df):
    for col in df.select_dtypes(include=['object']).columns:
        num_unique = len(df[col].unique())
        num_total = len(df[col])
        if num_unique / num_total < 0.5:
            df[col] = df[col].astype('category')
    return df

if __name__ == "__main__":
    # Step 1: Upload the Excel file to Google Colab (Skip this step if you are not using Google Colab)
    from google.colab import files
    uploaded = files.upload()
    file_path = next(iter(uploaded))

    # Replace 'column_datatypes' with a dictionary containing column names and their respective desired data types
    column_datatypes = {
        "bike_name": str,
        "price": float,
        "city": str,
        "kms_driven": int,
        "owner": str,
        "age": int,
        "power": float,
        "brand": str
    }

    df = read_csv_or_excel(file_path)

    # Check memory usage before changing data types
    before_memory = df.memory_usage(deep=True).sum()

    # Change data types of columns
    df = change_datatypes(df, column_datatypes)

    # Check memory usage after changing data types
    after_memory = df.memory_usage(deep=True).sum()

    # Optimize memory usage by converting relevant string columns to categorical
    df = optimize_memory_usage(df)
    optimized_memory = df.memory_usage(deep=True).sum()

    # Step 2: Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Step 3: Dump data from the DataFrame into the SQLite database
    table_name = 'used_bikes_table'
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Step 4: Index the specified column after data insertion
    column_to_index = "bike_name"
    index_query = f"CREATE INDEX index_{column_to_index} ON {table_name} ({column_to_index})"
    cursor.execute(index_query)
    conn.commit()

    # Close the connection
    conn.close()
    # Plot the improvement in memory usage
    improvement = [before_memory, after_memory, optimized_memory]
    labels = ['Before Optimization', 'After Data Type Change', 'After Optimization']

    plt.figure(figsize=(15, 8))  # Increase the figure size
    plt.bar(labels, improvement, color=['red', 'green', 'blue'])
    plt.ylabel('Memory Usage (bytes)')
    plt.title('Memory Usage Improvement After Data Type Change and Optimization')
    plt.xticks(rotation=45)

    # Add percentage change as annotations to the bars with proper alignment
    for i in range(len(improvement)):
        percentage_change = ((improvement[i] - before_memory) / before_memory) * 100
        label = f"{improvement[i]:.2f} bytes\n({percentage_change:.2f}% change)"
        plt.annotate(label, (labels[i], improvement[i]), ha='center', va='bottom', fontsize=9, rotation=0)

    plt.tight_layout()
    plt.show()

    # Print the percentage change in memory usage
    percentage_change_after_data_type_change = ((after_memory - before_memory) / before_memory) * 100
    percentage_change_after_optimization = ((optimized_memory - before_memory) / before_memory) * 100
    print(f"Percentage change after data type change: {percentage_change_after_data_type_change:.2f}%")
    print(f"Percentage change after optimization: {percentage_change_after_optimization:.2f}%")
