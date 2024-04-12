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

def round_special_values(x):
    if x == 4.5:
        return 5
    elif x == 2.5:
        return 3
    else:
        return round(x)

def main():
    print('\nGive the path for the following files (in .xlsx format): \n')
    print("The CTTR/WDSEN file from program 2.")
    cttr_wdsen_path = input()
    print("\nThe Type Frequency file from program 3.")
    num_words_path = input()
    print("\nThe Lemma Count file from program 1.")
    lem_counts = input()
    print("\nThe output file.")
    excel_file_path = input()


    df1 = pd.read_excel(cttr_wdsen_path, usecols=['FILENAME', 'CTTR', 'WDSEN']) # take values from specified columns in specified files
    df2 = pd.read_excel(num_words_path, usecols=['FILENAME', '100T'])
    df3 = pd.read_excel(lem_counts, usecols=['FILENAME', 'lemmatypes'])

    # merge the two DataFrames on 'FILENAME'
    df = pd.merge(df1, df2, on='FILENAME')
    df = pd.merge(df, df3, on='FILENAME')

    # assign values based on the ranges
    df['CTTRValue'] = df['CTTR'].apply(assign_value, ranges=CTTRRanges)
    df['WDSENValue'] = df['WDSEN'].apply(assign_value, ranges=WDSENRanges)
    df['TypeFreqValue'] = df['100T'].apply(assign_value, ranges=TypeFreqRanges)
    df['LemValue'] = df['lemmatypes'].apply(assign_value, ranges=lemRanges)

    # Calculate the average
    df['GradeValue'] = ((df['CTTRValue'] + df['WDSENValue'] + df['TypeFreqValue'] + df['LemValue'])/4)

    df['RoundGradeValue'] = df['GradeValue'].apply(round_special_values)

    # Define the function to compare grades and output the result
    def compare_and_output(df):
        # Filter rows where FILENAME starts with '01' to '06'
        filtered_df = df[df['FILENAME'].astype(str).str.startswith(('CTX1', 'CTX2', 'CTX3', 'SS01', 'SS02', 'SS03',
                                                                    'SS04', 'SS05', 'SS06', 'TTA', 'TTB', 'TTC', 'TTD',
                                                                    'TTE'))]

        # Create a new column 'DifferenceValue' based on the comparison
        filtered_df.loc[:, 'DifferenceValue'] = filtered_df.apply(
            lambda row: compare_grades(row['RoundGradeValue'], row['FILENAME']), axis=1)

        # Count the occurrences of each difference value
        difference_counts = filtered_df['DifferenceValue'].value_counts()

        # Calculate the percentages
        total_rows = len(filtered_df)
        percentages = {
            'Difference 0': (difference_counts.get(0, 0) / total_rows) * 100,
            'Difference 1': (difference_counts.get(1, 0) / total_rows) * 100,
            'Difference 0 or 1': ((difference_counts.get(0, 0) + difference_counts.get(1, 0)) / total_rows) * 100,
        }

        # Output the percentages
        print("\nPercentage of times the difference is 0: {:.2f}%".format(percentages['Difference 0']))
        print("Percentage of times the difference is 1: {:.2f}%".format(percentages['Difference 1']))
        print("Percentage of times the difference is 0 or 1: {:.2f}%".format(percentages['Difference 0 or 1']))

        # Write the filtered DataFrame to an Excel file
        filtered_df.to_excel(excel_file_path, index=False)

    def compare_grades(rounded_grade_value, filename):
        # Extract the numeric part of the filename prefix after "SS"
        if filename.startswith('CTX'):
            filename_prefix = int(filename[3:4])
        elif filename.startswith('SS'):
            filename_prefix = int(filename[2:4]) # Assuming the prefix is always "SS" followed by a number
        else:
            prefix_to_value = {
                'TTA': 1,
                'TTB': 2,
                'TTC': 3,
                'TTD': 4,
                'TTE': 5
            }
            filename_prefix = prefix_to_value.get(filename[:3], 0)

        # Compare the rounded grade value with the numeric part of the filename prefix
        if rounded_grade_value>filename_prefix:
            difference = abs(rounded_grade_value - filename_prefix)
        else:
            difference = abs(filename_prefix - rounded_grade_value)

        return difference

    # Example usage:
    compare_and_output(df)

    print('\nThe results have also been outputted to ' + excel_file_path + ' displaying the values used.\n')

if __name__ == "__main__":
    main()
