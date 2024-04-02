import pandas as pd
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

# Merge the two DataFrames on 'FILENAME'
df = pd.merge(df1, df2, on='FILENAME')

# Assign values based on the ranges
df['WDSENValue'] = df['WDSEN'].apply(assign_sen_value)
df['TypeFreqValue'] = df['10KplusW']

# Calculate the average of CTTR, WDSEN, and TypeFreq values
df['GradeValue'] = ((df['WDSENValue'] + df['TypeFreqValue']))
df['RoundGradeValue'] = round(df['GradeValue'])
# Prepare the output DataFrame
output_df = df[['FILENAME', 'WDSEN', '10KplusW', 'WDSENValue', 'TypeFreqValue', 'GradeValue', 'RoundGradeValue']]

# Write the results to a new Excel file
output_df.to_excel('/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/1GradingofTexts.xlsx', index=False)
