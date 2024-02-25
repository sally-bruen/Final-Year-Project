import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Read data from Excel file
df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/ave_sen_lenData.xlsx')

# Function to extract the prefix and suffix from the filename
def get_prefix_and_suffix(filename):
    parts = filename.split('_')
    return parts[0], parts[1]  # Return a tuple (prefix, suffix)

# Group data by filename prefix and suffix, and calculate averages and standard deviations
grouped_data = defaultdict(lambda: {'sum':   0, 'count':   0, 'squared_sum':   0})
for index, row in df.iterrows():
    file_name = row['FILENAME']
    prefix, suffix = get_prefix_and_suffix(file_name)
    # Select column   5 for average sentence length
    sentence_length = row.iloc[5]  # Use iloc to avoid FutureWarning
    grouped_data[(prefix, suffix)]['sum'] += sentence_length
    grouped_data[(prefix, suffix)]['count'] +=   1
    grouped_data[(prefix, suffix)]['squared_sum'] += sentence_length**2

average_sentence_lengths = {}
standard_deviations = {}
for (prefix, suffix), data in grouped_data.items():
    n = data['count']
    mean = data['sum'] / n
    variance = (data['squared_sum'] / n) - (mean**2)
    std_dev = variance**0.5
    average_sentence_lengths[(prefix, suffix)] = mean
    standard_deviations[(prefix, suffix)] = std_dev

# Prepare data for plotting
groups = list(average_sentence_lengths.keys())
avg_lengths = list(average_sentence_lengths.values())
std_devs = list(standard_deviations.values())

# Define a list of colors for the bars
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Adjust the list as needed

# Create the error bar chart with different colors for each bar
for i, ((prefix, suffix), avg_length, std_dev) in enumerate(zip(groups, avg_lengths, std_devs)):
    plt.errorbar(i, avg_length, yerr=std_dev, fmt='o', capsize=5, color=colors[i % len(colors)])

# Adding labels and title
plt.xticks(range(len(groups)), [f'{p}_{s}' for p, s in groups], rotation=45)  # Set x-tick labels
plt.xlabel('Group')
plt.ylabel('Average Sentence Length')
plt.title('Error Bar Chart of Average Sentence Lengths')
plt.grid(True)

# Display the plot
plt.show()
