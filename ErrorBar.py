import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Read data from Excel file
df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllTextMeasures.xlsx')

# Function to extract the prefix from the filename
def get_prefix(filename):
    return filename.split('_')[0]

# Group data by filename prefix and calculate averages and standard deviations
grouped_data = defaultdict(lambda: {'sum':  0, 'count':  0, 'squared_sum':  0})
for index, row in df.iterrows():
    file_name = row['FILENAME']
    prefix = get_prefix(file_name)
    # Select column   5 for average sentence length
    sentence_length = row.iloc[3]  # Use iloc to avoid FutureWarning
    grouped_data[prefix]['sum'] += sentence_length
    grouped_data[prefix]['count'] +=   1
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
    plt.errorbar(i, avg_length, yerr=std_dev, fmt='o', capsize=4, color=colors[i % len(colors)], label=prefix)

# Adding labels and title
plt.xlabel('Prefixed Filename')
plt.ylabel('CTTR Values')
plt.title('Error Bar Chart of CTTR Values for TT Files')
plt.grid(True)
#plt.legend()  # Legend will now work because we've assigned labels to the plot elements
plt.subplots_adjust(left=0.1, right=0.85)
plt.xticks(range(len(prefixes)), [])
plt.legend(bbox_to_anchor=(0.97, 1), loc='upper left')
# Display the plot
plt.show()