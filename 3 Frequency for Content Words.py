import os
import csv
from collections import defaultdict
import pandas as pd

type_ranges = [(101, '100C'), (301, '300C'), (501, '500C'), (1001, '1000C'), (2001, '2000C'), (3001, '3000C'),
                               (4001, '4000C'), (5001, '5000C'), (10001, '10KC')]

def process_file(filename, wordlist):
    text = []
    content_words = []
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            text.append(row[0])     # get words from .vert file
            content_words.append(row[3])    # get POS tags from .vert file

    word_counts = defaultdict(int)
    unwanted_values = {' ','...','–','','‘',',','.','’',"'",'…','?','!',':','‑','“','”','(',')','/','-'}
    for content, word in zip(content_words, text):
        if content.startswith('N') or content.startswith('V') or content.startswith('A') or content.startswith('R'):    # POS tags for content words
            lower_content_word = word.lower()

            if lower_content_word.isdigit():    # skip if it's a number
                continue
            if lower_content_word in unwanted_values:   # skip if it's unwanted
                continue

        # Check if the lowercase word is in the wordlist
            if lower_content_word in wordlist:
                word_id = wordlist.index(lower_content_word) + 1     # find index if word is in the word list
            # Increment the corresponding frequency band
                for threshold, label in type_ranges:
                    if word_id < threshold:
                        word_counts[label] += 1
                        break
                else:
                    word_counts['10KplusC'] += 1
                word_counts['CONTENT_WORDS'] += 1
            else:
                word_counts['10KplusC'] += 1
                word_counts['CONTENT_WORDS'] += 1  # Calculate the total number of types
            total_content = word_counts['CONTENT_WORDS']

    # Calculate percentages for each frequency band
    for band in ['100C', '300C', '500C', '1000C', '2000C', '3000C', '4000C', '5000C',
                 '10KC','10KplusC']:
        if total_content > 0:
            word_counts[band] = (word_counts[band] / total_content) * 100  # Avoid division by zero

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
    wordlist_file = '/Users/sallybruen/PycharmProjects/TextPrograms/wordlist_NCIv2_2022-10000.xlsx' # path to word list file in .xlsx format

    df = pd.read_excel(wordlist_file)   # Read the wordlist file
    wordlist = df.iloc[:, 1].tolist()   # make a list of words in the wordlist at index 1

    results = process_files_in_folder(folder, wordlist)

    excel_file_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/1ContentFrequency.xlsx' # path to output file

    fieldnames = ['FILENAME', 'CONTENT_WORDS', '100C', '300C', '500C', '1000C', '2000C', '3000C', '4000C', '5000C',
                  '10KC','10KplusC']
    df_results = pd.DataFrame(results, columns=fieldnames)
    df_results.to_excel(excel_file_path, index=False)

if __name__ == "__main__":
    main()