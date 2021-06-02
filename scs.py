#!/usr/bin/env python3

from argparse import ArgumentParser
import filecmp
import os

parser = ArgumentParser()
parser.add_argument('mod_path', help='mod directory', metavar='MOD_PATH')
parser.add_argument('scs_path', help='SCS directory', metavar='SCS_PATH')
parser.add_argument('-v', '--verbosity', action='count', default=0,
                    help='increase output verbosity (-vv for debug)')
args = parser.parse_args()

mod_path = args.mod_path
scs_path = args.scs_path


def get_2_latest_versions(scs_path):
    '''
    Returns list of 2 latest versions of SCS data directories
    '''
    dirs = []
    for item in os.scandir(scs_path):
        if os.path.isdir(item) and item.name[0:2] == '1.':
            dirs.append(os.path.join(scs_path, item.name))
    return [dirs[-2], dirs[-1]]


def get_mod_subdirectories(path):
    '''
    Returns list of subdirectories (mods) in the 'mod' directory
    '''
    dirs = []
    dirpath, dirnames, filenames = next(os.walk(path))
    for dirname in dirnames:
        dirs.append(os.path.join(path, dirname))
    return dirs


def get_files_for_mod(path):
    '''
    Returns list of files in mod subdirectory
    '''
    files = []
    os.chdir(path)
    for dirpath, _, filenames in os.walk('.'):
        if dirpath != '.':
            for filename in filenames:
                files.append(os.path.join(dirpath, filename))
    return files


def get_all_mod_files(mods):
    '''
    Returns set of files from all mods
    '''
    files = set()
    for mod in mods:
        mod_files = get_files_for_mod(mod)
        for file in mod_files:
            files.add(file[2:])
    return (files)


if __name__ == '__main__':
    print(f"- Mod path:\n{mod_path}")

    previous_version_dir, current_version_dir = get_2_latest_versions(scs_path)
    print(f"- SCS versions:\n{previous_version_dir}\n{current_version_dir}")

    mods = get_mod_subdirectories(mod_path)
    files = get_all_mod_files(mods)

    custom = []
    changed = []
    deprecated = []

    for file in files:
        file1 = os.path.join(previous_version_dir, file)
        file2 = os.path.join(current_version_dir, file)
        if os.path.isfile(file1):
            if os.path.isfile(file2):
                if not filecmp.cmp(file1, file2, shallow=False):
                    changed.append(file)
            else:
                deprecated.append(file)
        else:
            custom.append(file)

    if custom:
        print("- Custom files:")
        for i in custom:
            print(i)
    else:
        print("No custom files")

    if deprecated:
        print("- Deprecated:")
        for i in deprecated:
            print(i)
    else:
        print("- No deprecated files")

    if changed:
        print("- Changed:")
        for i in changed:
            print(i)
    else:
        print("- No changes")
