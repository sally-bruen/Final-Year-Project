import pandas as pd

# Define the ranges for CTTR, WDSEN, and TypeFreq
#CTTRRanges = [(1, 5), (4, 7.6), (7.6, 8.6), (8.6, 10), (9, 15)]
#WDSENRanges = [(0, 8), (8, 9), (9, 12), (12, 13), (13, 14), (14, 20)]
#TypeFreqRanges = [(40, 100), (25, 40), (19, 25), (13, 19), (10, 13), (0, 13)]
#lemRanges = [(0, 100), (100, 200), (200, 300), (300, 500), (500, 650), (650, 2000)]

# Function to assign a value based on the range
# def assign_value(value, ranges):
#     for i, (range_start, range_end) in enumerate(ranges):
#         if range_start <= value <= range_end:
#             return i + 1 # Assuming band 1 is the first range
#     return 0 # Default value if no match

def assign_sen_value(value):
    if value > 20:
        value = 1.5
        return value
    else: return 0
# Read the Excel files
wdsen_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllTextMeasures.xlsx'
num_words_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllWordFrequency.xlsx'
lem_counts = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllTextStats.xlsx'

df1 = pd.read_excel(wdsen_path, usecols=['FILENAME', 'WDSEN'])
df2 = pd.read_excel(num_words_path, usecols=['FILENAME', '10KplusW'])
#df3 = pd.read_excel(lem_counts, usecols=['FILENAME', 'lemtypes'])

# Merge the two DataFrames on 'FILENAME'
df = pd.merge(df1, df2, on='FILENAME')
#df = pd.merge(df, df3, on='FILENAME')

# Assign values based on the ranges
#df['CTTRValue'] = df['CTTR'].apply(assign_value, ranges=CTTRRanges)
df['WDSENValue'] = df['WDSEN'].apply(assign_sen_value)
df['TypeFreqValue'] = df['10KplusW']
#df['LemValue'] = df['lemtypes'].apply(assign_value, ranges=lemRanges)

# Calculate the average of CTTR, WDSEN, and TypeFreq values
df['GradeValue'] = ((df['WDSENValue'] + df['TypeFreqValue']))
df['RoundGradeValue'] = round(df['GradeValue'])
# Prepare the output DataFrame
output_df = df[['FILENAME', 'WDSEN', '10KplusW', 'WDSENValue', 'TypeFreqValue', 'GradeValue', 'RoundGradeValue']]

# Write the results to a new Excel file
output_df.to_excel('/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/GradingofTexts.xlsx', index=False)
