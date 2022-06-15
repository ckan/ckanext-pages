import pytest

from ckan.tests import factories, helpers


@pytest.mark.usefixtures("clean_db", "pages_setup")
class TestPagesActions():

    def test_pages_create_action(self, app):
        user = factories.User()
        helpers.call_action(
            'ckanext_pages_update',
            {'user': user['name']},
            name='page_name', title='New Page', content='This is a test content'
        )

        page = helpers.call_action(
            'ckanext_pages_show',
            {},
            page='page_name')

        assert page['name'] == 'page_name'
        assert page['title'] == 'New Page'
        assert page['content'] == 'This is a test content'

    def test_pages_update_action(self, app):
        user = factories.User()
        helpers.call_action(
            'ckanext_pages_update',
            {'user': user['name']},
            name='page_name', title='New Page', content='This is a test content'
        )

        page = helpers.call_action(
            'ckanext_pages_show',
            {},
            page='page_name')

        assert page['name'] == 'page_name'
        assert page['title'] == 'New Page'
        assert page['content'] == 'This is a test content'

        # sending the parameter page is mandatory for the validator to pass.
        helpers.call_action(
            'ckanext_pages_update',
            {'user': user['name']},
            name='page_name', title='New Page Updated', content='This is a test content updated', page='page_name'
        )

        page = helpers.call_action(
            'ckanext_pages_show',
            {},
            page='page_name')

        assert page['name'] == 'page_name'
        assert page['title'] == 'New Page Updated'
        assert page['content'] == 'This is a test content updated'
