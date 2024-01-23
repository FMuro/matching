# What does this do?

The goal of this `python` package is to rename PDF files according to a list of resembling names. The use case is the following. Files should be named according to names in a list, but you got the file names corrupted because, e.g. they were automatically generated after an OCR process.

# Install

Run the following command in terminal:

```
pip install --upgrade git+https://github.com/FMuro/matching.git#egg=matching
```

Use this command to update the package too. 

# How to use

We must have the following things:

- A folder `myfolder` with all PDF files.
- A text file `names.txt` such that: 
  * The number of lines is the number of PDF files.
  * Lines resemble the PDF files's names. 

```
$ matching path/to/names.txt path/to/myfolder
```

The output is a folder `myfolder_renamed` within the current location containing the renamed PDF files.

The option `-d` prints a list of the form `file name | macthed name | score` in decreasing failure likelihood order for you to check if there are errors.

# Testing

You can test this script by downloading the `test` folder and running the following commands:

```
$ cd test
$ matching.py -d names.txt myfolder
$ ls myfolder_renamed
```