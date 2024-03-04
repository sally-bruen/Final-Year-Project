# import pandas as pd
#
# def assign_value(value,filename):
#     if filename.startswith()
#
#
# cttr_wdsen_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/GradingofTexts.xlsx'
#
# df = pd.read_excel(cttr_wdsen_path, usecols=['FILENAME', 'RoundedGradeValue'])
#
# df['RGradeValue'] = df['RoundedGradeVale'].apply(assign_value,'FILENAME')

import pandas as pd

def compare_and_output(input_excel, output_excel):
    # Read the input Excel file
    df = pd.read_excel(input_excel)

    # Filter rows where FILENAME starts with '01' to '06'
    filtered_df = df[df['FILENAME'].astype(str).str.startswith(('01', '02', '03', '04', '05', '06'))]

    # Create a new column 'DifferenceValue' based on the comparison
    filtered_df['DifferenceValue'] = filtered_df.apply(
        lambda row: compare_grades(row['RoundGradeValue'], row['FILENAME']), axis=1)

    # Keep only 'FILENAME' and 'DifferenceValue' columns
    output_df = filtered_df[['FILENAME', 'DifferenceValue']]

    # Write the updated DataFrame to a new Excel file
    output_df.to_excel(output_excel, index=False)

def compare_grades(rounded_grade_value, filename):
    # Extract the prefix of the filename
    filename_prefix = filename[:2]

    # Compare the rounded grade value with the filename prefix
    difference = abs(rounded_grade_value - int(filename_prefix))

    if difference == 0:
        return 0
    elif difference == 1:
        return 1
    elif difference == 2:
        return 2
    elif difference == 3:
        return 3
    elif difference == 4:
        return 4
    elif difference == 5:
        return 5
    elif difference == 6:
        return 6
    else:
        # If the difference is greater than 6, you can handle it as needed
        return "Difference greater than 6"

# Example usage:
input_excel_file = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/GradingofTexts.xlsx'  # Replace with the actual input file path
output_excel_file = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/PercentAccuracy.xlsx'  # Replace with the desired output file path

compare_and_output(input_excel_file, output_excel_file)
