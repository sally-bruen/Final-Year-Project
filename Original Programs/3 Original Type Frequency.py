import os
import csv
from collections import defaultdict
import pandas as pd

def process_file(filename, wordlist):
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        # Extract values from the first column
        text = [row[0] for row in reader]
        content_words = [row[3] for row in reader]

    types = []
    word_counts = defaultdict(int)
    unwanted_values = {' ','...','–','','‘',',','.','’',"'",'…','?','!',':','‑','“','”','(',')','/','-'}
    for word, content in zip(text, content_words):
        if not content.startswith('N') or not content.startswith('V') or not content.startswith(
                'A') or not content.startswith('R'):
            continue

        word_without_punctuation = word.lower()
        if word_without_punctuation in unwanted_values:
            continue
        if word_without_punctuation.isdigit():
            continue
        # Check if the word without punctuation is in the wordlist
        if word_without_punctuation not in types:
            types.append(word_without_punctuation)
            if word_without_punctuation in wordlist:
                word_id = wordlist.index(word_without_punctuation) + 1
            # Increment the corresponding frequency band
                if word_id < 101:
                    word_counts['100FREQ'] += 1
                elif 100 < word_id < 301:
                    word_counts['300FREQ'] += 1
                elif 300 < word_id < 501:
                    word_counts['500FREQ'] += 1
                elif 500 < word_id < 1001:
                    word_counts['1000FREQ'] += 1
                elif 1000 < word_id < 2001:
                    word_counts['2000FREQ'] += 1
                elif 2000 < word_id < 3001:
                    word_counts['3000FREQ'] += 1
                elif 3000 < word_id < 4001:
                    word_counts['4000FREQ'] += 1
                elif 4000 < word_id < 5001:
                    word_counts['5000FREQ'] += 1
                elif 5000 < word_id < 10001:
                    word_counts['10000FREQ'] += 1
                word_counts['TYPES'] += 1
            else:
                word_counts['10KplusFREQ'] += 1
                word_counts['TYPES'] += 1
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
    wordlist_file = '/Users/sallybruen/PycharmProjects/TextPrograms/wordlist_NCIv2_2022-10000.xlsx' # path to word list file
    # Set the path to your wordlist file

    # Read the Excel file
    df = pd.read_excel(wordlist_file)
    # Assuming the content is in the second column (index 1)
    wordlist = df.iloc[:, 1].tolist()

    results = process_files_in_folder(folder, wordlist)

    # Writing the result to an Excel file
    excel_file_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllTextFrequency.xlsx'  # path to output file

    fieldnames = ['FILENAME', 'TYPES', '100FREQ', '300FREQ', '500FREQ', '1000FREQ', '2000FREQ', '3000FREQ', '4000FREQ',
                  '5000FREQ', '10000FREQ', '10KplusFREQ']

    df_results = pd.DataFrame(results, columns=fieldnames)
    df_results.to_excel(excel_file_path, index=False)

if __name__ == "__main__":
    main()