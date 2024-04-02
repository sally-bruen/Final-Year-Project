import pandas as pd

# Define the ranges for CTTR, WDSEN, TypeFreq and lemmas
CTTRRanges = [(1, 4.7), (4.7, 7.4), (7.4, 8.7), (8.7, 10.6), (10.6, 11), (11, 100)]
WDSENRanges = [(0, 7.6), (7.6, 9.8), (9.8, 11.1), (11.1, 12.8), (12.8, 14.6), (14.6, 100)]
TypeFreqRanges = [(40.7, 100), (25.5, 40.7), (19, 25.5), (15, 19), (12, 15), (0, 12)]
lemRanges = [(0, 107), (107, 276), (276, 312), (312, 510), (510, 720), (650, 2000)]

# assign a value based on the range
def assign_value(value, ranges):
    for i, (range_start, range_end) in enumerate(ranges):
        if range_start <= value <= range_end:
            return i + 1
    return 0


cttr_wdsen_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllTextMeasures.xlsx'   # path to cttr/wdsen .xlsx file
num_words_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllTypeFrequency.xlsx'   # path to type frequency file
lem_counts = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllTextStats.xlsx'           # path to lemma count file

df1 = pd.read_excel(cttr_wdsen_path, usecols=['FILENAME', 'CTTR', 'WDSEN']) # take values from specified columns in specified files
df2 = pd.read_excel(num_words_path, usecols=['FILENAME', '100T'])
df3 = pd.read_excel(lem_counts, usecols=['FILENAME', 'lemtypes'])

# merge the two DataFrames on 'FILENAME'
df = pd.merge(df1, df2, on='FILENAME')
df = pd.merge(df, df3, on='FILENAME')

# assign values based on the ranges
df['CTTRValue'] = df['CTTR'].apply(assign_value, ranges=CTTRRanges)
df['WDSENValue'] = df['WDSEN'].apply(assign_value, ranges=WDSENRanges)
df['TypeFreqValue'] = df['100T'].apply(assign_value, ranges=TypeFreqRanges)
df['LemValue'] = df['lemtypes'].apply(assign_value, ranges=lemRanges)

# Calculate the average
df['GradeValue'] = ((df['CTTRValue'] + df['WDSENValue'] + df['TypeFreqValue'] + df['LemValue'])/4)
df['RoundGradeValue'] = round(df['GradeValue'])

# Define the function to compare grades and output the result
def compare_and_output(df):
    # Filter rows where FILENAME starts with '01' to '06'
    filtered_df = df[df['FILENAME'].astype(str).str.startswith(('01', '02', '03', '04', '05', '06'))]

    # Create a new column 'DifferenceValue' based on the comparison
    filtered_df['DifferenceValue'] = filtered_df.apply(lambda row: compare_grades(row['RoundGradeValue'], row['FILENAME']), axis=1)

    # Count the occurrences of each difference value
    difference_counts = filtered_df['DifferenceValue'].value_counts()

    # Calculate the percentages
    total_rows = len(filtered_df)
    percentages = {
        'Difference 0': (difference_counts.get(0, 0) / total_rows) * 100,
        'Difference 1': (difference_counts.get(1, 0) / total_rows) * 100,
        'Difference 0 or 1': ((difference_counts.get(0, 0) + difference_counts.get(1, 0)) / total_rows) * 100,
        'Difference 2': (difference_counts.get(2, 0) / total_rows) * 100
    }

    # Output the percentages
    print("Percentage of times the difference is 0: {:.2f}%".format(percentages['Difference 0']))
    print("Percentage of times the difference is 1: {:.2f}%".format(percentages['Difference 1']))
    print("Percentage of times the difference is 0 or 1: {:.2f}%".format(percentages['Difference 0 or 1']))
    print("Percentage of times the difference is 2: {:.2f}%".format(percentages['Difference 2']))

    # Write the filtered DataFrame to an Excel file
    filtered_df.to_excel('/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/OutputWithDifferences.xlsx', index=False)

def compare_grades(rounded_grade_value, filename):
    # Extract the prefix of the filename
    filename_prefix = filename[:2]

    # Compare the rounded grade value with the filename prefix
    difference = abs(rounded_grade_value - int(filename_prefix))

    return difference

# Example usage:
compare_and_output(df)
