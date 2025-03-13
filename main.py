#Importing Required Libraries
import numpy as np
import pandas as pd
%matplotlib inline
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import folium


#Importing Data¶
from js import fetch
import io

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
resp = await fetch(URL)
text = io.BytesIO((await resp.arrayBuffer()).to_py())
import pandas as pd
df = pd.read_csv(text)
print('Data downloaded and read into a dataframe!')

df.describe()
df.columns


#Creating Visualizations for Data Analysis

#TASK 1.1: Develop a Line chart using the functionality of pandas to show how automobile sales fluctuate from year to year¶
# Group data by year and sum sales
df1 = df.groupby('Year')['Automobile_Sales'].mean().reset_index()

# Plot the line chart
df1.plot(x='Year', y='Automobile_Sales', kind='line', marker='o', linestyle='-', figsize=(10, 5))

# Customize the chart
plt.xticks(df1['Year'], rotation=75)
plt.xlabel('Year')
plt.ylabel('Total Automobile Sales')
plt.title('Yearly Automobile Sales Fluctuations')

# Annotate the 1981-82 Recession
plt.text(1982, 650, '1981-82 Recession', color='red')

plt.legend()
plt.grid(True)
# Show the plot
plt.show()

#TASK 1.2: Plot different lines for categories of vehicle type and analyse the trend to answer the question Is there a noticeable difference in sales trends between different vehicle types during recession periods?
# Assuming 'df' is your dataset
df_rec = df[df['Recession'] == 1]

# Calculate the average automobile sales by year and vehicle type during the recession
df_Mline = df_rec.groupby(['Year', 'Vehicle_Type'], as_index=False)['Automobile_Sales'].mean()

# Calculate the normalized sales by dividing by the average sales for each vehicle type
df_Mline['Normalized_Sales'] = df_Mline.groupby('Vehicle_Type')['Automobile_Sales'].transform(lambda x: x / x.mean())

# Set the 'Year' as the index
df_Mline.set_index('Year', inplace=True)

# Create the plot for each vehicle type
plt.figure(figsize=(12, 8))
for vehicle_type in df_Mline['Vehicle_Type'].unique():
    data = df_Mline[df_Mline['Vehicle_Type'] == vehicle_type]
    plt.plot(data.index, data['Normalized_Sales'], label=vehicle_type, marker='o')

# Highlight recession years
recession_years = df_rec['Year'].unique()
for year in recession_years:
    plt.axvline(x=year, color='gray', linestyle='--', alpha=0.5)

# Add labels, legend, and title
plt.legend(title="Vehicle Type", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.ylabel("Normalized Sales")
plt.xlabel("Year")
plt.title("Normalized Automobile Sales by Vehicle Type During Recession")

# Show the plot
plt.tight_layout()
plt.show()

#TASK 1.3: Use the functionality of Seaborn Library to create a visualization to compare the sales trend per vehicle type for a recession period with a non-recession period.
recession_data = df[df['Recession'] == 1]

dd=df.groupby(['Recession','Vehicle_Type'])['Automobile_Sales'].mean().reset_index()

    # Calculate the total sales volume by vehicle type during recessions
    #sales_by_vehicle_type = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index()

    # Create the grouped bar chart using seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x='Recession', y='Automobile_Sales', hue='Vehicle_Type', data=dd)
plt.xticks(ticks=[0, 1], labels=['Non-Recession', 'Recession'])
   
plt.title('Vehicle-Wise Sales during Recession and Non-Recession Period')

plt.show()

#TASK 1.4: Use sub plotting to compare the variations in GDP during recession and non-recession period by developing line plots for each period.
df_rec=df[df['Recession']==1]
df_non=df[df['Recession']==0]

df_rec_GDP=df_rec.groupby('Year')['GDP'].sum().reset_index()
df_non_GDP=df_non.groupby('Year')['GDP'].sum().reset_index()

fig, axes= plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
axes[0].plot(df_rec_GDP['Year'], df_rec_GDP['GDP'])
axes[1].plot(df_non_GDP['Year'], df_non_GDP['GDP'])

axes[0].set_title('GDP during during recession period')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Total GDP')

axes[1].set_title('GDP during during non-recession period')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Total GDP')

#TASK 1.5: Develop a Bubble plot for displaying the impact of seasonality on Automobile Sales.
df_non=df[df['Recession']==0]
df_non_month=df_non.groupby(['Month','Seasonality_Weight'])['Automobile_Sales'].mean().reset_index()

plt.figure(figsize=(8,6))
sns.scatterplot(data=df_non_month, x='Month', y='Automobile_Sales', size='Seasonality_Weight', color='blue', alpha=0.5, edgecolor='black')



plt.xlabel('Month')
plt.ylabel('Automobile_Sales')
plt.title('Seasonality impact on Automobile Sales')

plt.show()

#TASK 1.6: Use the functionality of Matplotlib to develop a scatter plot to identify the correlation between average vehicle price relate to the sales volume during recessions.¶
plt.scatter(data=df_rec, x='Price', y='Automobile_Sales',color='red', marker='o', s=50)
plt.title('Relationship between Average Vehicle Price and Sales during Recessions')
plt.xlabel('Price')
plt.ylabel('Automobile_Sales')
plt.show()

#TASK 1.7: Create a pie chart to display the portion of advertising expenditure of XYZAutomotives during recession and non-recession periods.

df_non_exp=df_non['Advertising_Expenditure'].sum()
df_rec_exp=df_rec['Advertising_Expenditure'].sum()

sizes = [df_rec_exp, df_non_exp]

plt.pie(sizes, labels=['Recession', 'Non-recession'], autopct='%1.1f%%', startangle=90 )
plt.title('Advertising expenditure of XYZAutomotives change during recession and non-recession periods')

#TASK 1.8: Develop a pie chart to display the total Advertisement expenditure for each vehicle type during recession period.
df_rec=df[df['Recession']==1]
df_exp_veh=df_rec.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()

sizes=df_exp_veh.values

plt.pie(sizes, labels=['Executive car', 'Medium family car', 'Small familiy car', 'Sports', 'Supperminicar'], autopct='%1.1f%%', startangle=90 )
plt.title('Total Advertisement expenditure for each vehicle type during recession period')

#TASK 1.9: Develop a lineplot to analyse the effect of the unemployment rate on vehicle type and sales during the Recession Period.
df_rec = df[df['Recession']==1]
sns.lineplot(data=df_rec, x='unemployment_rate', y='Automobile_Sales',
             hue='Vehicle_Type', style='Vehicle_Type', markers='o', err_style=None)
plt.ylim(0,850)
plt.legend(loc=(0.05,.3))
