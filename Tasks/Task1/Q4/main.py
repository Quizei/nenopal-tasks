import sqlite3

# Step 1: Connect to the existing SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Step 2: Find the total number of unique records using SQL query
query = '''
SELECT COUNT(*) AS total_unique_records
FROM (
    SELECT "Order ID", "Product ID" FROM table_data1
    UNION
    SELECT "Order ID", "Product ID" FROM table_data2
) AS combined_dataset;
'''

cursor.execute(query)
total_unique_records = cursor.fetchone()[0]

# Step 3: Print the total number of unique records
print(f"Total number of unique records: {total_unique_records}")

# Step 4: Close the connection
conn.close()
