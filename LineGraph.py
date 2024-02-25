# import pandas as pd
# import matplotlib.pyplot as plt
#
# # Read the Excel file
# df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/ave_sen_lenData.xlsx', sheet_name='Sheet1')
#
# # Group by 'column1' and calculate the mean of 'column5' for each group
# grouped = df.groupby('FILENAME')['average_sentence_length'].mean().reset_index()
#
# # Create a multiple line plot
# plt.figure(figsize=(10,   6))
# for index, row in grouped.iterrows():
#     plt.plot(row['FILENAME'], row['average_sentence_length'], label=row['FILENAME'])
# plt.title('Multiple Line Graph from Excel Data')
# plt.xlabel('Names from FILENAME')
# plt.ylabel('Mean of Numbers from average_sentence_length')
# plt.legend()
# plt.grid(True)
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Read the Excel file
df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/CTTRGraphData.xlsx', sheet_name='Sheet1')

# Calculate the average of 'column5' for each group in 'column1'
grouped_avg = df.groupby('FILENAME')[('CTTR')].mean().reset_index()

# Create a new column for the index of each group
grouped_avg['Index'] = range(len(grouped_avg))

# Plot the average values as a line graph
plt.figure(figsize=(10,  6))
plt.plot(grouped_avg['Index'], grouped_avg['CTTR'], marker='o', linestyle='-')

# Customize the plot
plt.title('Line Graph for CCTR Values of SS Files')
plt.xlabel('Group Index')
plt.ylabel('CTTR Valyes')
plt.xticks(grouped_avg['Index'], grouped_avg['FILENAME'], rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)

# Display the plot
plt.show()
