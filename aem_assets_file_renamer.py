from aem_naming_utils import AemNamingUtils
from shutil import copyfile, SameFileError
from pathlib import Path
from datetime import timedelta
import argparse
import logging
import sys
import timeit

proper_name = AemNamingUtils().create_proper_name
base_folder = Path().cwd()

__version__ = "1.0"

def main():
    start = timeit.default_timer()
    parser = argparse.ArgumentParser(
        description=
"""

Takes a file or a folder as input and renames the input file 
or the files in the input folder based on the AEM Assets convention.

""",
        epilog="""""", 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("path_name", help="name of the file or folder to be processed")
    parser.add_argument("-p", "--prefix", help="prefix string to prepend to the files", default="sps-his-", dest="prefix")
    parser.add_argument("-o", "--output-folder", help="output folder for the renamed files", default="renamed", dest="output_folder")
    parser.add_argument("-l", "--log-file", help="name of the log file", default='rename.log', dest='log_file')
    parser.add_argument("-v", "--version", help="show version", action="version", version=f"%(prog)s version {__version__}")

    args = parser.parse_args()

    if args.path_name is None:
        print(f"Please provide a file name or folder name.")
        sys.exit(1)
    in_path = Path(args.path_name)
    if not in_path.is_file() and not in_path.is_dir():
        print(f"Please provide a valid file name or folder name.")
        sys.exit(1)

    if not Path(args.output_folder).is_absolute():
        out_folder = base_folder / args.output_folder
    else:
        out_folder = Path(args.output_folder)
    prefix = args.prefix

    # preparing the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    # checking if a log file was passed as argument
    if args.log_file != '':
        log_file = args.log_file
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    # adding logging to the terminal (stdout)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

    logger.info(f"Processing '{in_path.as_posix()}', output folder '{out_folder.as_posix()}', prefix '{prefix}'")
    if not out_folder.is_dir():
        out_folder.mkdir()
    if in_path.is_file():
        result = rename_file(in_path, out_folder, prefix, logger)
        stop = timeit.default_timer()
        logger.info(f"Duration: {str(timedelta(seconds=(stop - start)))}")
        sys.exit(0)
    if in_path.is_dir():
        in_files = [f for f in in_path.glob('*') if f.is_file()]
        for in_path in in_files:
            result = rename_file(in_path, out_folder, prefix, logger)
        stop = timeit.default_timer()
        logger.info(f"Duration: '{str(timedelta(seconds=(stop - start)))}'")
        sys.exit(0)


def rename_file(file_path, out_folder, prefix, logger):
    new_name = out_folder / (prefix + proper_name(file_path.name))
    if new_name.is_file():
        logger.warning(f"Skipping file '{file_path.name}'. Destination file already exists: '{new_name.as_posix()}'.")
        return False
    try:
        result = copyfile(file_path.as_posix(), new_name.as_posix())
        if result == new_name.as_posix():
            logger.info(f"Renamed '{file_path.name}' to '{result}'")
            return True
        else:
            logger.error(f"Renamed '{file_path}' to '{result}' but the expected destination is different: '{new_name.as_posix()}'")
            return False
    except SameFileError:
        logger.error(f"Trying to move a file to itself: '{file_path.name}'")
    except OSError:
        logging.error(f"Error trying to write file: '{new_name.as_posix()}'. Check folder permissions.")
    return False

if __name__ == "__main__":
    main()