import click
import ckanext.pages.db as db


def get_commands():
    return [pages]


@click.group()
def pages():
    pass


@pages.command()
def initdb():
    """Adds simple pages to ckan

    Usage:

        pages initdb
        - Creates the necessary tables in the database
    """
    db.init_db()
    click.secho(u"DB tables created", fg=u"green")
