import sqlite3
import core
import click


def definitions_sqlite(definitions):
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
    with click.progressbar(enumerate(definitions), length=len(definitions), label="Inserting definitions") as definitions:
        for i, definition in definitions:
            definition = core.Definition(
                definition.word.replace("\"", "''"),
                definition.text.replace("\"", "''"),
                definition.source.replace("\"", "''"),
                definition.pos.replace("\"", "''")
            )
            db.execute(
                f"""
                INSERT INTO Definitions (id, word, text, source, pos) VALUES (
                    {i},
                    "{definition.word}",
                    "{definition.text}",
                    "{definition.source}",
                    "{definition.pos}"
                ) 
                """
            )

    # Close DB
    print("Closing database")

    db.commit()
    db.close()
