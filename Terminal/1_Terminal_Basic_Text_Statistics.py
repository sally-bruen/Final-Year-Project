import os
import csv
from collections import defaultdict
from openpyxl import Workbook
import argparse

values_to_skip = {'Xx', 'Fa', 'Fi', 'Fq', 'Fp', 'F', 'Fb'} # defines a set of values to skip

def process_file(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')

        sentence_count, tokens, overall_words, gen_count, words_in_current_sentence, max_sentence_length = 0, 0, 0, 0, 0, 0
        types, lemmatypes, pos_count = set(), set(), defaultdict(int)

        for row in reader:
            if row[3] in values_to_skip: # check if value should be skipped
                continue

            if row[3] == 'Fe': # check if value is s a full stop
                sentence_count += 1
                if words_in_current_sentence > max_sentence_length:
                    max_sentence_length = words_in_current_sentence
                words_in_current_sentence = 0  # Reset word count in the current sentence
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
    pass


def main(folder_path, excel_file_path):
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process .vert files and output statistics to an Excel file.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing .vert files.')
    parser.add_argument('excel_file_path', type=str, help='Path to the output Excel file.')

    args = parser.parse_args()

    main(args.folder_path, args.excel_file_path)
    print("\nThe basic text statistics calculated here are presented in the Excel file specified in the parameters.\n")