import os
import csv
from collections import defaultdict
import pandas as pd

type_ranges = [(101, '100T'), (201, '200T'), (301, '300T'), (401, '400T'), (501, '500T')]

def process_file(filename, wordlist):
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        # Extract values from the first column
        text = [row[0] for row in reader]


    types = []
    type_counts = defaultdict(int)
    unwanted_values = {' ','...','–','','‘',',','.','’',"'",'…','?','!',':','‑','“','”','(',')','/','-'}
    for type in text:
        type_without_punctuation = type.lower()

        if type_without_punctuation in unwanted_values:
            continue
        if type_without_punctuation.isdigit():
            continue
        # Check if the type without punctuation is in the wordlist
        if type_without_punctuation not in types:
            types.append(type_without_punctuation)
            if type_without_punctuation in wordlist:
                type_id = wordlist.index(type_without_punctuation) + 1
            # Increment the corresponding frequency band
                for threshold, label in type_ranges:
                    if type_id < threshold:
                        type_counts[label] += 1
                        break
                else:
                    type_counts['NotinCorpusT'] += 1
                type_counts['TYPES'] += 1
            else:
                type_counts['NotinCorpusT'] += 1
                type_counts['TYPES'] += 1  # Calculate the total number of types
        total_types = type_counts['TYPES']

    # Calculate percentages for each frequency band
    for band in ['100T', '200T', '300T', '400T', '500T', 'NotinCorpusT']:
        if total_types >  0:  # Avoid division by zero
            type_counts[band] = (type_counts[band] / total_types) *  100

    return type_counts

def process_files_in_folder(folder, wordlist):
    files = [f for f in os.listdir(folder) if f.endswith('.vert')]
    results = []
    for file in files:
        result = {'FILENAME': file}
        type_counts = process_file(os.path.join(folder, file), wordlist)
        result.update(type_counts)
        results.append(result)

    return results

def main():
    folder = '/Users/sallybruen/PycharmProjects/TextPrograms/SeideanSi2.vert'  # Set folder path
    wordlist_file = '/Users/sallybruen/PycharmProjects/TextPrograms/breacadh_P215-teenv3.xlsx'
    # Set the path to your wordlist file

    # Read the Excel file
    df = pd.read_excel(wordlist_file)
    # Assuming the content is in the second column (index 1)
    wordlist = df.iloc[:, 1].tolist()

    results = process_files_in_folder(folder, wordlist)

    # Writing the result to an Excel file
    excel_file_path = '/Users/sallybruen/PycharmProjects/B3TypeFrequency.xlsx'

    fieldnames = ['FILENAME', 'TYPES','100T', '200T', '300T', '400T', '500T', 'NotinCorpusT']

    df_results = pd.DataFrame(results, columns=fieldnames)
    df_results.to_excel(excel_file_path, index=False)


if __name__ == "__main__":
    main()