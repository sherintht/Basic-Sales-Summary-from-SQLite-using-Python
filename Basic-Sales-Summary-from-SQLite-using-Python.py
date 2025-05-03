import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. Create database and insert sample data
conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

# Drop table if exists to reset
cursor.execute('DROP TABLE IF EXISTS sales')

# Create table
cursor.execute('''
    CREATE TABLE sales (
        id INTEGER PRIMARY KEY,
        product TEXT,
        quantity INTEGER,
        price REAL,
        sale_date DATE
    )
''')

# Insert sample data
sample_data = [
    ('Product A', 2, 10.0, '2023-10-01'),
    ('Product B', 5, 20.0, '2023-10-02'),
    ('Product A', 3, 10.0, '2023-10-03'),
    ('Product C', 7, 15.0, '2023-10-04'),
    ('Product B', 1, 20.0, '2023-10-05'),
]

cursor.executemany('''
    INSERT INTO sales (product, quantity, price, sale_date)
    VALUES (?, ?, ?, ?)
''', sample_data)

conn.commit()

# 2. Query data with SQL
query = '''
    SELECT product, 
           SUM(quantity) AS total_quantity, 
           SUM(quantity * price) AS total_revenue
    FROM sales
    GROUP BY product
    ORDER BY product
'''

df = pd.read_sql_query(query, conn)
conn.close()

# 3. Print summary
print("📊 Basic Sales Summary")
print("---------------------------")
print(f"Total Quantity Sold: {df['total_quantity'].sum()} units")
print(f"Total Revenue: ${df['total_revenue'].sum():.2f}")
print("\nSales by Product:")
print(df.to_string(index=False))

# 4. Plotting (ensure both plots appear)
plt.style.use('ggplot')

# First Plot: Quantity
plt.figure(figsize=(8, 5))
plt.bar(df['product'], df['total_quantity'], color='skyblue')
plt.title('Total Quantity Sold by Product')
plt.xlabel('Product')
plt.ylabel('Units Sold')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show(block=True)  # Force this window to stay open

# Second Plot: Revenue
plt.figure(figsize=(8, 5))
plt.bar(df['product'], df['total_revenue'], color='orange')
plt.title('Total Revenue by Product')
plt.xlabel('Product')
plt.ylabel('Revenue ($)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show(block=True)  # Force this window to stay open