import click
import gcide_parser
import gcide_sqlite
import gcide_serializer

@click.command()
def cli():
    """Example script."""
    click.echo('Hello World!')