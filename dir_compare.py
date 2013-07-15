#!/usr/bin/env python
"""
Recursively compares the contents of two directories.

Short Description of the script.

NAME
    dir_compare.py

SYNOPSYS
    python ./dir_compare.py <Directory_1> <Directory_2>

DESCRIPTION
    Prints the names of the files that are different between the two trees.
    The output is in the form: Status  F/D  File/Directory  Name
    Status: L - in left tree only
            R - in right tree only
            C  - present in both trees but conflict in content
    F/D - file or directory.
    Name - Name of the file or directory

OPTIONS
    <Directory 1> <Directory 2>
        Names of directories to compare

NOTES
    This follows the method discussed in:
    stackoverflow.com/questions/4187564/
    recursive-dircmp-compare-two-directories-to-ensure-they-have-the-same-
    files-and

AUTHOR
    Abhisek Pan, pana@purdue.edu

LICENSE
    Copyright (C) 2013  Abhisek Pan, Purdue University. All rights reserved.

    This file is distributed under the University of Illinois/NCSA Open Source
    License.
    You can obtain a soft copy of the license either by visiting
    http://otm.illinois.edu/uiuc_openSource, or by mailing pana@purdue.edu.
"""

import filecmp as fc
import os
import sys


def print_members(path, memlist, level, status):
    """Print memebers of the list with appropriate indentation.

    Args:
        path: path to be prefixed to the members.
        memlist: list of members (files/dirs) to print.
        level: depth in the tree, indentation level.
        status: L/R/C, see script description.
    """
    indent = '\t' * level
    for e in memlist:
        member = os.path.join(path, e)
        if os.path.isdir(member):
            sys.stdout.write('%s%s %s %s\n' % (indent, status, 'D', member))
        else:
            sys.stdout.write('%s%s %s %s\n' % (indent, status, 'F', member))


def compare_rec(dir1, dir2, level):
    """Recursively compare two directory trees.

    Args:
        dir1: directory 1.
        dir2:directory 2.
        level: depth in tree.
    """
    dcmp = fc.dircmp(dir1, dir2)
    print_members(dir1, dcmp.left_only, level, 'L')
    print_members(dir2, dcmp.right_only, level, 'R')
    (_, mismatch, errors) = fc.cmpfiles(dir1, dir2, dcmp.common_files,
                                        shallow=False)
    print_members(dir1, mismatch, level, 'C')
    assert not errors
    common_dirs = dcmp.common_dirs
    if common_dirs is None:
        return
    for common_dir in common_dirs:
        compare_rec(os.path.join(dir1, common_dir),
                    os.path.join(dir2, common_dir),
                    (level + 1))


def compare_dirs():
    """Start directory comparison after reading CLA."""
    dir1 = sys.argv[1]
    dir2 = sys.argv[2]
    level = 0
    compare_rec(dir1, dir2, level)


if __name__ == '__main__':
        compare_dirs()
