import os
import csv
from collections import defaultdict
import pandas as pd

type_ranges = [(101, '100T'), (301, '300T'), (501, '500T'), (1001, '1000T'), (2001, '2000T'), (3001, '3000T'),
               (4001, '4000T'), (5001, '5000T'), (10001, '10KT')]

def process_file(filename, wordlist):
    text = []
    total_tokens = 0
    content_words = []
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            text.append(row[0]) # words from .vert file
            content_words.append(row[3])    # get POS tags from .vert file

    word_counts = defaultdict(int)
    unwanted_values = {' ','...','–','','‘',',','.','’',"'",'…','?','!',':','‑','“','”','(',')','/','-'}
    for content, word in zip(content_words, text):
        if 'Nc' in content: # Nc is the POS tag for common nouns
            lower_common_noun = word.lower()
            if lower_common_noun in unwanted_values:    # skip if it's unwanted
                continue
            if lower_common_noun.isdigit(): # skip if it's a digit
                continue

            if lower_common_noun in wordlist:           # Check if the common noun is in the wordlist
                word_id = wordlist.index(lower_common_noun) + 1
                for threshold, label in type_ranges:
                    if word_id < threshold:
                        word_counts[label] += 1
                        break
                else:
                    word_counts['10KplusT'] += 1
                word_counts['TOKENS'] += 1
            else:
                word_counts['10KplusT'] += 1
                word_counts['TOKENS'] += 1 # Calculate the total number of types
        total_tokens = word_counts['TOKENS']

    # Calculate percentages for each frequency band
    for band in ['100T', '300T', '500T', '1000T', '2000T', '3000T', '4000T', '5000T',
                 '10KT','10KplusT']:
        if total_tokens > 0:
            word_counts[band] = (word_counts[band] / total_tokens) * 100 # Avoid division by zero

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
    print('Give the paths to the following files and folders.\n')
    print("The input folder:")
    folder = input()
    print("The word list file (in .xlsx format):")
    wordlist_file = input()
    print("The output file (in .xlsx format):")
    excel_file_path = input()

    df = pd.read_excel(wordlist_file)       # Read the wordlist file
    wordlist = df.iloc[:, 1].tolist()       # make a list of words in the wordlist at index 1

    results = process_files_in_folder(folder, wordlist)

    fieldnames = ['FILENAME', 'TOKENS', '100T', '300T', '500T', '1000T', '2000T', '3000T', '4000T', '5000T',
                 '10KT', '10KplusT']
    df_results = pd.DataFrame(results, columns=fieldnames)
    df_results.to_excel(excel_file_path, index=False)

    print('\nThe results have been outputted to ' + excel_file_path + '.\n')

if __name__ == "__main__":
    main()
