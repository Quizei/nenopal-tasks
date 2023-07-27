import pandas as pd
import sqlite3

# Step 1: Upload the Excel file to Google Colab (Skip this step if you are not using Google Colab)
from google.colab import files
uploaded = files.upload()

# Step 2: Connect to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Step 3: Read and insert data from each sheet in the Excel file
excel_file = pd.ExcelFile('data1.xlsx')

for sheet_name in excel_file.sheet_names:
    data = excel_file.parse(sheet_name)
    table_name = f'table_{sheet_name}'  
    column_names = ', '.join(f'"{col}"' for col in data.columns)
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_names})"
    cursor.execute(create_table_query)

    for _, row in data.iterrows():
        insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({', '.join(['?'] * len(row))})"
        cursor.execute(insert_query, tuple(row))

# Step 4: Commit the changes and close the connection
conn.commit()
conn.close()
