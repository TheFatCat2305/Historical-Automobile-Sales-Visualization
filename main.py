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

