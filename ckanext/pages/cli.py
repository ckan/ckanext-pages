import click
from ckanext.pages.main_cli_func.main_cli import insert_main_page_rows


@click.group(short_help="pages CLI.")
def pages():
    """pages CLI.
    """
    pass


@pages.command()
@click.argument("name", default="pages")
def command(name):
    """Docs.
    """
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [pages]


@pages.command()
def insert_default_rows():
    insert_main_page_rows()


