# # import pandas as pd
# # import matplotlib.pyplot as plt
# # from collections import defaultdict
# #
# # # Read data from Excel file
# # df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/Book4.xlsx')
# #
# # # Function to extract the prefix from the filename
# # def get_prefix(filename):
# #     return filename.split('_')[0]
# #
# # # Group data by filename prefix and calculate averages and standard deviations
# # grouped_data = defaultdict(lambda: {'sum':   0, 'count':   0, 'squared_sum':   0})
# # for index, row in df.iterrows():
# #     file_name = row['FILENAME']
# #     prefix = get_prefix(file_name)
# #     # Select columns starting from the   11th column
# #     frequencies = row.iloc[5].values
# #     grouped_data[prefix]['sum'] += frequencies.sum()
# #     grouped_data[prefix]['count'] += len(frequencies)
# #     grouped_data[prefix]['squared_sum'] += (frequencies**2).sum()
# #
# # average_frequencies = {}
# # standard_deviations = {}
# # for prefix, data in grouped_data.items():
# #     n = data['count']
# #     mean = data['sum'] / n
# #     variance = (data['squared_sum'] / n) - (mean**2)
# #     std_dev = variance**0.5
# #     average_frequencies[prefix] = mean
# #     standard_deviations[prefix] = std_dev
# #
# # # Extract data for x-axis (Word Count) and y-axis (Average Frequencies)
# # # Get the column names starting from the   11th column
# # word_count_ranges = df.columns[5]
# # for prefix, avg_freq in average_frequencies.items():
# #     # Calculate the average frequency for each word count range
# #     avg_freq_per_range = [avg_freq / len(word_count_ranges)] * len(word_count_ranges)
# #     plt.errorbar(word_count_ranges, avg_freq_per_range, yerr=standard_deviations[prefix], fmt='o', capsize=5, label=prefix)
# #
# # # Adding labels and title
# # plt.xlabel('Word Count Ranges')
# # plt.ylabel('Average Frequencies')
# # plt.title('Error Bar Graph of Average Frequencies for Word Count Ranges')
# # plt.grid(True)
# # plt.legend()
# #
# # # Display the plot
# # plt.show()
#
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Read data from Excel file
df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/AllTextStats.xlsx')

# Function to extract the prefix from the filename
def get_prefix(filename):
    return filename.split('_')[0]

# Group data by filename prefix and calculate averages and standard deviations
grouped_data = defaultdict(lambda: {'sum':  0, 'count':  0, 'squared_sum':  0})
for index, row in df.iterrows():
    file_name = row['FILENAME']
    prefix = get_prefix(file_name)
    # Select column   5 for average sentence length
    sentence_length = row.iloc[5]  # Use iloc to avoid FutureWarning
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
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Adjust the list as needed

# Create the error bar chart with different colors for each bar
for i, (prefix, avg_length, std_dev) in enumerate(zip(prefixes, avg_lengths, std_devs)):
    plt.errorbar(i, avg_length, yerr=std_dev, fmt='o', capsize=5, color=colors[i % len(colors)], label=prefix)

# Adding labels and title
plt.xlabel('Prefixed Filename')
plt.ylabel('Average Sentence Length')
plt.title('Error Bar Chart of Average Sentence Lengths for All Files')
plt.grid(True)
#plt.legend()  # Legend will now work because we've assigned labels to the plot elements

plt.legend(bbox_to_anchor=(0.95,   1), loc='upper left')
# Display the plot
plt.show()




# import pandas as pd
# import matplotlib.pyplot as plt
# from collections import defaultdict
#
# # Read data from Excel file
# df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/ave_sen_lenData.xlsx')
#
# # Function to extract the prefix from the filename
# def get_prefix(filename):
#     return filename.split('_')[0]
#
# # Group data by filename prefix and calculate averages and standard deviations
# grouped_data = defaultdict(lambda: {'sum': 0, 'count': 0, 'squared_sum': 0})
# for index, row in df.iterrows():
#     file_name = row['FILENAME']
#     prefix = get_prefix(file_name)
#     # Select column   5 for average sentence length
#     sentence_length = row[5]
#     grouped_data[prefix]['sum'] += sentence_length
#     grouped_data[prefix]['count'] +=  1
#     grouped_data[prefix]['squared_sum'] += sentence_length**2
#
# average_sentence_lengths = {}
# standard_deviations = {}
# for prefix, data in grouped_data.items():
#     n = data['count']
#     mean = data['sum'] / n
#     variance = (data['squared_sum'] / n) - (mean**2)
#     std_dev = variance**0.5
#     average_sentence_lengths[prefix] = mean
#     standard_deviations[prefix] = std_dev
#
# # Prepare data for plotting
# prefixes = list(average_sentence_lengths.keys())
# avg_lengths = list(average_sentence_lengths.values())
# std_devs = list(standard_deviations.values())
#
# # Create the error bar chart
# plt.errorbar(prefixes, avg_lengths, yerr=std_devs, fmt='o', capsize=5)
#
# # Adding labels and title
# plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
# plt.xlabel('Prefixed Filename')
# plt.ylabel('Average Sentence Length')
# plt.title('Error Bar Chart of Average Sentence Lengths')
# plt.grid(True)
# plt.legend().remove()  # Remove the legend since we're using labels on the x-axis
#
# # Display the plot
# plt.show()




# import pandas as pd
# import matplotlib.pyplot as plt
# from collections import defaultdict
#
# # Read data from Excel file
# df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/Book4.xlsx')
#
# # Function to extract the prefix from the filename
# def get_prefix(filename):
#     return filename.split('_')[0]
#
# # Group data by filename prefix and calculate averages and standard deviations
# grouped_data = defaultdict(lambda: {'sum':   0, 'count':   0, 'squared_sum':   0})
# for index, row in df.iterrows():
#     file_name = row['FILENAME']
#     prefix = get_prefix(file_name)
#     # Select column   5 for average sentence length using iloc
#     sentence_length = row.iloc[5]
#     grouped_data[prefix]['sum'] += sentence_length
#     grouped_data[prefix]['count'] +=   1
#     grouped_data[prefix]['squared_sum'] += sentence_length**2
#
# average_sentence_lengths = {}
# standard_deviations = {}
# for prefix, data in grouped_data.items():
#     n = data['count']
#     mean = data['sum'] / n
#     variance = (data['squared_sum'] / n) - (mean**2)
#     std_dev = variance**0.5
#     average_sentence_lengths[prefix] = mean
#     standard_deviations[prefix] = std_dev
#
# # Prepare data for plotting
# prefixes = list(average_sentence_lengths.keys())
# avg_lengths = list(average_sentence_lengths.values())
# std_devs = list(standard_deviations.values())
#
# # Create the error bar chart
# for i, (prefix, avg_length, std_dev) in enumerate(zip(prefixes, avg_lengths, std_devs)):
#     plt.errorbar(i, avg_length, yerr=std_dev, fmt='o', capsize=5, label=prefix)
#
# # Adding labels and title
# plt.xticks(range(len(prefixes)), prefixes, rotation=45)  # Set x-tick labels and rotate for readability
# plt.xlabel('Prefixed Filename')
# plt.ylabel('Average Sentence Length')
# plt.title('Error Bar Chart of Average Sentence Lengths')
# plt.grid(True)
# plt.legend()  # Legend will now work because we've assigned labels to the plot elements
#
# # Display the plot
# plt.show()
