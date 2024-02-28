import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Read data from Excel file
df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllTypeFrequency.xlsx')

# Function to extract the prefix from the filename
def get_prefix(filename):
    return filename.split('_')[0]

# Group data by filename prefix and calculate averages
grouped_data = defaultdict(list)
for index, row in df.iterrows():
    file_name = row['FILENAME']
    prefix = get_prefix(file_name)
    # Drop the  14th column and keep the rest starting from the  13th column
    frequencies = row[2:11]
    grouped_data[prefix].append(frequencies)

average_frequencies = {prefix: sum(freqs)/len(freqs) for prefix, freqs in grouped_data.items()}

# Extract data for x-axis (Word Count) and y-axis (Average Frequencies)
# Get the column names excluding the  14th column
word_count_ranges = df.columns[2:11]  # Exclude the last column
for prefix, avg_freq in average_frequencies.items():
    plt.plot(word_count_ranges, avg_freq, label=prefix, marker='o')

# Adding labels and title
plt.xlabel('Word Frequency Ranges')
plt.ylabel('Percentage of Types in Frequencies %')
plt.title('Line Plot for Percentage of Word Frequencies/Types in SS & CT Files')
plt.grid(True)
#plt.legend()

plt.subplots_adjust(left=0.15, right=0.85)
plt.legend(bbox_to_anchor=(0.97,   1), loc='upper left')
# Display the plot
plt.show()
