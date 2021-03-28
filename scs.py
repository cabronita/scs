#!/usr/bin/env python3

import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('mod_path', help='mod directory', metavar='MOD_PATH')
args = parser.parse_args()

mod_path = args.mod_path


def get_files_in_dir(mod_dir):
    files = []
    os.chdir(mod_dir)
    for dirpath, _, filenames in os.walk('.'):
        if dirpath != '.':  # Ignore top mod directory, as it's just metadata
            for filename in filenames:
                files.append(os.path.join(dirpath, filename))
    return files


print(f"Getting mod files from {mod_path}")
mod_files = get_files_in_dir(mod_path)

for file in mod_files:
    print(file)
