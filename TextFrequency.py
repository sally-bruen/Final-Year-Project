import pandas as pd
import os
import string
import csv


def process_file(text_words, word_list):
    with (open(text_words, 'r') as file):
        text_words = csv.reader(file, delimiter='\t')
        #Extract values from the first column
        text_words = [row[0] for row in text_words]

    translator = str.maketrans('', '', string.punctuation)

    #text_words = text_words.split()
    word_counts = {'100FREQ': 0, '300FREQ': 0, '500FREQ': 0, '1000FREQ': 0, '5000FREQ': 0,
                   '10000FREQ': 0, '10KPLUSGREQ': 0}
    word_count = 0
    # Compare the words from the Excel array to the list from the text file
    for text_word in text_words:
        # Check if the word is punctuation in a box by itself
        if len(text_word) == 1 and text_word in string.punctuation:
            continue

        text_word = text_word.translate(translator)
        text_word_clean = text_word.lower().strip(string.punctuation)
        text_word_clean = text_word_clean.replace("‘", "").replace(',', '').replace('.', '').replace('’', '').replace(
            ' ', '')

        word_count += 1

        if text_word_clean in word_list:
            word_index = word_list.index(text_word_clean) + 1

            if word_index < 101:
                word_counts['100FREQ'] += 1
            elif 100 < word_index <= 300:
                word_counts['300FREQ'] += 1
            elif 300 < word_index <= 500:
                word_counts['500FREQ'] += 1
            elif 500 < word_index <= 1000:
                word_counts['1000FREQ'] += 1
            elif 1000 < word_index <= 5000:
                word_counts['1000FREQ'] += 1
            elif 5000 < word_index <= 10000:
                word_counts['1000FREQ'] += 1
            else:
                word_counts['10KPlusFREQ'] += 1
        else:
            word_counts['10KPLUSGREQ'] += 1
            print(text_word_clean)

    return word_counts


def process_files_in_folder(folder, wordlist):
    files = [f for f in os.listdir(folder) if f.endswith('.vert')]
    results = []

    for file in files:
        result = {'FILENAME': file}
        word_counts = process_file(os.path.join(folder, file), wordlist)
        result.update(word_counts)
        result['WORDS'] = sum(word_counts.values())  # Total words in the file
        results.append(result)

    return results


def main():
    # Define the paths to your files
    excel_file_path = '/Users/sallybruen/PycharmProjects/TextPrograms/wordlist_NCIv2_2022-10000.xlsx'
    text_folder_path = '/Users/sallybruen/PycharmProjects/TextPrograms/SeideanSi-2'

    # Load the Excel file into a DataFrame
    df = pd.read_excel(excel_file_path, engine='openpyxl')

    # Convert the relevant column to a list
    word_list = df['WORD'].tolist()

    # # Load the text file
    # with (open(text_file_path, 'r') as file):
    #     text_words = file.read()
    #
    # text_words = text_words.split()

    # Process the text file
    #word_counts = process_file(text_words, word_list)
    results = process_files_in_folder(text_folder_path, word_list)

    # Writing the result to a CSV file
    with open('/Users/sallybruen/PycharmProjects/TextPrograms/SS Results/TestTextFrequency.txt', 'w',
              newline='') as file:
        fieldnames = ['FILENAME', 'WORDS', '100FREQ', '300FREQ', '500FREQ', '1000FREQ', '5000FREQ', '10000FREQ',
                      '10KPLUSGREQ']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()

        for result in results:
            writer.writerow(result)


if __name__ == "__main__":
    main()

##########need to deal with not in folder parts of the folder
##########need to split files for excel file, line for each file

# import pandas as pd
# import string
#
#
# # Function to process a single file
# def process_file(filename, wordlist):
#     word_counts = {'100FREQ': 0, '300FREQ': 0, '500FREQ': 0, '1000FREQ': 0, '10KplusFREQ': 0}
#
#     with open(filename, 'r') as file:
#         text = file.read().split()
#
#     for word in text:
#         word_without_punctuation = word.translate(str.maketrans('', '', string.punctuation)).lower()
#         if word_without_punctuation in wordlist:
#             word_index = wordlist.index(word_without_punctuation) + 1
#
#             if word_index < 101:
#                 word_counts['100FREQ'] += 1
#             elif 100 < word_index <= 300:
#                 word_counts['300FREQ'] += 1
#             elif 300 < word_index <= 500:
#                 word_counts['500FREQ'] += 1
#             elif 500 < word_index <= 1000:
#                 word_counts['1000FREQ'] += 1
#             else:
#                 word_counts['10KplusFREQ'] += 1
#
#     return word_counts
#
#
# # Main function to run the program
# def main():
#     excel_file_path = 'wordfreq.xlsx'
#     text_file_path = 'story.txt'
#
#     # Read the Excel file into a DataFrame
#     df = pd.read_excel(excel_file_path, engine='openpyxl')
#
#     # Convert the relevant column to a list
#     wordlist = df['ColumnNameForWord'].tolist()
#
#     # Process the text file
#     word_counts = process_file(text_file_path, wordlist)
#
#     # Output to an Excel file
#     output_df = pd.DataFrame([{'FILENAME': text_file_path, 'WORDS': len(wordlist), **word_counts}])
#     output_df.to_excel('output.xlsx', index=False)
#
#
# if __name__ == "__main__":
#     main()
