import pandas as pd
import numpy as np

def calculate_measures(df):
    # Convert relevant columns to integers
    df['tokens'] = df['tokens'].astype(int)
    df['types'] = df['types'].astype(int)
    df['word_count'] = df['word_count'].astype(int)
    df['sentence_count'] = df['sentence_count'].astype(int)

    # Calculate measures
    df['TTR'] = df['types'] / df['tokens'].where(df['tokens'] > 0, 0)
    df['WTR'] = df['word_count'] / df['types'].where(df['types'] > 0, 0)
    df['CTTR'] = df['types'] / ((np.sqrt(2 * df['word_count']))).where(df['word_count'] > 0, 0)
    df['WDSEN'] = df['word_count'] / df['sentence_count'].where(df['sentence_count'] > 0, 0)

    return df

def process_text_stats(input_file, output_file):
    df = pd.read_excel(input_file)
    df = calculate_measures(df)

    selected_columns = ['FILENAME', 'TTR', 'WTR', 'CTTR', 'WDSEN']
    df_selected = df[selected_columns] # get the columns we want

    df_selected.to_excel(output_file, index=False)

if __name__ == "__main__":
    print("\nGive the path for the input file in .xlsx format containing the basic text statistics.")
    input_file = input()
    print("\nGive the path for the output file in .xlsx format to contain these four text measures.")
    output_file = input()

    process_text_stats(input_file, output_file)
    print('\nThe results have been outputted to ' + output_file + '.\n')
