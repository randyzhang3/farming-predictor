import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
data = pd.read_csv("Total_Corn_Yield_Per_Acre_of_Land.csv")

# Extract the columns you want to plot
xpoints = data['Year']
ypoints = data['Value']
yAsList = []
for i in ypoints:
    x = int(i.replace(',', ''))
    yAsList.append(x)

# Create a line plot
plt.plot(xpoints, yAsList)

# Add labels
plt.xlabel('Year')
plt.ylabel('Value')

# Show the plot
plt.show()
