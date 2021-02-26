# encoding: utf-8

import pytest

from ckan.plugins import toolkit
import mock
from ckantoolkit.tests import factories, helpers

from ckanext.pages.logic import schema


@pytest.mark.usefixtures("clean_db", "pages_setup")
class TestPages():

    def test_create_page(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        response = app.post(
            url=toolkit.url_for('pages_edit', page='/test_page'),
            params={
                'title': 'Page Title',
                'name': 'page_name',
            },
            extra_environ=env,
        )
        assert '<h1 class="page-heading">Page Title</h1>' in response.body

    @pytest.mark.ckan_config('ckanext.pages.allow_html', 'True')
    def test_rendering_with_html_allowed(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        response = app.post(
            url=toolkit.url_for('pages_edit', page='/test_html_page'),
            params={
                'title': 'Allowed',
                'name': 'page_html_allowed',
                'content': '<a href="/test">Test Link</a>',
            },
            extra_environ=env,
        )
        response = response.follow(extra_environ=env)
        assert '<h1 class="page-heading">Allowed</h1>' in response.body
        if toolkit.check_ckan_version(min_version='2.3'):
            assert '<a href="/test">Test Link</a>' in response.body
        else:
            assert 'Test Link' in response.body

    @pytest.mark.ckan_config('ckanext.pages.allow_html', False)
    def test_rendering_with_html_disallowed(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        response = app.post(
            url=toolkit.url_for('pages_edit', page='/test_html_page'),
            params={
                'title': 'Disallowed',
                'name': 'page_html_disallowed',
                'content': '<a href="/test">Test Link</a>',
            },
            extra_environ=env,
        )
        response = response.follow(extra_environ=env)
        assert '<h1 class="page-heading">Disallowed</h1>' in response.body
        assert 'Test Link' in response.body
        assert '<a href="/test">Test Link</a>' not in response.body

    @pytest.mark.ckan_config('ckanext.pages.allow_html', False)
    def test_rendering_no_p_tags_added_with_html_disallowed(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        response = app.post(
            url=toolkit.url_for('pages_edit', page='/test_html_page_p'),
            params={
                'title': 'Disallowed',
                'name': 'page_html_disallowed_p',
                'content': 'Hi there **you**',
            },
            extra_environ=env,
        )
        response = response.follow(extra_environ=env)
        assert '<p>Hi there <strong>you</strong></p>' in response.body

    @pytest.mark.ckan_config('ckanext.pages.allow_html', True)
    def test_rendering_no_div_tags_added_with_html_allowed(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        response = app.post(
            url=toolkit.url_for('pages_edit', page='/test_html_page_div'),
            params={
                'title': 'Disallowed',
                'name': 'page_html_allowed_div',
                'content': '<p>Hi there</p>',
            },
            extra_environ=env,
        )
        response = response.follow(extra_environ=env)
        assert '<p>Hi there</p>' in response.body
        assert '<div><p>Hi there</p></div>' not in response.body

    def test_pages_index(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        url = toolkit.url_for('pages_index')
        response = app.get(url, status=200, extra_environ=env)
        assert '<h2>Pages</h2>' in response.body
        assert 'Add page</a>' in response.body

    def test_blog_index(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        url = toolkit.url_for('blog_index')
        response = app.get(url, status=200, extra_environ=env)
        assert '<h2>Blog</h2>' in response.body
        assert 'Add Article</a>' in response.body

    def test_organization_pages_index(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        org = factories.Organization()
        url = toolkit.url_for('organization_pages_index', id=org['id'])
        response = app.get(url, status=200, extra_environ=env)
        assert '<h2>Pages</h2>' in response.body
        assert 'Add page</a>' in response.body

    def test_group_pages_index(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        group = factories.Group()
        url = toolkit.url_for('group_pages_index', id=group['id'])
        response = app.get(url, status=200, extra_environ=env)
        assert '<h2>Pages</h2>' in response.body
        assert 'Add page</a>' in response.body

    def test_unicode(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        response = app.post(
            url=toolkit.url_for('pages_edit', page='/test_unicode_page'),
            params={
                'title': u'Tïtlé'.encode('utf-8'),
                'name': 'page_unicode',
                'content': u'Çöñtéñt'.encode('utf-8'),
                'order': 1,
                'private': False,
            },
            extra_environ=env,
        )
        response = response.follow(extra_environ=env)
        assert u'<title>Tïtlé - CKAN</title>' in response.unicode_body
        assert u'<a href="/pages/page_unicode">Tïtlé</a>' in response.unicode_body
        assert u'<h1 class="page-heading">Tïtlé</h1>' in response.unicode_body
        if toolkit.check_ckan_version(min_version='2.8.0'):
            assert u'<p>&#199;&#246;&#241;t&#233;&#241;t</p>' in response.unicode_body
        else:
            assert u'<p>Çöñtéñt</p>' in response.unicode_body

    def test_pages_saves_custom_schema_fields(self, app):
        user = factories.Sysadmin()
        context = {'user': user['name']}

        mock_schema = schema.default_pages_schema()
        mock_schema.update({
            'new_field': [toolkit.get_validator('ignore_missing')],
        })

        with mock.patch('ckanext.pages.actions.update_pages_schema', return_value=mock_schema):
            helpers.call_action(
                'ckanext_pages_update',
                context=context,
                title='Page Title',
                name='page_name',
                page='page_name',
                new_field='new_field_value',
                content='test',
            )

        pages = helpers.call_action('ckanext_pages_list', context)
        assert pages[0]['new_field'] == 'new_field_value'
