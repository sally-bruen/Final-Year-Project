import csv
import math
import pandas as pd

def calculate_measures(row):
    # Convert 'types' and 'tokens' to integers
    tokens = int(row['tokens'])
    types = int(row['types'])
    words = int(row['word_count'])
    sens = int(row['sentence_count'])

    # Calculate measures
    ttr = types / tokens if tokens > 0 else 0
    wtr = words / types if types > 0 else 0
    cttr = types / (math.sqrt(2 * words)) if words > 0 else 0
    wdsen = words / sens if sens > 0 else 0

    return {
        'FILENAME': row['FILENAME'],
        'TTR': ttr,
        'WTR': wtr,
        'CTTR': cttr,
        'WDSEN': wdsen
        # Add more measures as needed
    }

def process_text_stats(input_file, output_file):
    df = pd.read_excel(input_file)

    measures_list = []
    for _, row in df.iterrows():
        measures = calculate_measures(row)
        measures_list.append(measures)

    measures_df = pd.DataFrame(measures_list)

    measures_df.to_excel(output_file, index=False)


if __name__ == "__main__":
    input_file = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllTextStats.xlsx'
    output_file = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllTextMeasures.xlsx'
    process_text_stats(input_file, output_file)