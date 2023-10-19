from thefuzz import process
from scipy import optimize
from scipy.sparse import csr_matrix
import numpy as np
import os
import collections
import shutil

# get the list of PDF file names (without extension) in path
def PDF_names(path):
    return [os.path.splitext(filename)[0] for filename in os.listdir(
        path) if filename.endswith('.pdf')]

# get the score matrix comparing strings in two lists
def score_matrix(list1, list2):
    rows_list = []
    columns_list = []
    scores_list = []
    for file, count in collections.Counter(list1).items():
        matches = process.extract(file, list2)
        for match in matches:
            rows_list.append(list1.index(file))
            columns_list.append(list2.index(match[0]))
            scores_list.append(match[1])
    rows = np.array(rows_list)
    columns = np.array(columns_list)
    scores = np.array(scores_list)
    return csr_matrix((scores, (rows, columns)), shape=(
        len(list1), len(list2))).toarray()

# given two lists, create a new list whose elements are of the form [element of first list, best match in second list, score]
def best_match_list(list1, list2):
    M = score_matrix(list1, list2)
    # solve the linear sum assignment problem
    [list1_positions, list2_positions] = optimize.linear_sum_assignment(
    M, maximize=True)
    return [[list1[list1_positions[i]], list2[list2_positions[i]],M[list1_positions[i],list2_positions[i]]]
              for i in range(len(list1_positions))]

# rename source folder files according to a list of pairs of the form [filename, newname] and copy them to output folder
def rename_files(source_path, output_path, list):
    for item in list:
        shutil.copy(os.path.join(source_path, item[0]+'.pdf'), os.path.join(output_path, item[1]+'.pdf'))