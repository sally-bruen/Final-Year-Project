import pandas as pd
import matplotlib.pyplot as plt

# Read data from Excel file
df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/SSTextFrequency.xlsx')

# Divide each column by column B
for col in df.columns:
    if col != 'TYPES':  # Assuming 'B' is the column you want to divide by
        df[col] = df[col] / df['TYPES']

# Group by the filename prefix and calculate the average of the divided values
grouped_data = df.groupby(df['FILENAME'].apply(lambda x: x.split('_')[0]))
average_values = grouped_data.mean()

# Plot the averages
plt.figure(figsize=(10,  6))
for group, avg_values in average_values.iteritems():
    plt.plot(avg_values, label=group)

# Adding labels and title
plt.xlabel('Columns')
plt.ylabel('Average of Divided Values')
plt.title('Line Plot for Divided Values Averages')
plt.grid(True)
plt.legend(bbox_to_anchor=(1.05,  1), loc='upper left')

# Display the plot
plt.show()
