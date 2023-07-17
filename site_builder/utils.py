import os
import argparse
import logging

def parse_arguments():
    """ Parse command line arguments.
     
    Returns: args namespace 
    """
    parser = argparse.ArgumentParser(
        prog = "build_site",
        description="Build website from templates"
    )
    parser.add_argument('-t', '--template_path', default="templates")
    parser.add_argument('-o', '--output_path', default="site")
    parser.add_argument('-s', '--skip_paths', action='append', default=['templates/components'])
    parser.add_argument('-c', '--copy_paths', action="append", default=['assets', 'static'])

    args = parser.parse_args()
    return args


def init_log(name: str=None, level: int=logging.INFO):
    """ Initialize logger configuration. """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(level)

    formatter = logging.Formatter("[%(asctime)s %(levelname)s (%(funcName)s)] %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.debug(f"Initialized logger {logger.name}.")

    return logger


def recurse_path_search(path: str, files: list, skip_dirs: set=set()) -> None:
    """ Recursively travel through path and store each file in a list. """
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            files.append(full_path)
            logging.debug(f"File found: {full_path}")
        elif os.path.isdir(full_path) and full_path.replace("\\", "/") not in skip_dirs:
            recurse_path_search(full_path, files)


def recurse_path_remove(path: str) -> int:
    """ Recursively travel through path to delete all files and directories.
    
    Returns: number of files removed.
    """
    count = 0
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            os.remove(full_path)
            count += 1
            logging.debug(f"Removed file: {full_path}")
        elif os.path.isdir(full_path):
            count += recurse_path_remove(full_path)
    
    os.rmdir(path)
    return count