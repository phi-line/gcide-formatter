import click
import gcide_parser
import definitions_sqlite
import definitions_json
import gcide_downloader


@click.group()
def cli():
    """
    Transforms GCIDE_XML into structured data formats (JSON or SQLite3-database). Gcide-Formatter
    Parses only definitions and their respective sources and part of speech.
    """
    pass


@cli.command()
def json():
    """
    Creates 'gcide.json' file.

    \b
    JSON Format example:
    [
        ...
        {
            "id":12,
            "word":"prolong",
            "text":"To put off to a distant time; to postpone",
            "source":"1913 Webster",
            "pos":"v. t."
        }
        ...
    ]
    """
    click.echo("json")


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
    click.echo("sqlite")
