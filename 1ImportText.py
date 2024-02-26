import os
import csv
from collections import defaultdict
from openpyxl import Workbook


def process_file(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        sentence_count =  0
        tokens =  0
        types = set()
        overallwords =  0
        lemtypes = set()
        pos_count = defaultdict(int)
        gen_count =  0
        words_in_current_sentence =  0  # Variable to store words in the current sentence
        total_words_in_sentences =  0  # Variable to store total number of words in sentences
        total_sentences =  0  # Variable to store total number of sentences
        max_sentence_length = 0

        for row in reader:
            if row[3] == 'Xx':
                continue
            if row[3] == 'Fa':
                continue
            if row[3] == 'Fi':
                continue
            if row[3] == 'Fq':
                continue
            elif row[3] == 'Fe':
                sentence_count +=  1
                total_sentences +=  1  # Increment the total number of sentences
                if words_in_current_sentence > max_sentence_length:
                    max_sentence_length = words_in_current_sentence
                total_words_in_sentences += words_in_current_sentence  # Add words in current sentence to total
                words_in_current_sentence =  0  # Reset words in current sentence
                continue
            else:
                if row[0].lower() not in types:
                    types.add(row[0].lower())
                tokens +=  1
                #types.add(row[0])
            #do I need these if statements?
            # if not row[3].startswith('F'):
            #     if row[3] not in ['Xx']: #removed Sp and removed F*
                overallwords += 1
                #print(row[0],overallwords, len(types))
                words_in_current_sentence += 1
                lemtypes.add(row[2])
                pos_count[row[3][:2]] +=  1
                if row[3].startswith('N') and 'g' in row[3]:
                    gen_count +=  1

        # Compute average sentence length as average number of words per sentence
        avg_sentence_length = total_words_in_sentences / total_sentences

        # Convert defaultdict to a regular dictionary
        pos_count = dict(pos_count)
        #print('the types for this file are', types)

        return {
            'FILENAME': os.path.basename(filename),
            'sentence_count': sentence_count,
            'tokens': tokens,
            'types': len(types),
            'word_count': overallwords,
            'max_sentence_length': max_sentence_length,
            'average_sentence_length': avg_sentence_length,
            'lemtypes': len(lemtypes),
            'gen_count': gen_count,
            'pos_count': pos_count
        }

folder = '/Users/sallybruen/PycharmProjects/TextPrograms/SeideanSi2.vert'
files = [file for file in os.listdir(folder) if file.endswith('.vert')]
results = []

for file in files:
    result = process_file(os.path.join(folder, file))
    results.append(result)

excel_file_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/AllTextStats.xlsx'

wb = Workbook()
ws = wb.active

all_pos_keys = set(key for result in results for key in result['pos_count'])

fieldnames = ['FILENAME', 'sentence_count', 'tokens', 'types', 'word_count', 'max_sentence_length', 'average_sentence_length',
              'lemtypes', 'gen_count'] + list(all_pos_keys)

header_row = fieldnames
ws.append(header_row)

for result in results:
    row = [result[key] for key in fieldnames if key not in all_pos_keys]
    row += [result['pos_count'].get(key, 0) for key in all_pos_keys]
    ws.append(row)

wb.save(excel_file_path)
