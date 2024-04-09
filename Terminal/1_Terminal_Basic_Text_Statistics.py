import os
import csv
from collections import defaultdict
from openpyxl import Workbook

values_to_skip = {'Xx', 'Fa', 'Fi', 'Fq', 'Fp', 'F', 'Fb'} # defines a set of values to skip

def process_file(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')

        sentence_count, tokens, overall_words, gen_count, words_in_current_sentence, max_sentence_length = 0, 0, 0, 0, 0, 0
        types, lemmatypes, pos_count = set(), set(), defaultdict(int)

        for row in reader:
            if row[3] in values_to_skip: # check if value should be skipped
                continue

            if row[3] == 'Fe': # check if value is a full stop
                sentence_count += 1
                if words_in_current_sentence > max_sentence_length:
                    max_sentence_length = words_in_current_sentence
                words_in_current_sentence = 0 # Reset word count in the current sentence
            else:
                types.add(row[0].lower())
                tokens += 1
                overall_words += 1
                words_in_current_sentence += 1
                lemmatypes.add(row[2])
                pos_count[row[3][:2]] += 1

                if row[3].startswith('N') and 'g' in row[3]:
                    gen_count += 1

        if sentence_count == 0:
            sentence_count = 1

        avg_sentence_length = overall_words / sentence_count
        pos_count = dict(pos_count)

        return {
            'FILENAME': os.path.basename(filename),
            'sentence_count': sentence_count,
            'tokens': tokens,
            'types': len(types),
            'word_count': overall_words,
            'max_sentence_length': max_sentence_length,
            'average_sentence_length': avg_sentence_length,
            'lemmatypes': len(lemmatypes),
            'gen_count': gen_count,
            'pos_count': pos_count
        }

def main():
    print('\nGive the path to the following folder and file: \n')
    print("The folder containing the .vert files.")
    folder_path = input()
    print("\nThe output file in .xlsx format where you want these basic text statistics to be stored.")
    excel_file_path = input()

    files = [file for file in os.listdir(folder_path) if file.endswith('.vert')]
    results = [process_file(os.path.join(folder_path, file)) for file in files]

    wb = Workbook()
    ws = wb.active

    all_pos_keys = set(key for result in results for key in result['pos_count'])

    fieldnames = ['FILENAME', 'sentence_count', 'tokens', 'types', 'word_count', 'max_sentence_length', 'average_sentence_length',
                 'lemmatypes', 'gen_count'] + list(all_pos_keys)

    ws.append(fieldnames)

    for result in results:
        row = [result[key] for key in fieldnames if key not in all_pos_keys]
        row += [result['pos_count'].get(key, 0) for key in all_pos_keys]
        ws.append(row)

    wb.save(excel_file_path)

    print('\nThe results have been outputted to ' + excel_file_path + '.\n')

if __name__ == "__main__":
    main()
