import click
import gcide_parser
import gcide_sqlite
import gcide_serializer

@click.group()
def cli():
    pass

@cli.command()
def json():
    click.echo("json")

@cli.command()
def sqlite():
    click.echo("sqlite")