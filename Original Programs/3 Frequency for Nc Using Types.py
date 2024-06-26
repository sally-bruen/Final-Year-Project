import os
import csv
from collections import defaultdict
import pandas as pd

type_ranges = [(101, '100T'), (301, '300T'), (501, '500T'), (1001, '1000T'), (2001, '2000T'), (3001, '3000T'),
                               (4001, '4000T'), (5001, '5000T'), (10001, '10KT')]

def process_file(filename, wordlist):
    text = []
    total_common_noun = 0
    content_words = []
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            text.append(row[0]) # get words from .vert file
            content_words.append(row[3])    # get POS tags from .vert file

    types = []
    word_counts = defaultdict(int)
    unwanted_values = {' ', '...', '–', '', '‘', ',', '.', '’', "'", '…', '?', '!', ':', '‑', '“', '”', '(', ')', '/','-'}
    for content, type in zip(content_words, text):
        if 'Nc' in content:
            lower_common_noun = type.lower()
            if lower_common_noun in unwanted_values:    # skip if it's unwanted
                continue
            if lower_common_noun.isdigit(): # skip if it's a digit
                continue
            # Check if the word without punctuation is in the wordlist
            if lower_common_noun not in types:
                types.append(lower_common_noun)
                if lower_common_noun in wordlist:
                    word_id = wordlist.index(lower_common_noun) + 1
                    # Increment the corresponding frequency band
                    for threshold, label in type_ranges:
                        if word_id < threshold:
                            word_counts[label] += 1
                            break
                    else:
                        word_counts['10KplusT'] += 1
                    word_counts['TYPES'] += 1
                else:
                    word_counts['10KplusT'] += 1
                    word_counts['TYPES'] += 1  # Calculate the total number of types
            total_common_noun = word_counts['TYPES']

    # Calculate percentages for each frequency band
    for band in ['100C', '300C', '500C', '1000C', '2000C', '3000C', '4000C', '5000C',
                 '10KC','10KplusC']:
        if total_common_noun > 0:
            word_counts[band] = (word_counts[band] / total_common_noun) * 100  # Avoid division by zero

    return word_counts

def process_files_in_folder(folder, wordlist):
    files = [f for f in os.listdir(folder) if f.endswith('.vert')]
    results = []
    for file in files:
        result = {'FILENAME': file}
        word_counts = process_file(os.path.join(folder, file), wordlist)
        result.update(word_counts)
        results.append(result)

    return results

def main():
    folder = '/Users/sallybruen/PycharmProjects/TextPrograms/SeideanSi2.vert'  # path to folder of vert files
    wordlist_file = '/Users/sallybruen/PycharmProjects/TextPrograms/wordlist_NCIv2_2022-10000.xlsx' # path to wordlist in .xlsx format

    df = pd.read_excel(wordlist_file)       # Read the wordlist file
    wordlist = df.iloc[:, 1].tolist()       # make a list of words in wordlist at index 1

    results = process_files_in_folder(folder, wordlist)

    excel_file_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/NcTypeFrequency.xlsx'   # path to output file

    fieldnames = ['FILENAME', 'TYPES', '100C', '300C', '500C', '1000C', '2000C', '3000C', '4000C',
                  '5000C', '10KC','10KplusC']
    df_results = pd.DataFrame(results, columns=fieldnames)
    df_results.to_excel(excel_file_path, index=False)

if __name__ == "__main__":
    main()