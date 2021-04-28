import pytest

import ckan.model as model

from ckanext.pages import db


@pytest.fixture
def pages_setup():
    if db.pages_table is None:
        db.init_db()


@pytest.fixture
def clean_pages():
    if db.pages_table is not None:
        model.Session.query(db.Page).delete()
        model.Session.commit()
