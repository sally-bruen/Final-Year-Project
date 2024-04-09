import os
import csv
from collections import defaultdict
import pandas as pd

type_ranges = [(101, '100C'), (301, '300C'), (501, '500C'), (1001, '1000C'), (2001, '2000C'), (3001, '3000C'),
               (4001, '4000C'), (5001, '5000C'), (10001, '10KC')]

def process_file(filename, wordlist):
    text = []
    total_content = 0
    lemmas_in_story = []    # all lemmas in .vert file
    content_words = []
    lemma_string = []   # string to only count unique lemmas
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            text.append(row[0]) # get words from .vert file
            lemmas_in_story.append(row[2]) # get lemmas from .vert file
            content_words.append(row[3])    # get POS tags from .vert file

    word_counts = defaultdict(int)
    unwanted_values = {' ','...','–','','‘',',','.','’',"'",'…','?','!',':','‑','“','”','(',')','/','-'}
    for lemma, word, content in zip(lemmas_in_story, text, content_words):
        if 'Nc' in content:     # Nc is the POS tag for common nouns
            lower_common_noun = word.lower()
            if lower_common_noun in unwanted_values:    # skip if it's unwanted
                continue
            if lower_common_noun.isdigit():     # skip if it's a digit
                continue

            if lemma not in lemma_string:   # if unique lemma found, add to string
                lemma_string.append(lemma)
                if lower_common_noun in wordlist:
                    word_id = wordlist.index(lower_common_noun) + 1 # find index if noun is in the word list
                    # Increment the corresponding frequency band
                    for threshold, label in type_ranges:
                        if word_id < threshold:
                            word_counts[label] += 1
                            break
                    else:
                        word_counts['10KplusC'] += 1
                    word_counts['LEMMAS'] += 1
                else:
                    word_counts['10KplusC'] += 1
                    word_counts['LEMMAS'] += 1 # Calculate the total number of types
                total_content = word_counts['LEMMAS']

    # Calculate percentages for each frequency band
    for band in ['100C', '300C', '500C', '1000C', '2000C', '3000C', '4000C', '5000C',
                 '10KC','10KplusC']:
        if total_content > 0:
            word_counts[band] = (word_counts[band] / total_content) * 100 # Avoid division by zero

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

    df = pd.read_excel(wordlist_file)    # Read the wordlist file
    wordlist = df.iloc[:, 1].tolist()   # make a list of words in the wordlist at index 1

    results = process_files_in_folder(folder, wordlist)

    fieldnames = ['FILENAME', 'LEMMAS', '100C', '300C', '500C', '1000C', '2000C', '3000C', '4000C',
                 '5000C', '10KC','10KplusC']
    df_results = pd.DataFrame(results, columns=fieldnames)
    df_results.to_excel(excel_file_path, index=False)

    print('\nThe results have been outputted to ' + excel_file_path + '.\n')

if __name__ == "__main__":
    main()
