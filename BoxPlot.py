import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Read data from Excel file
df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllTextMeasures.xlsx')

# Function to extract the prefix from the filename
def get_prefix(filename):
    return filename.split('_')[0]

# Group data by filename prefix and calculate averages and standard deviations
grouped_data = defaultdict(list)
for index, row in df.iterrows():
    file_name = row['FILENAME']
    prefix = get_prefix(file_name)
    # Select column 5 for average sentence length
    sentence_length = row.iloc[3] # Use iloc to avoid FutureWarning
    grouped_data[prefix].append(sentence_length)

# Prepare data for plotting
data_for_boxplot = [grouped_data[prefix] for prefix in grouped_data]

# Create the box plot
plt.boxplot(data_for_boxplot, patch_artist=True, notch=True, vert=1, widths=0.6)

# Adding labels and title
plt.xlabel('Prefixed Filename')
plt.ylabel('CTTR Values')
plt.title('Box Plot of CTTR Values for TT Files')
plt.grid(True)
plt.subplots_adjust(left=0.1, right=0.85)
plt.xticks(range(1, len(grouped_data) + 1), list(grouped_data.keys()))

# Display the plot
plt.show()
