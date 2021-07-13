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


# Get definitions
print("Getting definitions")

definitions = gcide_json.get_definitions()

# Create an Sqlite3 database
print("Creating gcide.db")

db = sqlite3.connect("gcide.db")

# Create a table
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

# Insert definitions to table
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

# Close DB
print("Closing database")

db.commit()
db.close()
