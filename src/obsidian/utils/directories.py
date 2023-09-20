import argparse
import os

# Comments for review:
# - File name:
#   - I thought it was big enough to separate from utils.py
#   - I tried directory-utils.py - but the hyphen meant I could  not import it
#   - And an underscore in directory_utils.py was inconsistent with existing filenames


push_stack = list()


def push_dir(dirname: str):
    global push_stack
    push_stack.append(os.getcwd())
    os.chdir(dirname)


def pop_dir():
    global push_stack
    os.chdir(push_stack.pop())


def use_directory(dir, create_if_missing):
    class PushPopDirectory:
        def __init__(self, dir):
            self.dir = dir

        def __enter__(self):
            push_dir(dir)

        def __exit__(self, exc_type, exc_val, exc_tb):
            pop_dir()

    if create_if_missing:
        os.makedirs(dir, exist_ok=True)
    return PushPopDirectory(dir)


# From https://stackoverflow.com/q/11415570/104370
def readable_dir(prospective_dir):
    if not os.path.isdir(prospective_dir):
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
    if os.access(prospective_dir, os.R_OK):
        return prospective_dir
    else:
        raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))
