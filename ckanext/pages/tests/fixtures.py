import pytest

import ckan.model as model

from ckanext.pages import db


@pytest.fixture
def clean_db(reset_db, migrate_db_for):
    reset_db()
    migrate_db_for("pages")


@pytest.fixture
def clean_pages():
    if db.pages_table is not None:
        model.Session.query(db.Page).delete()
        model.Session.commit()
