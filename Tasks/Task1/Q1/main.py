import sqlite3

# Step 1: Connect to the existing SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Step 2: Find the number of missing records using SQL query
query = '''
SELECT COUNT(*) FROM (
    SELECT "Order ID", "Product ID" FROM table_data1
    EXCEPT
    SELECT "Order ID", "Product ID" FROM table_data2
) AS missing_records;
'''

cursor.execute(query)
number_of_missing_records = cursor.fetchone()[0]

# Step 3: Print the number of missing records
print(f"Number of missing records: {number_of_missing_records}")

# Step 4: Close the connection
conn.close()
