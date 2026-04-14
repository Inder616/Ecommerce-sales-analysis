import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv(r"data\Sample - Superstore.csv", encoding='latin-1')

# Check the dataset
'''
print(df.head())
print(df.columns)
print(df.shape)
print(df.describe())
print(df.info())
print(df.dtypes)
print(df.isnull().sum())
print(df.duplicated().sum())
'''

# -------------------------------
# BQ1: Which category sells the most?
# Analyze total sales by category to identify the top-performing category

group = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)

# -------------------------------
# BQ2: Which region performs best?
# Analyze region-wise sales to identify the highest contributing region

region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)

# -------------------------------
# BQ3: How are sales changing over time?
# Analyze monthly sales trend to identify growth patterns and seasonality

df['Order Date'] = pd.to_datetime(df['Order Date'])
monthly_sales = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum()

# -------------------------------
# BQ4: Which category generates the highest profit?
# Analyze profit by category to identify the most profitable segment

profit_by_category = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)

# -------------------------------
# Visualization 

plt.figure(figsize=(13,10))

# Main title 
plt.suptitle("E-Commerce Sales Insights Dashboard", 
             fontsize=18, fontweight='bold')

# -------------------------------
# 1. Sales by Category (Bar Chart)
plt.subplot(2,2,1)

# Highlight top category
colors = ['#4C9AFF' if i != 0 else '#1f4e79' for i in range(len(group))]

plt.bar(group.index, group.values,
        color=colors, edgecolor='black')

for i in range(len(group)):
    value = group.values[i]
    plt.text(i, value + 10000,
             f'{value/1000:.0f}K',
             ha='center', fontsize=9)

plt.title('Top Category by Sales', fontsize=12, fontweight='bold')
plt.ylabel('Total Sales')
plt.ylim(600000, 900000) 
plt.grid(axis='y', alpha=0.25)

# -------------------------------
# 2. Sales by Region (Pie Chart)
plt.subplot(2,2,2)

plt.pie(region_sales.values,
        labels=region_sales.index,
        autopct='%1.1f%%',
        startangle=140, 
        colors=['#4C9AFF','#FF9F40','#4CAF50','#FF6384'],
        wedgeprops={'edgecolor':'white'})

plt.title('Sales Distribution by Region', fontsize=12, fontweight='bold')

# -------------------------------
# 3. Monthly Sales Trend (Line Chart)
plt.subplot(2,2,3)

plt.plot(monthly_sales.index.astype(str), monthly_sales.values,
         color='#1f4e79',  linewidth=2)

plt.fill_between(monthly_sales.index.astype(str), monthly_sales.values, 
                 color='#4C9AFF', alpha=0.2)

plt.title('Monthly Sales Trend Over Time', fontsize=12, fontweight='bold')
plt.xlabel('Month-Year')

# Reduce clutter
plt.xticks(monthly_sales.index.astype(str)[::3], rotation=45)

plt.grid(alpha = False)

# -------------------------------
# 4. Profit by Category (Bar Chart)
plt.subplot(2,2,4)

# Highlight top profit category
colors_profit = ['#4C9AFF' if i != 0 else '#1f4e79' for i in range(len(profit_by_category))]

plt.bar(profit_by_category.index, profit_by_category.values,
        color=colors_profit, edgecolor='black')

for i in range(len(profit_by_category)):
    value = profit_by_category.values[i]
    plt.text(i, value + 1000,
             f'{value/1000:.0f}K',
             ha='center', fontsize=9)


plt.title('Profit by Category\n(Furniture: High Sales, Low Profit!)', fontsize=11, fontweight='bold')
plt.ylabel('Total Profit')
plt.grid(axis='y', alpha=0.25)

# -------------------------------
# Final layout
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save the figure
plt.savefig("dashboard.png", dpi=300)

plt.show()