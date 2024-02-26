import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Read data from Excel file
file_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllTextStats.xlsx'
df = pd.read_excel(file_path)

# Function to extract the prefix from the filename
def get_prefix(filename):
    return filename.split('_')[0]

# Group data by filename prefix and calculate averages and standard deviations
grouped_data = defaultdict(lambda: {'sum': 0, 'count': 0, 'squared_sum': 0})
for _, row in df.iterrows():
    file_name = row['FILENAME']
    prefix = get_prefix(file_name)
    # Select column 5 for average sentence length
    sentence_length = row.iloc[5]  # Use iloc to avoid FutureWarning
    grouped_data[prefix]['sum'] += sentence_length
    grouped_data[prefix]['count'] += 1
    grouped_data[prefix]['squared_sum'] += sentence_length**2

average_sentence_lengths = {}
standard_deviations = {}
for prefix, data in grouped_data.items():
    n = data['count']
    mean = data['sum'] / n
    variance = (data['squared_sum'] / n) - (mean**2)
    std_dev = variance**0.5
    average_sentence_lengths[prefix] = mean
    standard_deviations[prefix] = std_dev

# Prepare data for plotting
prefixes = list(average_sentence_lengths.keys())
avg_lengths = list(average_sentence_lengths.values())
std_devs = list(standard_deviations.values())

# Define a list of colors for the bars
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'b', 'g', 'r', 'c', 'm', 'y', 'k']  # Adjust the list as needed

# Create the error bar chart with different colors for each bar
for i, (prefix, avg_length, std_dev) in enumerate(zip(prefixes, avg_lengths, std_devs)):
    plt.errorbar(i, avg_length, yerr=std_dev, fmt='o', capsize=5, color=colors[i % len(colors)])

# Adjust the figure's subplot parameters to move the graph to the left
plt.subplots_adjust(left=0.1, right=0.85)  # Example: Set the left margin to 5% of the figure width

# Remove x-axis labels
plt.xticks(range(len(prefixes)), [])

# Display the plot with a title
plt.suptitle('Error Bar Chart of Average Sentence Lengths for All Files', y=1.02)
plt.show()