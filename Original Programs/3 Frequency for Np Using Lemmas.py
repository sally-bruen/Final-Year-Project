import os
import csv
from collections import defaultdict
import pandas as pd

type_ranges = [(101, '100P'), (301, '300P'), (501, '500P'), (1001, '1000P'), (2001, '2000P'), (3001, '3000P'),
                               (4001, '4000P'), (5001, '5000P'), (10001, '10KP')]

def process_file(filename, wordlist):
    text = []
    lemmas_in_story = []    # all lemmas in .vert file
    content_words = []
    lemma_string = []   # string to only count unique lemmas
    total_content = 0
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            text.append(row[0]) # get words from .vert file
            lemmas_in_story.append(row[2])  # get lemmas from .vert file
            content_words.append(row[3])    # get POS tags from .vert file

    word_counts = defaultdict(int)
    unwanted_values = {' ','...','–','','‘',',','.','’',"'",'…','?','!',':','‑','“','”','(',')','/','-'}
    for lemma, word, content in zip(lemmas_in_story, text, content_words):
        if 'Np' in content:     # Np is the POS tag for proper nouns
            lower_proper_noun = word.lower()
            if lower_proper_noun in unwanted_values:    # skip if it's unwanted
                continue
            if lower_proper_noun.isdigit():     # skip if it's a digit
                continue

            if lemma not in lemma_string:   # if unique lemma found, add to string
                lemma_string.append(lemma)
                if lower_proper_noun in wordlist:
                    word_id = wordlist.index(lower_proper_noun) + 1  # find index if noun is in the word list
                    # Increment the corresponding frequency band
                    for threshold, label in type_ranges:
                        if word_id < threshold:
                            word_counts[label] += 1
                            break
                    else:
                        word_counts['10KplusP'] += 1
                    word_counts['LEMMAS'] += 1
                else:
                    word_counts['10KplusP'] += 1
                    word_counts['LEMMAS'] += 1  # Calculate the total number of types
                total_content = word_counts['LEMMAS']


    # Calculate percentages for each frequency band
    for band in ['100P', '300P', '500P', '1000P', '2000P', '3000P', '4000P', '5000P',
                 '10KP','10KplusP']:
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
    wordlist_file = '/Users/sallybruen/PycharmProjects/TextPrograms/wordlist_NCIv2_2022-10000.xlsx' # path to wordlist file in .xlsx format

    df = pd.read_excel(wordlist_file)    # Read the wordlist file
    wordlist = df.iloc[:, 1].tolist()   # make a list of words in the wordlist at index 1

    results = process_files_in_folder(folder, wordlist)

    excel_file_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/NcLemmaFrequency.xlsx'  # path to output file

    fieldnames = ['FILENAME', 'LEMMAS', '100P', '300P', '500P', '1000P', '2000P', '3000P', '4000P',
                  '5000P', '10KP','10KplusP']
    df_results = pd.DataFrame(results, columns=fieldnames)
    df_results.to_excel(excel_file_path, index=False)

if __name__ == "__main__":
    main()