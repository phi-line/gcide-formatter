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
    for definition_escaped in entry.definitions:
        d = Definition(i, entry.word, definition_escaped.text, definition_escaped.source, entry.pos)
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

# Step 6: Insert definitions to table
print("Inserting definitions")

for definition in definitions:
    definition_escaped = Definition(
        definition.db_id,
        definition.word.replace("\"", "''"),
        definition.text.replace("\"", "''"),
        definition.source.replace("\"", "''"),
        definition.pos.replace("\"", "''")
    )
    print("===")
    print(definition_escaped.db_id)
    print(definition_escaped.word)
    print(definition_escaped.text)
    print(definition_escaped.pos)
    print("===")
    db.execute(
        f"""
        INSERT INTO Definitions (id, word, text, source, pos) VALUES
        ({definition_escaped.db_id}, "{definition_escaped.word}", "{definition_escaped.text}", "{definition_escaped.source}", "{definition_escaped.pos}")
        """
    )

db.close()
