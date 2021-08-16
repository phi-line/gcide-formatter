import click
import core
import definitions_sqlite
import definitions_json
import gcide_downloader


@click.group()
@click.option('--fetch-xml', default=False, help='Download GCIDE_XML files from ibiblio.org/webster/.')
@click.option('--gcide-dir', default='xml_files', help='GCIDE_XML directory path.')
def cli(fetch_xml, gcide_dir):
    """
    Transforms GCIDE_XML into structured data formats (JSON or SQLite3-database). Gcide-Formatter
    parses definitions and their respective sources and part of speech.

    A gcide_xml directory is required. You can automatically download it using the --fetch option
    or download it yourself and pass the directory containing the xml files using the --gcide-dir
    option.

    Learn more about GCIDE_XML on ibiblio.org/webster/.
    """
    if (fetch):
        gcide_downloader.download_gcide_xml()
    else:
        global gcide_dir = gcide_dir
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
    definitions = core.xml_to_objects()
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
    definitions = core.xml_to_objects()
    definitions_sqlite.definitions_sqlite(definitions)
