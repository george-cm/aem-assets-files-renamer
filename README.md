# AEM Assets File Renamer

Command line tool to rename files in prepartion for uploading into Adobe Experience Manager (AEM) Assets (DAM).
Written in Python.

```
usage: aem_assets_file_renamer.py [-h] [-p PREFIX] [-o OUTPUT_FOLDER]
                                  [-l LOG_FILE] [-v]
                                  path_name

Takes a file or a folder as input and renames the input file or the files in
the input folder based on the AEM Assets convention.

positional arguments:
  path_name             name of the file or folder to be processed

optional arguments:
  -h, --help            show this help message and exit
  -p PREFIX, --prefix PREFIX
                        prefix string to prepend to the files (default: sps-
                        his-)
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        output folder for the renamed files (default: renamed)
  -l LOG_FILE, --log-file LOG_FILE
                        name of the log file (default: rename.log)
  -v, --version         show version
```
