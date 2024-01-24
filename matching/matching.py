import os
from libmatching.libmatching import PDF_names, best_matches, rename_files
import argparse

# CLI arguments

parser = argparse.ArgumentParser(
    prog='matching',
    description='Rename PDFs according to a list of resembling names',
    epilog='Hope this helps!')

parser.add_argument('-l', '--list', help='list of real names')
parser.add_argument('-f', '--folder', help='folder containing the PDF files')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='print matching list with scores')

args = parser.parse_args()


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
        sorted_log_list = sorted(matches, key=lambda x: x[2])
        for match in sorted_log_list:
            print(*match, sep=' | ')

    # trim scores
    for match in matches:
        match.pop()

    # rename source folder files according to dictionary whose keys are the files's names, place them in output folder and create a log file in source folder
    rename_files(path, output_folder, matches)
