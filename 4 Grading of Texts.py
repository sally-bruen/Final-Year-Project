import pandas as pd

# Define the ranges for CTTR, WDSEN, TypeFreq and lemmas
CTTRRanges = [(1, 4), (4, 7.6), (7.6, 8.6), (8.6, 9.5), (9.5, 13.5), (13.5, 20)]
WDSENRanges = [(0, 8), (8, 9), (9, 12), (12, 13), (13, 14), (14, 20)]
TypeFreqRanges = [(40, 100), (25, 40), (19, 25), (15, 19), (12, 15), (0, 12)]
lemRanges = [(0, 100), (100, 200), (200, 300), (300, 500), (500, 650), (650, 2000)]

# assign a value based on the range
def assign_value(value, ranges):
    for i, (range_start, range_end) in enumerate(ranges):
        if range_start <= value <= range_end:
            return i + 1 # band 1 is the first range
    return 0 # default value if there's no match

# Read the Excel files
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
df1['CTTRValue'] = df1['CTTR'].apply(assign_value, ranges=CTTRRanges)
df1['WDSENValue'] = df1['WDSEN'].apply(assign_value, ranges=WDSENRanges)
df2['TypeFreqValue'] = df2['100T'].apply(assign_value, ranges=TypeFreqRanges)
df3['LemValue'] = df3['lemtypes'].apply(assign_value, ranges=lemRanges)

# Calculate the average
df1['GradeValue'] = ((df1['CTTRValue'] + df1['WDSENValue'] + df2['TypeFreqValue'] + df3['LemValue'])/4)
df1['RoundGradeValue'] = round(df1['GradeValue'])
# Prepare the output DataFrame
output_df = df1[['FILENAME', 'CTTR', 'WDSEN', 'GradeValue', 'RoundGradeValue']] # output each column to easily see different values

output_df.to_excel('/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/GradingofTexts.xlsx', index=False) # path to output file
