# Q8 - Compressed Log Index using Pickle and Zip

## Problem Description

A server produces several text log files.

The program scans all log files in a specified folder and builds an inverted index.

The inverted index maps each normalized token to the file names and line numbers where the token occurs.

The index is stored using Python pickle.

The original log files and the pickle index are compressed into a ZIP archive.

The program also provides a SEARCH mode that loads the pickle index and searches for tokens.

---

## Modes

The program supports two modes:

1. BUILD
2. SEARCH

---

## BUILD Mode

### Command

```text
python 12402080601054_Assignment1_Q8.py BUILD logs archive.zip
