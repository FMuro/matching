from thefuzz import process
from scipy import optimize
from scipy.sparse import csr_matrix
import numpy as np
import os
import collections
import shutil
from unidecode import unidecode
from tabulate import tabulate

# get the list of PDF file names (without extension) in path

def PDF_names(path):
    return [os.path.splitext(filename)[0] for filename in os.listdir(
        path) if filename.endswith('.pdf')]


# get the score matrix comparing strings in two lists

def score_matrix(list1, list2):
    rows_list = []
    columns_list = []
    scores_list = []
    list1 = [unidecode(item) for item in list1]
    list2 = [unidecode(item) for item in list2]
    for item, count in collections.Counter(list1).items():
        matches = process.extract(item, list2)
        for match in matches:
            rows_list.append(list1.index(item))
            columns_list.append(list2.index(match[0]))
            scores_list.append(match[1])
    rows = np.array(rows_list)
    columns = np.array(columns_list)
    scores = np.array(scores_list)
    return csr_matrix((scores, (rows, columns)), shape=(
        len(list1), len(list2))).toarray()


# given two lists, create a new list whose elements are of the form [element of first list, best match in second list, score]
# and a dictionary of the form {best match in second list: element of first list}


def best_matches(list1, list2):
    M = score_matrix(list1, list2)
    # solve the linear sum assignment problem
    [list1_positions, list2_positions] = optimize.linear_sum_assignment(
        M, maximize=True)
    return [[list1[list1_positions[i]], list2[list2_positions[i]], M[list1_positions[i], list2_positions[i]]]
            for i in range(len(list1_positions))], {list2[list2_positions[i]]: list1[list1_positions[i]]
                                                    for i in range(len(list1_positions))}


# rename source folder files according to a list of pairs of the form [filename, newname] and copy them to output folder


def rename_files(source_path, output_path, list):
    for item in list:
        shutil.copy(os.path.join(
            source_path, item[0]+'.pdf'), os.path.join(output_path, item[1]+'.pdf'))


# normalize a string removing/modifying special characters from strings (diacritics, spaces, capitals, etc.)


def normalize_string(string):
    return unidecode(string).strip().replace(" ", "").replace(",", "").lower()

# print table from list of lists of the form [string1, string2, score] ordered by score (descending)

def sorted_table(list, old_name = 'OLD name', new_name = 'NEW name'):
    sorted_list = sorted(list, key=lambda x: x[2])
    print(tabulate(sorted_list, headers=[old_name, new_name, 'SCORE']))

def funcion():
    # text file with real names
    data = args.list

    # parse lines as elements of a list
    file = open(data, 'r')
    realnames = file.read().splitlines()
    file.close()

    # folder with the PDF files, whose names should be more or less the previous real names
    path = args.folder

    # get the list of PDF file names (without extension) in path
    filenames = PDF_names(path)

    # base folder name
    base_folder = os.path.basename(os.path.abspath(
        os.path.normpath(path)))

    # create output subfolder if it doesn't already exist
    output_folder = base_folder+'_matched'
    os.makedirs(output_folder, exist_ok=True)

    # create best match list for filenames and realnames
    # elements of this list are of the form [filename, best realname match, score]
    matches = best_matches(filenames, realnames)[0]

    # print log if verbose mode is on ("-v" option) in decreasing failure likelihood order
    if args.verbose:
        sorted_table(matches)

    # trim scores
    for match in matches:
        match.pop()

    # rename source folder files according to dictionary whose keys are the files's names, place them in output folder and create a log file in source folder
    rename_files(path, output_folder, matches)
