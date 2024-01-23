import sys
import os
from libmatching.libmatching import PDF_names, best_matches, rename_files

# separate user-provided options and arguments (only expected argument "-d" for debug/test)
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]


def funcion():
    # text file with real names
    data = args[0]

    # parse lines as elements of a list
    file = open(data, 'r')
    realnames = file.read().splitlines()
    file.close()

    # folder with the PDF files, whose names should be more or less the previous real names
    path = args[1]

    # get the list of PDF file names (without extension) in path
    filenames = PDF_names(path)

    # base folder name
    base_folder = os.path.basename(os.path.abspath(
        os.path.normpath(path)))

    # create output subfolder if it doesn't already exist
    output_folder = base_folder+'_renamed'
    os.makedirs(output_folder, exist_ok=True)

    # create best match list for filenames and realnames
    # elements of this list are of the form [filename, best realname match, score]
    matches = best_matches(filenames, realnames)[0]

    # print log if debug mode is on ("-d" option) in decreasing failure likelihood order
    if '-d' in opts:
        sorted_log_list = sorted(matches, key=lambda x: x[2])
        for match in sorted_log_list:
            print(*match, sep=' | ')

    # trim scores
    for match in matches:
        match.pop()

    # rename source folder files according to dictionary whose keys are the files's names, place them in output folder and create a log file in source folder
    rename_files(path, output_folder, matches)
