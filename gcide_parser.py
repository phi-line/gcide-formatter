#!/usr/bin/env python

import re
import os

"""
Parses gcide directory and returns python objects
"""


class Definition:
    def __init__(self, word, text, source, pos):
        self.word = word
        self.text = text
        self.source = source
        self.pos = pos


def __get_cide_files():
    files = os.listdir("input")
    files_sorted = sorted(files)
    files_filtered = filter(lambda name: re.match("^CIDE.\\w$", name), files_sorted)
    files_list = list(files_filtered)
    return files_list


# TODO there could be multiple <ent>s (e.g. 'Newton') (not high priority)
# TODO unsafe group() call (could be None type)
def __get_word(entry):
    return re.search("""(?<=<ent>).*?(?=</?ent>)""", entry).group()


def __get_pos(entry):
    match = re.search("""(?<=<pos>).*?(?=</pos>)""", entry)
    return "None" if match is None else match.group()


def __get_definitions_raw(entry):
    match = re.findall("""<def>.*?</def>.*?</source>]""", entry)
    filtered = filter(lambda x: x is not None, match)
    return filtered or None


def get_definitions():
    # Concatenate CIDE.[A-Z]
    print("Concatenating CIDE files")

    concatenated = ""
    for file in __get_cide_files():
        with open(f"input/{file}", encoding='cp1252') as f:
            concatenated = concatenated + f.read()

    # Remove new lines
    print("Removing new lines")

    concatenated = concatenated.replace("\n", " ")

    # Group entries in list
    print("Grouping entries")

    entries_raw = re.findall("""<p><ent>.*?(?=<p><ent>)""", concatenated)

    # Convert entries_raw to definitions
    print("Converting entries to objects")

    definitions = []

    for i, entry_raw in enumerate(entries_raw):
        definitions_raw = __get_definitions_raw(entry_raw)
        word = __get_word(entry_raw)
        pos = __get_pos(entry_raw)

        for definition in definitions_raw:
            definition_texts = re.findall("""(?<=<def>).*?(?=</def>)""", definition)
            definition_sources = re.findall("""(?<=<source>).*?(?=</source>)""", definition)
            # TODO sources not bound to texts, could lead to errors/wrong source

            for text, source in zip(definition_texts, definition_sources):
                definitions.append(Definition(word, text, source, pos))

    return definitions
