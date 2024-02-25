# # # import pandas as pd
# # # import matplotlib.pyplot as plt
# # #
# # # #Read the Excel file
# # # df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/PractiseGraphData.xlsx', sheet_name='Sheet1')
# # #
# # # #extract data from the columns
# # # filenames = df['FILENAME']
# # # numbers = df['CTTR']
# # #
# # # #iterate over unique names and plot a line for each
# # # for name in filenames.unique():
# # #     plt.plot(numbers[filenames == name], label=name)
# # #
# # # #set up the plot
# # # plt.title('Line Graph with File Names as X-Axis Labels')
# # # plt.xlabel('File Names from FILENAME')
# # # plt.ylabel('Data from CTTR')
# # # plt.legend() #show legend with the names
# # # plt.grid(True)
# # # plt.show()
# # #
# # # import pandas as pd
# # # import matplotlib.pyplot as plt
# # #
# # # # Read the Excel file
# # # df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/PractiseGraphData.xlsx', sheet_name='Sheet1')
# # #
# # # # Extract the data for the x and y axes
# # # x_data = df['FILENAME']
# # # y_data = df['CTTR']
# # #
# # #
# # # # Create a scatter plot
# # # plt.figure(figsize=(10,  10))
# # # plt.scatter(x_data, y_data, marker="o", s=50, alpha=0.5)
# # #
# # # # Customize the plot
# # # plt.title('Cluster Plot from Excel Data')
# # # plt.xlabel('Data from FILENAME')
# # # plt.ylabel('Data from CTTR')
# # # plt.grid(True)
# # #
# # # # Display the plot
# # # plt.show()
# #
# # import pandas as pd
# # import matplotlib.pyplot as plt
# #
# # # Read the Excel file
# # df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/CTTRGraphData.xlsx', sheet_name='Sheet1')
# #
# # # Define a dictionary mapping filename prefixes to colors
# # filename_prefix_to_color = {
# #     '01': 'red',
# #     '02': 'blue',
# #     '03': 'green',
# #     '04': 'purple',
# #     '05': 'orange',
# #     '06': 'pink',
# #     '07': 'grey',
# #     '08': 'yellow'
# #     # Add more mappings as needed
# # }
# #
# # # Get the list of unique filename prefixes
# # unique_prefixes = df['FILENAME'].str[:2].unique()
# #
# #
# # # Function to map a filename to a color
# # def get_color(filename):
# #     return filename_prefix_to_color.get(filename[:2], 'black')
# #
# #
# # # Create a scatter plot with different colors based on the filename prefix
# # for prefix in unique_prefixes:
# #     # Filter the DataFrame by the current filename prefix
# #     subset_df = df[df['FILENAME'].str.startswith(prefix)]
# #
# #     # Plot the subset with the corresponding color
# #     plt.scatter(subset_df['FILENAME'], subset_df['CTTR'], c=get_color(prefix), label=prefix)
# #
# # # Customize the plot
# # plt.title('Cluster Plot for CTTR Values')
# # plt.xlabel('Data from FILENAME')
# # plt.ylabel('Data from CTTR')
# # plt.legend()  # Show legend with the filename prefixes
# # plt.grid(True)
# #
# # # Display the plot
# # plt.show()
#
#
#
#
# import pandas as pd
# import matplotlib.pyplot as plt
#
# # Read the Excel file
# df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/AllTextMeasures.xlsx', sheet_name='Sheet1')
#
# # Define a dictionary mapping filename prefixes to colors
# filename_prefix_to_color = {
#     '01': 'red',
#     '02': 'blue',
#     '03': 'green',
#     '04': 'purple',
#     '05': 'orange',
#     '06': 'pink',
#     '07': 'grey',
#     '08': 'black',
#     'A_': 'red',
#     'B_': 'blue',
#     'C_': 'green',
#     'D_': 'purple',
#     'E_': 'orange'
#     # Add more mappings as needed
# }
#
# # Get the list of unique filename prefixes
# unique_prefixes = df['FILENAME'].str[:2].unique()
#
# # Function to map a filename to a color
# def get_color(filename):
#     return filename_prefix_to_color.get(filename[:2], 'black')
#
# # Create a scatter plot with different colors based on the filename prefix
# for prefix in unique_prefixes:
#     # Filter the DataFrame by the current filename prefix
#     subset_df = df[df['FILENAME'].str.startswith(prefix)]
#
#     # Plot the subset with the corresponding color
#     plt.scatter(subset_df['FILENAME'], subset_df['CTTR'], c=get_color(prefix), label=prefix)
#
# # Customize the plot
# plt.title('Cluster Plot of CTTR of All Files')
# plt.ylabel('Data from CTTR Values')
# plt.xlabel('File Prefixes')
# #plt.legend()  # Show legend with the filename prefixes
# plt.grid(True)
#
# # Display the plot
# plt.show()


import pandas as pd
import matplotlib.pyplot as plt

# Read the Excel file
df = pd.read_excel('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/AllTextMeasures.xlsx', sheet_name='Sheet1')

# Define a function to extract the prefix from the filename
def get_prefix(filename):
    return filename.split('_')[0]

# Group by the filename prefix and calculate the average of the 'CTTR' column
grouped_df = df.groupby(df['FILENAME'].apply(get_prefix)).mean()

# Plot the averages
plt.figure(figsize=(10,  6))
for group, avg_values in grouped_df.iteritems():
    plt.plot(avg_values['CTTR'], label=group)

# Customize the plot
plt.title('Average CTTR Values by File Prefix')
plt.ylabel('Average CTTR')
plt.xlabel('File Prefixes')
plt.grid(True)
plt.legend(bbox_to_anchor=(1.05,  1), loc='upper left')

# Display the plot
plt.show()
