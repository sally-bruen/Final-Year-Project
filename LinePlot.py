import pandas as pd
import matplotlib.pyplot as plt

# Read data from Excel file
df = pd.read_excel('data.xlsx')

# Extract data for x-axis (Time) and y-axis (Values)
time = df['FILENAME']
value1 = df['Value1']
value2 = df['Value2']
value3 = df['Value3']

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(time, value1, label='Value1', marker='o')
plt.plot(time, value2, label='Value2', marker='o')
plt.plot(time, value3, label='Value3', marker='o')

# Adding labels and title
plt.xlabel('FILENAME')
plt.ylabel('Values')
plt.title('Multiple Line Plot from Excel Data')
plt.legend()

# Display the plot
plt.show()
