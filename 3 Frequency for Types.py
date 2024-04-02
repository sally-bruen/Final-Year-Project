import os
import csv
from collections import defaultdict
import pandas as pd

type_ranges = [(101, '100T'), (301, '300T'), (501, '500T'), (1001, '1000T'), (2001, '2000T'), (3001, '3000T'),
                               (4001, '4000T'), (5001, '5000T'), (10001, '10KT')]

def process_file(filename, wordlist):
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        text = [row[0] for row in reader]         # Get values from the first column of wordlist

    types = []      # string to add each unique type read
    type_counts = defaultdict(int)
    unwanted_values = {' ','...','–','','‘',',','.','’',"'",'…','?','!',':','‑','“','”','(',')','/','-'}
    for type in text:
        lowercase_type = type.lower()
        if lowercase_type.isdigit(): # skip if it's a number
            continue
        if lowercase_type in unwanted_values: # skip if it's unwanted
            continue

        # Check if the lowercase type is in the wordlist, if already in types string then skip
        if lowercase_type not in types:
            types.append(lowercase_type)
            if lowercase_type in wordlist:
                type_id = wordlist.index(lowercase_type) + 1    # find index if type is in the word list
            # Increment the corresponding frequency band
                for threshold, label in type_ranges:
                    if type_id < threshold:
                        type_counts[label] += 1
                        break
                else:
                    type_counts['10KplusT'] += 1
                type_counts['TYPES'] += 1
            else:
                type_counts['10KplusT'] += 1
                type_counts['TYPES'] += 1   # Calculate the total number of types
    total_types = type_counts['TYPES']

    # Calculate percentages for each frequency band
    for band in ['100T', '300T', '500T', '1000T', '2000T', '3000T', '4000T', '5000T', '10KT','10KplusT']:
        if total_types > 0:  # Avoid division by zero
            type_counts[band] = (type_counts[band] / total_types) *  100    # get percentage of types in each range

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
    folder = '/Users/sallybruen/PycharmProjects/TextPrograms/SeideanSi2.vert'  # path to folder of vert files
    wordlist_file = '/Users/sallybruen/PycharmProjects/TextPrograms/wordlist_NCIv2_2022-10000.xlsx' # path to word list file in .xlsx format

    df = pd.read_excel(wordlist_file)       # Read the wordlist file
    wordlist = df.iloc[:, 1].tolist()       # make a list of words in wordlist at index 1

    results = process_files_in_folder(folder, wordlist)

    excel_file_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllTypeFrequency.xlsx'    # path to output file

    fieldnames = ['FILENAME', 'TYPES', '100T', '300T', '500T', '1000T', '2000T', '3000T', '4000T', '5000T',
                  '10KT','10KplusT']
    df_results = pd.DataFrame(results, columns=fieldnames)
    df_results.to_excel(excel_file_path, index=False)

if __name__ == "__main__":
    main()