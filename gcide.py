import click
import gcide_parser
import definitions_sqlite
import definitions_json
import gcide_downloader


@click.group()
def cli():
    """
    Transforms GCIDE_XML into structured data formats (JSON or SQLite3-database). Gcide-Formatter
    parses definitions and their respective sources and part of speech.
    """
    pass


@cli.command()
def json():
    """
    Creates 'gcide.json' file. It consists of an array of JSON objects.

    \b
    JSON object format:
    {
        "word":"prolong",
        "text":"To put off to a distant time; to postpone",
        "source":"1913 Webster",
        "pos":"v. t."
    }
    """
    definitions = gcide_parser.xml_to_objects()
    json = definitions_json.definitions_json(definitions)
    with open("gcide.json", "w") as file:
        file.write(json)


@cli.command()
def sqlite():
    """
    Creates 'gcide.db' file.

    \b
    Definitions table columns:
    id          INT         NOT NULL    PRIMARY KEY,
    word        TEXT        NOT NULL,
    text        TEXT        NOT NULL,
    source      TEXT        NOT NULL,
    pos         TEXT        NOT NULL

    """
    definitions = gcide_parser.xml_to_objects()
    definitions_sqlite.definitions_sqlite(definitions)
