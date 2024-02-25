import os
import csv
from collections import defaultdict
import pandas as pd

def process_file(filename, wordlist):
    types_10kPlus = []
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        # Extract values from the first column
        text = [row[0] for row in reader]


    types = []
    type_counts = defaultdict(int)
    unwanted_values = {' ','...','–','','‘',',','.','’',"'",'…','?','!',':','‑','“','”','(',')','/','-'}
    for type in text:
        type_wihtout_punctuation = type.lower()

        if type_wihtout_punctuation in unwanted_values:
            continue
        if type_wihtout_punctuation.isdigit():
            continue
        # Check if the type without punctuation is in the wordlist
        if type_wihtout_punctuation not in types:
            types.append(type_wihtout_punctuation)
            if type_wihtout_punctuation in wordlist:
                type_id = wordlist.index(type_wihtout_punctuation) + 1
            # Increment the corresponding frequency band
                if type_id < 101:
                    type_counts['100FREQ'] += 1
                elif 100 < type_id < 301:
                    type_counts['300FREQ'] += 1
                elif 300 < type_id < 501:
                    type_counts['500FREQ'] += 1
                elif 500 < type_id < 1001:
                    type_counts['1000FREQ'] += 1
                elif 1000 < type_id < 2001:
                    type_counts['2000FREQ'] += 1
                elif 2000 < type_id < 3001:
                    type_counts['3000FREQ'] += 1
                elif 3000 < type_id < 4001:
                    type_counts['4000FREQ'] += 1
                elif 4000 < type_id < 5001:
                    type_counts['5000FREQ'] += 1
                elif 5000 < type_id < 10001:
                    type_counts['10000FREQ'] += 1
                type_counts['TYPES'] += 1
            else:
                type_counts['10KplusFREQ'] += 1
                types_10kPlus.append(type_wihtout_punctuation)
                type_counts['TYPES'] += 1   # Calculate the total number of types
    total_types = type_counts['TYPES']

    # Calculate percentages for each frequency band
    for band in ['100FREQ', '300FREQ', '500FREQ', '1000FREQ', '2000FREQ', '3000FREQ', '4000FREQ', '5000FREQ', '10000FREQ','10KplusFREQ']:
        if total_types >  0:  # Avoid division by zero
            type_counts[band] = (type_counts[band] / total_types) *  100

    return type_counts, types_10kPlus

def process_files_in_folder(folder, wordlist):
    files = [f for f in os.listdir(folder) if f.endswith('.vert')]
    results = []
    all_types_10kPlus = []
    for file in files:
        result = {'FILENAME': file}
        type_counts, types_10kPlus = process_file(os.path.join(folder, file), wordlist)
        result.update(type_counts)
        results.append(result)
        all_types_10kPlus.extend(types_10kPlus)

    return results, all_types_10kPlus

def main():
    types_10kPlus = []
    folder = '/Users/sallybruen/PycharmProjects/TextPrograms/SeideanSi2.vert'  # Set folder path
    wordlist_file = '/Users/sallybruen/PycharmProjects/TextPrograms/wordlist_NCIv2_2022-10000.xlsx'
    # Set the path to your wordlist file

    # Read the Excel file
    df = pd.read_excel(wordlist_file)
    # Assuming the content is in the second column (index 1)
    wordlist = df.iloc[:, 1].tolist()

    results, all_types_10kPlus = process_files_in_folder(folder, wordlist)

    # Writing the result to an Excel file
    excel_file_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/SSTypeFrequency.xlsx'

    fieldnames = ['FILENAME', 'TYPES', '100FREQ', '300FREQ', '500FREQ', '1000FREQ', '2000FREQ', '3000FREQ', '4000FREQ',
                  '5000FREQ', '10000FREQ', '10KplusFREQ']

    df_results = pd.DataFrame(results, columns=fieldnames)
    df_results.to_excel(excel_file_path, index=False)

    # Write the  10kPlusFREQ types to a text file
    text_file_path = '/Users/sallybruen/PycharmProjects/TextPrograms/TestFiles/10kplusFREQ_types.txt'
    with open(text_file_path, 'w') as f:
        for type in all_types_10kPlus:
            f.write(type + '\n')

if __name__ == "__main__":
    main()