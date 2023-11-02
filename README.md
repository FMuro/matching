The goal of this `python` script is to rename PDF files according to a list of resembling names. The use case is the following. Files should be named according to names in a list, but you got the file names corrupted because, e.g. they were automatically generated after an OCR process.

We must have the following things:

- A folder `myfolder` with all PDF files.
- A text file `names.txt` such that: 
  * The number of lines is the number of PDF files.
  * Lines resemble the PDF files's names. 

Install the requirements and run the script as follows:

```
$ python3 matching.py path/to/names.txt path/to/myfolder
```

The output is a folder `myfolder_renamed` within the current location containing the renamed PDF files.

The option `-d` prints a list of the form `file name | macthed name | score` in decreasing failure likelihood order for you to check if there are errors.

You can test this script as follows. Assuming you're at this project's root:

```
$ cd test
$ python3 ../matching.py -d names.txt myfolder
$ ls myfolder_renamed
$ cat myfolder_matching.log
```