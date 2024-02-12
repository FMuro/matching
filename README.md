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
- A text file `names.txt` whose lines resemble the PDF files's names. 

```
matching --list path/to/names.txt --folder path/to/myfolder
```

The output is a folder `myfolder_matched` within the current location containing the renamed PDF files.

The option `-v` prints a list of the form `file name | matched name | score` in decreasing failure likelihood order for you to check if there are errors.

You can get help by running:

```
matching -h
```

# Testing

You can test this package by downloading the `test` folder and running the following commands:

```
cd test
matching -v -l names.txt -f myfolder
ls myfolder_matched
```