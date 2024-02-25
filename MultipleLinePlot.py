# # # # import pandas as pd
# # # # import matplotlib.pyplot as plt
# # # #
# # # # # Read data from Excel file
# # # # df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/Book4.xlsx')
# # # #
# # # # # Extract data for x-axis (Word Count) and y-axis (Frequencies) for each file
# # # # word_count_ranges = df.columns[10:]
# # # # for index, row in df.iterrows():
# # # #     file_name = row['FILENAME']
# # # #     frequencies = row[10:]
# # # #
# # # #     # Plotting
# # # #     plt.plot(word_count_ranges, frequencies, label=file_name, marker='o')
# # # #
# # # # # Adding labels and title
# # # # plt.xlabel('Word Count Ranges')
# # # # plt.ylabel('Frequencies')
# # # # plt.title('Line Plot of Frequencies for Word Count Ranges')
# # # # plt.grid(True)
# # # # plt.legend()
# # # #
# # # # # Display the plot
# # # # plt.show()
# # #
# # # import pandas as pd
# # # import matplotlib.pyplot as plt
# # # from collections import defaultdict
# # #
# # # # Read data from Excel file
# # # df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/Book4.xlsx')
# # #
# # # # Function to extract the prefix from the filename
# # # def get_prefix(filename):
# # #     return '_'.join(filename.split('_')[:2])
# # #
# # # # Group data by filename prefix and calculate averages
# # # grouped_data = defaultdict(list)
# # # for index, row in df.iterrows():
# # #     file_name = row['FILENAME']
# # #     prefix = get_prefix(file_name)
# # #     frequencies = row[10:].values
# # #     grouped_data[prefix].append(frequencies)
# # #
# # # average_frequencies = {prefix: sum(freqs)/len(freqs) for prefix, freqs in grouped_data.items()}
# # #
# # # # Extract data for x-axis (Word Count) and y-axis (Average Frequencies)
# # # word_count_ranges = df.columns[10:]
# # # for prefix, avg_freq in average_frequencies.items():
# # #     plt.plot(word_count_ranges, avg_freq, label=prefix, marker='o')
# # #
# # # # Adding labels and title
# # # plt.xlabel('Word Count Ranges')
# # # plt.ylabel('Average Frequencies')
# # # plt.title('Line Plot of Average Frequencies for Word Count Ranges')
# # # plt.grid(True)
# # # plt.legend()
# # #
# # # # Display the plot
# # # plt.show()
# #
# # import pandas as pd
# # import matplotlib.pyplot as plt
# # from collections import defaultdict
# #
# # # Read data from Excel file
# # df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/Book4.xlsx')
# #
# # # Group data by filename and calculate averages
# # grouped_data = defaultdict(list)
# # for index, row in df.iterrows():
# #     file_name = row['FILENAME']
# #     frequencies = row[10:].values
# #     grouped_data[file_name].append(frequencies)
# #
# # average_frequencies = {file_name: sum(freqs)/len(freqs) for file_name, freqs in grouped_data.items()}
# #
# # # Extract data for x-axis (Word Count) and y-axis (Average Frequencies)
# # word_count_ranges = df.columns[10:]
# # for file_name, avg_freq in average_frequencies.items():
# #     plt.plot(word_count_ranges, avg_freq, label=file_name, marker='o')
# #
# # # Adding labels and title
# # plt.xlabel('Word Count Ranges')
# # plt.ylabel('Average Frequencies')
# # plt.title('Line Plot of Average Frequencies for Word Count Ranges')
# # plt.grid(True)
# # plt.legend()
# #
# # # Display the plot
# # plt.show()
#
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
# # Group data by filename prefix and calculate averages
# grouped_data = defaultdict(list)
# for index, row in df.iterrows():
#     file_name = row['FILENAME']
#     prefix = get_prefix(file_name)
#     frequencies = row[11:].values
#     grouped_data[prefix].append(frequencies)
#
# average_frequencies = {prefix: sum(freqs)/len(freqs) for prefix, freqs in grouped_data.items()}
#
# # Extract data for x-axis (Word Count) and y-axis (Average Frequencies)
# word_count_ranges = df.columns[11:]
# for prefix, avg_freq in average_frequencies.items():
#     plt.plot(word_count_ranges, avg_freq, label=prefix, marker='o')
#
# # Adding labels and title
# plt.xlabel('Word Count Ranges')
# plt.ylabel('Average Frequencies')
# plt.title('Line Plot of Average Frequencies for Word Count Ranges')
# plt.grid(True)
# plt.legend()
#
# # Display the plot
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Read data from Excel file
df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/AllTextFrequency.xlsx')

# Function to extract the prefix from the filename
def get_prefix(filename):
    return filename.split('_')[0]

# Group data by filename prefix and calculate averages
grouped_data = defaultdict(list)
for index, row in df.iterrows():
    file_name = row['FILENAME']
    prefix = get_prefix(file_name)
    # Drop the  14th column and keep the rest starting from the  13th column
    frequencies = row[13:]
    grouped_data[prefix].append(frequencies)

average_frequencies = {prefix: sum(freqs)/len(freqs) for prefix, freqs in grouped_data.items()}

# Extract data for x-axis (Word Count) and y-axis (Average Frequencies)
# Get the column names excluding the  14th column
word_count_ranges = df.columns[13:]  # Exclude the last column
for prefix, avg_freq in average_frequencies.items():
    plt.plot(word_count_ranges, avg_freq, label=prefix, marker='o')

# Adding labels and title
plt.xlabel('Words in Frequency Ranges / Total Types')
plt.ylabel('Percentage of Frequencies %')
plt.title('Line Plot for Percentage of Word Frequencies / Types in All Files')
plt.grid(True)
#plt.legend()

plt.legend(bbox_to_anchor=(0.95,   1), loc='upper left')
# Display the plot
plt.show()
