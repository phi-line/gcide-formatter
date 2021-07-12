#!/usr/bin/env python

import gcide_to_json_converter as gcide_json
import json
import sqlite3


class Definition:
    def __init__(self, word, text, source, pos):
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

for entry in entries:
    for definition_escaped in entry.definitions:
        d = Definition(entry.word, definition_escaped.text, definition_escaped.source, entry.pos)
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

for id, definition in enumerate(definitions):
    definition_escaped = Definition(
        definition.word.replace("\"", "''"),
        definition.text.replace("\"", "''"),
        definition.source.replace("\"", "''"),
        definition.pos.replace("\"", "''")
    )
    db.execute(
        f"""
        INSERT INTO Definitions (id, word, text, source, pos) VALUES (
            {id},
            "{definition_escaped.word}",
            "{definition_escaped.text}",
            "{definition_escaped.source}",
            "{definition_escaped.pos}"
        ) 
        """
    )

db.commit()
db.close()
