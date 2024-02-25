import pandas as pd
import matplotlib.pyplot as plt

# Read the Excel file
df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/ave_sen_lenData.xlsx', sheet_name='Sheet1')

# Define a dictionary mapping filename prefixes to colors
filename_prefix_to_color = {
    '01': 'red',
    '02': 'blue',
    '03': 'green',
    '04': 'purple',
    '05': 'orange',
    '06': 'pink',
    'A_': 'red',
    'B_': 'blue',
    'C_': 'green',
    'D_': 'purple',
    'E_': 'orange'
    # Add more mappings as needed
}

# Get the list of unique filename prefixes
unique_prefixes = df['FILENAME'].str[:2].unique()


# Function to map a filename to a color
def get_color(filename):
    return filename_prefix_to_color.get(filename[:2], 'black')


# Create a scatter plot with different colors based on the filename prefix
for prefix in unique_prefixes:
    # Filter the DataFrame by the current filename prefix
    subset_df = df[df['FILENAME'].str.startswith(prefix)]

    # Plot the subset with the corresponding color
    plt.scatter(subset_df['FILENAME'], subset_df['average_sentence_length'], c=get_color(prefix), label=prefix)

# Customize the plot
plt.title('Cluster Plot for Average Sentence Length of All Files')
plt.xlabel('Data from FILENAME')
plt.ylabel('Data from Sentence Length')
#plt.legend()  # Show legend with the filename prefixes
plt.grid(True)


# plt.legend(bbox_to_anchor=(1.05,  1), loc='upper left')

# Display the plot
plt.show()
