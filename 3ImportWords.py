import os
import csv
from collections import defaultdict
import pandas as pd

def process_file(filename, wordlist):
    words_10kplus = []
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        # Extract values from the first column
        text = [row[0] for row in reader]


    word_counts = defaultdict(int)
    unwanted_values = {' ','...','–','','‘',',','.','’',"'",'…','?','!',':','‑','“','”','(',')','/','-'}
    for word in text:
        word_without_punctuation = word.lower()
        if word_without_punctuation in unwanted_values:
            continue
        if word_without_punctuation.isdigit():
            continue
        # Check if the word without punctuation is in the wordlist

        if word_without_punctuation in wordlist:
            word_id = wordlist.index(word_without_punctuation) + 1
            # Increment the corresponding frequency band
            if word_id < 101:
                word_counts['100W'] += 1
            elif 100 < word_id < 301:
                word_counts['300W'] += 1
            elif 300 < word_id < 501:
                word_counts['500W'] += 1
            elif 500 < word_id < 1001:
                word_counts['1000W'] += 1
            elif 1000 < word_id < 2001:
                word_counts['2000W'] += 1
            elif 2000 < word_id < 3001:
                word_counts['3000W'] += 1
            elif 3000 < word_id < 4001:
                word_counts['4000W'] += 1
            elif 4000 < word_id < 5001:
                word_counts['5000W'] += 1
            elif 5000 < word_id < 10001:
                word_counts['10000W'] += 1
            word_counts['WORDS'] += 1
            #print(word_without_punctuation, word_counts.values())
        else:
            word_counts['10KplusW'] += 1
            words_10kplus.append(word_without_punctuation)
            word_counts['WORDS'] += 1
    total_words = word_counts['WORDS']

    # Calculate percentages for each frequency band
    for band in ['100W', '300W', '500W', '1000W', '2000W', '3000W', '4000W', '5000W','10000W','10KplusW']:
        if total_words > 0:
            word_counts[band] = (word_counts[band] / total_words) * 100# Avoid division by zero

    return word_counts, words_10kplus

def process_files_in_folder(folder, wordlist):
    files = [f for f in os.listdir(folder) if f.endswith('.vert')]
    results = []
    all_words_10kplus = []
    for file in files:
        result = {'FILENAME': file}
        word_counts, words_10kplus = process_file(os.path.join(folder, file), wordlist)
        result.update(word_counts)
        results.append(result)
        all_words_10kplus.extend(words_10kplus)

    return results, all_words_10kplus

def main():
    words_10kplus = []
    folder = '/Users/sallybruen/PycharmProjects/TextPrograms/SeideanSi2.vert'  # Set folder path
    wordlist_file = '/Users/sallybruen/PycharmProjects/TextPrograms/wordlist_NCIv2_2022-10000.xlsx'
    # Set the path to your wordlist file

    # Read the Excel file
    df = pd.read_excel(wordlist_file)
    # Assuming the content is in the second column (index 1)
    wordlist = df.iloc[:, 1].tolist()

    results, all_words_10kplus = process_files_in_folder(folder, wordlist)

    # Writing the result to an Excel file
    excel_file_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/SSWordFrequency.xlsx'

    fieldnames = ['FILENAME', 'WORDS', '100W', '300W', '500W', '1000W', '2000W', '3000W', '4000W', '5000W',
                  '10000W','10KplusW']

    df_results = pd.DataFrame(results, columns=fieldnames)
    df_results.to_excel(excel_file_path, index=False)

    # Write the  10kPlusFREQ words to a text file
    text_file_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/10kplusFREQ_types.txt'
    with open(text_file_path, 'w') as f:
        for word in all_words_10kplus:
            f.write(word + '\n')

if __name__ == "__main__":
    main()