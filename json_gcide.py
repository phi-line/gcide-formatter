#!/usr/bin/env python

import os
import re
import shutil


# Place this script in a directory that contains the latest, unpacked version of GCIDE in a folder named "in".
# It will create a formatted JSON file in a folder called "out".

def get_cide_files():
    files = os.listdir("in")
    files_sorted = sorted(files)
    files_filtered = filter(lambda name: re.match("^CIDE.\\w$", name), files_sorted)
    files_list = list(files_filtered)
    return files_list


# Step 1: Concatenate CIDE.(A-Z)

concatenated = ""
for file in get_cide_files():
    with open(f"in/{file}", encoding='cp1252') as f:
        print(f.name)
        concatenated = concatenated + f.read()

# Step 2: Group entries in list
