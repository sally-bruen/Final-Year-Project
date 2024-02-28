import os
import csv
from collections import defaultdict
import pandas as pd

def process_file(filename, wordlist):
    words_10kplus = []
    text = []
    lemmas = []
    content_words = []
    lemma_string = []
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        # Extract values from the last column
        for row in reader:
            # Extract values from the first and last columns
            text.append(row[0])
            lemmas.append(row[2])
            content_words.append(row[3])



    word_counts = defaultdict(int)
    unwanted_values = {' ','...','–','','‘',',','.','’',"'",'…','?','!',':','‑','“','”','(',')','/','-'}
    for lemma, word, content in zip(lemmas, text, content_words):
        if 'Np' in content:
            content_word_without_punctuation = word.lower()
            if content_word_without_punctuation in unwanted_values:
                continue
            if content_word_without_punctuation.isdigit():
                continue
            # Check if the word without punctuation is in the wordlist
            if lemma not in lemma_string:
                lemma_string.append(lemma)
                if content_word_without_punctuation in wordlist:
                    word_id = wordlist.index(content_word_without_punctuation) + 1
                    # Increment the corresponding frequency band
                    if word_id < 101:
                        word_counts['100C'] += 1
                    elif 100 < word_id < 301:
                        word_counts['300C'] += 1
                    elif 300 < word_id < 501:
                        word_counts['500C'] += 1
                    elif 500 < word_id < 1001:
                        word_counts['1000C'] += 1
                    elif 1000 < word_id < 2001:
                        word_counts['2000C'] += 1
                    elif 2000 < word_id < 3001:
                        word_counts['3000C'] += 1
                    elif 3000 < word_id < 4001:
                        word_counts['4000C'] += 1
                    elif 4000 < word_id < 5001:
                        word_counts['5000C'] += 1
                    elif 5000 < word_id < 10001:
                        word_counts['10000C'] += 1
                    word_counts['LEMMAS'] += 1
                # print(content_word_without_punctuation, content, word_id)
                else:
                    word_counts['10KplusC'] += 1
                    # print(content_word_without_punctuation, content, 'not in corpus')
                    words_10kplus.append(content_word_without_punctuation)
                    word_counts['LEMMAS'] += 1
                pass
        else:
            continue
    total_content = word_counts['LEMMAS']

    # Calculate percentages for each frequency band
    for band in ['100C', '300C', '500C', '1000C', '2000C', '3000C', '4000C', '5000C',
                 '10000C','10KplusC']:
        if total_content > 0:
            word_counts[band] = (word_counts[band] / total_content) * 100  # Avoid division by zero

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
    excel_file_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/NpLemmaFrequency.xlsx'

    fieldnames = ['FILENAME', 'LEMMAS', '100C', '300C', '500C', '1000C', '2000C', '3000C', '4000C',
                  '5000C', '10000C','10KplusC']

    df_results = pd.DataFrame(results, columns=fieldnames)
    df_results.to_excel(excel_file_path, index=False)

    # Write the  10kPlusFREQ words to a text file
    # text_file_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/10kplusFREQ_types.txt'
    # with open(text_file_path, 'w') as f:
    #     for word in all_words_10kplus:
    #         f.write(word + '\n')

if __name__ == "__main__":
    main()