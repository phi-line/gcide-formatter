#!/usr/bin/env python

import gcide_parser
import sqlite3

"""
Inserts parsed definitions to sqlite database
"""

# Get definitions
print("Getting definitions")

definitions = gcide_parser.get_definitions()

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
    definition_escaped = gcide_parser.Definition(
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
