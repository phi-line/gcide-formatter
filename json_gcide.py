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
    return re.search("""(?<=<ent>).*?(?=</?ent>)""", entry_raw).group()


def get_pos(entry):
    match = re.search("""(?<=<pos>).*?(?=</pos>)""", entry_raw)
    return "None" if match is None else match.group()


def get_definitions_raw(entry):
    match = re.findall("""<def>.*?</def>.*?</source>]""", entry_raw)
    filtered = filter(lambda x: x is not None, match)
    return filtered or None


# Step 1: Concatenate CIDE.(A-Z)

concatenated = ""
for file in get_cide_files():
    with open(f"input/{file}", encoding='cp1252') as f:
        concatenated = concatenated + f.read()

# Step 2: Remove new lines

concatenated = concatenated.replace("\n", " ")

# Step 3: Group entries in list

entries_raw = re.findall("""<p><ent>.*?(?=<p><ent>)""", concatenated)

# Step 4: Convert entries_raw to entries

entries = []

for entry_raw in entries_raw:
    definitions_raw = get_definitions_raw(entry_raw)
    definitions = []

    for definition in definitions_raw:
        definition_texts = re.findall("""(?<=<def>).*?(?=</def>)""", definition)
        definition_sources = re.findall("""(?<=<source>).*?(?=</source>)""", definition)

        definitions_map = map(lambda text, source: Definition(text, source), definition_texts, definition_sources)
        definitions = list(definitions_map)

    word = get_word(entry_raw)
    pos = get_pos(entry_raw)
    entries.append(Entry(word, definitions, pos))

# Step 5: Format json string based on entryObjects

json_str = json.dumps(entries, default=json_handler)

# Step 6: Check json validity

try:
    json.loads(json_str)
except ValueError:
    print("Error: Json is invalid.")
    exit(-1)

# Step 7: Write file

with open("output.json", "w") as out:
    out.write(json_str)
