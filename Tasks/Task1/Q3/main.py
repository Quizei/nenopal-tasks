import pandas as pd

data1 = pd.read_csv('data1.csv') 
data2 = pd.read_csv('data2.csv')  

missing_data1 = data2[~data2.set_index(['Order ID', 'Product ID']).index.isin(data1.set_index(['Order ID', 'Product ID']).index)]
num_missing_data1 = len(missing_data1)

sum_qty_missing_data1_in_data2 = missing_data1['Qty'].sum()

print("Sum of the total Qty of Records missing in data1 but present in data2:", sum_qty_missing_data1_in_data2)



