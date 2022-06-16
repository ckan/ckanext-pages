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


    def test_pages_list(self, app):
        sysadmin = factories.Sysadmin()
        helpers.call_action(
            'ckanext_pages_update',
            {'user': sysadmin['name']},
            name='page_name_1', title='New Page 1', content='This is a test content', private=False
        )
        helpers.call_action(
            'ckanext_pages_update',
            {'user': sysadmin['name']},
            name='page_name_2', title='New Page 2', content='This is a test content', private=False
        )
        helpers.call_action(
            'ckanext_pages_update',
            {'user': sysadmin['name']},
            name='page_name_3', title='New Page 3', content='This is a test content', private=False
        )

        results = helpers.call_action(
            'ckanext_pages_list',
            {'user': sysadmin['name']}
            )

        assert len(results) == 3
        assert results[0]['title'] == 'New Page 3'
        assert results[2]['title'] == 'New Page 1'

        helpers.call_action(
            'ckanext_pages_update',
            {'user': sysadmin['name']},
            name='page_name_4', title='New Page 4', content='This is a test content', private=True
        )

        results = helpers.call_action(
            'ckanext_pages_list',
            {'user': sysadmin['name']}
            )
        assert len(results) == 4

        user = factories.User()
        results = helpers.call_action(
            'ckanext_pages_list',
            {'user': user['name'], 'ignore_auth': False}
            )
        assert len(results) == 3
