#!/usr/bin/env python

import gcide_to_json_converter as gcide_json
import json
import sqlite3


class Definition:
    def __init__(self, db_id, word, text, source, pos):
        self.db_id = db_id
        self.word = word
        self.text = text
        self.source = source
        self.pos = pos


# Step 1: Get json
print("Retrieving json")

json_str = gcide_json.get_json()

# Step 2: Deserialize json
print("Deserializing json")

entries = json.loads(json_str)
entries = map(lambda j: gcide_json.Entry.from_json(j), entries)
entries = list(entries)

# Step 3: Convert entries to definitions

definitions = []

for i, entry in enumerate(entries):
    for definition in entry.definitions:
        d = Definition(i, entry.word, definition.text, definition.source, entry.word)
        definitions.append(d)

# Step 4: Create an Sqlite3 database
print("Creating gcide.db")

db = sqlite3.connect("gcide.db")

# Step 5: Create a table
print("Creating Definitions table")

db.execute(
    """
    CREATE TABLE Definitions (
    id          INT         NOT NULL    PRIMARY KEY,
    word        TEXT        NOT NULL,
    text        TEXT        NOT NULL,
    source      TEXT        NOT NULL,
    pos         TEXT        NOT NULL
    );
    """
)

db.close()
