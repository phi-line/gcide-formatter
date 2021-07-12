#!/usr/bin/env python

import os
import re


# Place this script in a directory that contains the latest, unpacked version of GCIDE in a folder named "in".
# It will create a formatted JSON file in a folder called "out".

class Entry:
    def __init__(self, word, definitions, pos):
        self.word = word
        self.definitions = definitions
        self.pos = pos


class Definition:
    def __init__(self, text, source):
        self.text = text
        self.source = source


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
        concatenated = concatenated + f.read()

# Step 2: Remove new lines

concatenated = concatenated.replace("\n", " ")

# Step 3: Group entries in list

entries = re.findall("""<p><ent>.*?(?=<p><ent>)""", concatenated)

# Step 4: Turn entries into objects

entryObjects = []

for entry_str in entries:
    # TODO there could be multiple <ent>s (e.g. 'Newton') (not high priority)
    wordMatch = re.search("""(?<=<ent>).*?(?=</?ent>)""", entry_str)  # </?ent> because slash is missing on "Newton"
    if wordMatch is None:
        print("err: wordMatch is none")
        break
    word = wordMatch.group()

    posMatch = re.search("""(?<=<pos>).*?(?=</pos>)""", entry_str)
    pos = "None" if posMatch is None else posMatch.group()

    if not filter(lambda x: x is not None, re.findall("""<def>.*?</def>.*?</source>]""", entry_str)):
        break
    definitionsUnformatted = re.findall("""<def>.*?</def>.*?</source>]""", entry_str)
    for definition in definitionsUnformatted:
        definitionTexts = re.findall("""(?<=<def>).*?(?=</def>)""", definition)
        definitionSources = re.findall("""(?<=<source>).*?(?=</source>)""", definition)
        definitionObjects = map(lambda text, source: Definition(text, source), definitionTexts, definitionSources)

        entryObjects.append(Entry(word, definitionObjects, pos))
