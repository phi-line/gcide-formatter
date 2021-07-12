#!/usr/bin/env python

import json
import os
import re


class Entry:
    def __init__(self, word, definitions, pos):
        self.word = word
        self.definitions = definitions
        self.pos = pos

    def to_json(self):
        return self.__dict__


class Definition:
    def __init__(self, text, source):
        self.text = text
        self.source = source

    def to_json(self):
        return self.__dict__


def json_handler(obj):
    return obj.to_json()


def get_cide_files():
    files = os.listdir("input")
    files_sorted = sorted(files)
    files_filtered = filter(lambda name: re.match("^CIDE.\\w$", name), files_sorted)
    files_list = list(files_filtered)
    return files_list


# TODO there could be multiple <ent>s (e.g. 'Newton') (not high priority)
# TODO unsafe group() call (could be None type)
def get_word(entry):
    return re.search("""(?<=<ent>).*?(?=</?ent>)""", entry).group()


def get_pos(entry):
    match = re.search("""(?<=<pos>).*?(?=</pos>)""", entry)
    return "None" if match is None else match.group()


def get_definitions_raw(entry):
    match = re.findall("""<def>.*?</def>.*?</source>]""", entry)
    filtered = filter(lambda x: x is not None, match)
    return filtered or None


def get_json():
    # Step 1: Concatenate CIDE.(A-Z)
    print("Concatenating CIDE files")

    concatenated = ""
    for file in get_cide_files():
        with open(f"input/{file}", encoding='cp1252') as f:
            concatenated = concatenated + f.read()

    # Step 2: Remove new lines
    print("Removing new lines")

    concatenated = concatenated.replace("\n", " ")

    # Step 3: Group entries in list
    print("Grouping entries")

    entries_raw = re.findall("""<p><ent>.*?(?=<p><ent>)""", concatenated)

    # Step 4: Convert entries_raw to entries
    print("Converting entries to objects")

    entries = []

    for i, entry_raw in enumerate(entries_raw):
        print(f"  Parsing entry {i}", end=" ")
        definitions_raw = get_definitions_raw(entry_raw)
        definitions = []

        for definition in definitions_raw:
            definition_texts = re.findall("""(?<=<def>).*?(?=</def>)""", definition)
            definition_sources = re.findall("""(?<=<source>).*?(?=</source>)""", definition)
            # TODO sources not bound to texts, could lead to errors/wrong source

            definitions_map = map(lambda text, source: Definition(text, source), definition_texts, definition_sources)
            definitions = list(definitions_map)

        word = get_word(entry_raw)
        pos = get_pos(entry_raw)
        entries.append(Entry(word, definitions, pos))
        print(f":: {word}")

    # Step 5: Format json string based on entryObjects
    print("Formatting object list to json")

    json_str = json.dumps(entries, default=json_handler)

    # Step 6: Check json validity
    print("Validating json")

    try:
        json.loads(json_str)
    except ValueError:
        print("Error: Json is invalid.")
        exit(-1)

    # Step 7: Return json
    print("Done, returning")
    return json_str
