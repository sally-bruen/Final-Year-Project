import pandas as pd
import matplotlib.pyplot as plt

# Read the Excel file
df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/AllTextMeasures.xlsx', sheet_name='Sheet1')

# Create a scatter plot with all data points
plt.scatter(df['FILENAME'], df['CTTR'], marker="o", s=50, alpha=0.5)

# Customize the plot
plt.title('Scatter Plot for CTTR Values of All Files')
plt.xlabel('File Names from FILENAME')
plt.ylabel('Data from CTTR')
plt.grid(True)

# Display the plot
plt.show()
