import os
import csv
from collections import defaultdict
import pandas as pd

type_ranges = [(101, '100W'), (301, '300W'), (501, '500W'), (1001, '1000W'), (2001, '2000W'), (3001, '3000W'),
               (4001, '4000W'), (5001, '5000W'), (10001, '10KW')]

def process_file(filename, wordlist):
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        text = [row[0] for row in reader]   # get words from the first column of .vert file
    total_words = 0
    word_counts = defaultdict(int)
    unwanted_values = {' ','...','–','','‘',',','.','’',"'",'…','?','!',':','‑','“','”','(',')','/','-'}
    for word in text:
        lower_word = word.lower()
        if lower_word.isdigit():    # skip if it's a number
            continue
        if lower_word in unwanted_values:   # skip if it's unwanted
            continue

        # Check if the lowercase word is in the wordlist
        if lower_word in wordlist:
            word_id = wordlist.index(lower_word) + 1    # find index if the word is in the word list
            # Increment the corresponding frequency band
            for threshold, label in type_ranges:
                if word_id < threshold:
                    word_counts[label] += 1
                    break
            else:
                word_counts['10KplusW'] += 1
            word_counts['WORDS'] += 1
        else:
            word_counts['10KplusW'] += 1
            word_counts['WORDS'] += 1 # Calculate the total number of types
        total_words = word_counts['WORDS']

    # Calculate percentages for each frequency band
    for band in ['100W', '300W', '500W', '1000W', '2000W', '3000W', '4000W', '5000W','10KW','10KplusW']:
        if total_words > 0:
            word_counts[band] = (word_counts[band] / total_words) * 100# Avoid division by zero

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

    fieldnames = ['FILENAME', 'WORDS', '100W', '300W', '500W', '1000W', '2000W', '3000W', '4000W', '5000W',
                 '10KW','10KplusW']
    df_results = pd.DataFrame(results, columns=fieldnames)
    df_results.to_excel(excel_file_path, index=False)

    print('\nThe results have been outputted to ' + excel_file_path + '.\n')

if __name__ == "__main__":
    main()
