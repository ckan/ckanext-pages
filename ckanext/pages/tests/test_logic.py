# encoding: utf-8

try:
    from unittest import mock
except ImportError:
    import mock
import pytest
from collections import OrderedDict
import datetime

from ckan.plugins import toolkit
from ckan.tests import factories, helpers

from ckanext.pages.logic import schema

ckan_29_or_higher = toolkit.check_ckan_version(u'2.9')


@pytest.mark.usefixtures("with_plugins", "clean_db")
@pytest.mark.ckan_config("ckan.plugins", "pages")
class TestPages():

    def test_create_page(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        page = 'test_page'
        response = app.post(
            url=toolkit.url_for('pages_edit', page=page),
            params={
                'title': 'Page Title',
                'name': 'page_name',
                'private': False,
            },
            extra_environ=env,
        )
        assert '<h1 class="page-heading">Page Title</h1>' in response.body

    @pytest.mark.ckan_config('ckanext.pages.allow_html', 'True')
    def test_rendering_with_html_allowed(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        page = 'test_html_page'
        response = app.post(
            url=toolkit.url_for('pages_edit', page=page),
            params={
                'title': 'Allowed',
                'name': 'page_html_allowed',
                'content': '<a href="/test">Test Link</a>',
                'private': False,
            },
            extra_environ=env,
        )
        assert '<h1 class="page-heading">Allowed</h1>' in response.body
        assert 'Test Link' in response.body

    @pytest.mark.ckan_config('ckanext.pages.allow_html', False)
    def test_rendering_with_html_disallowed(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        page = 'test_html_page'
        response = app.post(
            url=toolkit.url_for('pages_edit', page=page),
            params={
                'title': 'Disallowed',
                'name': 'page_html_disallowed',
                'content': '<a href="/test">Test Link</a>',
                'private': False,
            },
            extra_environ=env,
        )
        assert '<h1 class="page-heading">Disallowed</h1>' in response.body
        assert 'Test Link' in response.body
        assert '<a href="/test">Test Link</a>' not in response.body

    @pytest.mark.ckan_config('ckanext.pages.allow_html', False)
    def test_rendering_no_p_tags_added_with_html_disallowed(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        page = 'test_html_page_p'
        response = app.post(
            url=toolkit.url_for('pages_edit', page=page),
            params={
                'title': 'Disallowed',
                'name': 'page_html_disallowed_p',
                'content': 'Hi there **you**',
                'private': False,
            },
            extra_environ=env,
        )
        assert '<p>Hi there <strong>you</strong></p>' in response.body

    @pytest.mark.ckan_config('ckanext.pages.allow_html', True)
    def test_rendering_no_div_tags_added_with_html_allowed(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        page = 'test_html_page_div'
        response = app.post(
            url=toolkit.url_for('pages_edit', page=page),
            params={
                'title': 'Disallowed',
                'name': 'page_html_allowed_div',
                'content': '<p>Hi there</p>',
                'private': False,
            },
            extra_environ=env,
        )
        assert '<p>Hi there</p>' in response.body
        assert '<div><p>Hi there</p></div>' not in response.body

    def test_pages_index(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        url = toolkit.url_for('pages.pages_index')
        response = app.get(url, status=200, extra_environ=env)
        assert '<h1 class="page-heading page-list-header">Pages</h1>' in response.body
        assert 'Add page</a>' in response.body

    def test_blog_index(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        endpoint = 'pages.blog_index'
        url = toolkit.url_for(endpoint)
        response = app.get(url, status=200, extra_environ=env)
        assert '<h1 class="page-heading page-list-header">Blog</h1>' in response.body
        assert 'Add Article</a>' in response.body

    def test_organization_pages_index(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        org = factories.Organization()

        endpoint = 'pages.organization_pages_index'
        url = toolkit.url_for(endpoint, id=org['id'])
        response = app.get(url, status=200, extra_environ=env)
        assert '<h1 class="page-heading page-list-header">Pages</h1>' in response.body
        assert 'Add page</a>' in response.body

    def test_group_pages_index(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        group = factories.Group()
        endpoint = 'pages.group_pages_index'
        url = toolkit.url_for(endpoint, id=group['id'])
        response = app.get(url, status=200, extra_environ=env)
        assert '<h1 class="page-heading page-list-header">Pages</h1>' in response.body
        assert 'Add page</a>' in response.body

    def test_unicode(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        page = 'test_html_page_div'
        response = app.post(
            url=toolkit.url_for('pages_edit', page=page),
            params={
                'title': u'Tïtlé'.encode('utf-8'),
                'name': 'page_unicode',
                'content': u'Çöñtéñt'.encode('utf-8'),
                'order': 1,
                'private': False,
            },
            extra_environ=env,
        )

        assert u'<p>Çöñtéñt</p>' in response.get_data(as_text=True)
        assert u'<title>Tïtlé - CKAN</title>' in response.get_data(as_text=True)
        assert u'<a href="/pages/page_unicode">Tïtlé</a>' in response.get_data(as_text=True)
        assert u'<h1 class="page-heading">Tïtlé</h1>' in response.get_data(as_text=True)

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

    def test_cannot_create_page_with_same_name(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}
        page = 'test_page'
        response = app.post(
            url=toolkit.url_for('pages.new', page=page),
            params={
                'title': 'Page Title',
                'name': 'page_name',
                'private': False,
            },
            extra_environ=env,
        )
        assert '<h1 class="page-heading">Page Title</h1>' in response.body

        response = app.post(
            url=toolkit.url_for('pages.new', page=page),
            params={
                'title': 'Page Title',
                'name': 'page_name',
                'private': False,
            },
            extra_environ=env,
        )

        assert '<div class="flash-messages">' in response.body
        assert 'Page name already exists' in response.body

    def test_revisions_page(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}

        helpers.call_action(
            "ckanext_pages_update",
            {"user": user["name"]},
            name="page_name",
            title="New Page",
            content="This is a test content",
        )

        response = app.get(
            toolkit.url_for('pages.pages_revisions', page="page_name"),
            status=200, extra_environ=env)

        assert '<span class="badge badge-inverse">Active Revision</span>' in response.body

        response = app.get(
            toolkit.url_for('pages.pages_revisions', page="page_name1"),
            status=404, extra_environ=env)

        assert '404 Not Found' in response.body

        if toolkit.check_ckan_version(min_version="2.10.0"):
            response = app.get(
                toolkit.url_for('pages.pages_revisions', page="page_name"),
                status=401)

            assert '<h1>401 Unauthorized</h1>' in response.body
        else:
            response = app.get(
                toolkit.url_for('pages.pages_revisions', page="page_name")
            )
            assert '<h1 class="page-heading">Login</h1>' in response.body

    def test_revision_preview_page(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}

        helpers.call_action(
            "ckanext_pages_update",
            {"user": user["name"]},
            name="page_name",
            title="New Page",
            content="This is a test content",
        )

        page = helpers.call_action("ckanext_pages_show", {}, page="page_name")

        revision_id = [i for i in page['revisions']][0]

        response = app.get(
            toolkit.url_for(
                'pages.pages_revisions_preview',
                page="page_name",
                revision=revision_id),
            status=200, extra_environ=env)

        assert '<p>This is a test content</p>' in response.body

        response = app.get(
            toolkit.url_for(
                'pages.pages_revisions_preview',
                page="page_name",
                revision=revision_id + '1'),
            status=404, extra_environ=env)

        assert '404 Not Found' in response.body

        if toolkit.check_ckan_version(min_version="2.10.0"):
            response = app.get(
                toolkit.url_for(
                    'pages.pages_revisions_preview',
                    page="page_name",
                    revision=revision_id),
                status=401)

            assert '<h1>401 Unauthorized</h1>' in response.body
        else:
            response = app.get(
                toolkit.url_for(
                    'pages.pages_revisions_preview',
                    page="page_name",
                    revision=revision_id),
            )
            assert '<h1 class="page-heading">Login</h1>' in response.body

    def test_revision_restore_page(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}

        helpers.call_action(
            "ckanext_pages_update",
            {"user": user["name"]},
            name="page_name",
            title="New Page",
            content="This is a test content",
        )

        helpers.call_action(
            "ckanext_pages_update",
            {"user": user["name"]},
            name="page_name",
            title="New Page Updated",
            content="This is a test content updated",
            page="page_name",
        )

        page = helpers.call_action("ckanext_pages_show", {}, page="page_name")

        assert page['content'] == 'This is a test content updated'

        revisions = page['revisions']

        sorted_revisions = OrderedDict(reversed(sorted(
                revisions.items(),
                key=lambda x: datetime.datetime.timestamp(
                    datetime.datetime.fromisoformat(x[1]['created'])
                    )
        )))

        last_revision = sorted_revisions.popitem()
        response = app.get(
            toolkit.url_for(
                'pages.pages_revision_restore',
                page="page_name",
                revision=last_revision[0]),
            status=200, extra_environ=env)

        assert 'Content from revision created on' in response.body

        response = app.get(
            toolkit.url_for(
                'pages.pages_revision_restore',
                page="page_name",
                revision=last_revision[0] + '1'),
            status=200, extra_environ=env)

        assert 'Bad values, please make sure that provided values exist' in response.body

        if toolkit.check_ckan_version(min_version="2.10.0"):
            response = app.get(
                toolkit.url_for(
                    'pages.pages_revision_restore',
                    page="page_name",
                    revision=last_revision[0]),
                status=401)

            assert '<h1>401 Unauthorized</h1>' in response.body
        else:
            response = app.get(
                toolkit.url_for(
                    'pages.pages_revision_restore',
                    page="page_name",
                    revision=last_revision[0]),
            )

            assert '<h1 class="page-heading">Login</h1>' in response.body

    def test_revisions_blog(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}

        helpers.call_action(
            "ckanext_pages_update",
            {"user": user["name"]},
            name="blog_name",
            title="New Blog",
            content="This is a test content",
            page_type="blog",
            publish_date="2024-10-15"
        )

        response = app.get(
            toolkit.url_for('pages.blog_revisions', page="blog_name"),
            status=200, extra_environ=env)

        assert '<span class="badge badge-inverse">Active Revision</span>' in response.body

        response = app.get(
            toolkit.url_for('pages.blog_revisions', page="blog_name1"),
            status=404, extra_environ=env)

        assert '404 Not Found' in response.body

        if toolkit.check_ckan_version(min_version="2.10.0"):
            response = app.get(
                toolkit.url_for('pages.blog_revisions', page="blog_name"),
                status=401)

            assert '<h1>401 Unauthorized</h1>' in response.body
        else:
            response = app.get(
                toolkit.url_for('pages.blog_revisions', page="blog_name"),
            )

            assert '<h1 class="page-heading">Login</h1>' in response.body

    def test_revision_preview_blog(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}

        helpers.call_action(
            "ckanext_pages_update",
            {"user": user["name"]},
            name="blog_name",
            title="New Blog",
            content="This is a test content",
            page_type="blog",
            publish_date="2024-10-15"
        )

        page = helpers.call_action("ckanext_pages_show", {}, page="blog_name")

        revision_id = [i for i in page['revisions']][0]

        response = app.get(
            toolkit.url_for(
                'pages.blog_revisions_preview',
                page="blog_name",
                revision=revision_id),
            status=200, extra_environ=env)

        assert '<p>This is a test content</p>' in response.body

        response = app.get(
            toolkit.url_for(
                'pages.blog_revisions_preview',
                page="blog_name",
                revision=revision_id + '1'),
            status=404, extra_environ=env)

        assert '404 Not Found' in response.body

        if toolkit.check_ckan_version(min_version="2.10.0"):
            response = app.get(
                toolkit.url_for(
                    'pages.blog_revisions_preview',
                    page="blog_name",
                    revision=revision_id),
                status=401)

            assert '<h1>401 Unauthorized</h1>' in response.body
        else:
            response = app.get(
                toolkit.url_for(
                    'pages.blog_revisions_preview',
                    page="blog_name",
                    revision=revision_id),
            )
            assert '<h1 class="page-heading">Login</h1>' in response.body

    def test_revision_restore_blog(self, app):
        user = factories.Sysadmin()
        env = {'REMOTE_USER': user['name'].encode('ascii')}

        helpers.call_action(
            "ckanext_pages_update",
            {"user": user["name"]},
            name="blog_name",
            title="New Blog",
            content="This is a test content",
            page_type="blog",
            publish_date="2024-10-15"
        )

        helpers.call_action(
            "ckanext_pages_update",
            {"user": user["name"]},
            name="blog_name",
            title="New Blog Updated",
            content="This is a test content updated",
            page="blog_name",
            page_type="blog",
            publish_date="2024-10-15"
        )

        page = helpers.call_action("ckanext_pages_show", {}, page="blog_name")

        assert page['content'] == 'This is a test content updated'

        revisions = page['revisions']

        sorted_revisions = OrderedDict(reversed(sorted(
                revisions.items(),
                key=lambda x: datetime.datetime.timestamp(
                    datetime.datetime.fromisoformat(x[1]['created'])
                    )
        )))

        last_revision = sorted_revisions.popitem()

        response = app.get(
            toolkit.url_for(
                'pages.blog_revision_restore',
                page="blog_name",
                revision=last_revision[0]),
            status=200, extra_environ=env)

        assert 'Content from revision created on' in response.body

        response = app.get(
            toolkit.url_for(
                'pages.blog_revision_restore',
                page="blog_name",
                revision=last_revision[0] + '1'),
            status=200, extra_environ=env)

        assert 'Bad values, please make sure that provided values exist' in response.body

        if toolkit.check_ckan_version(min_version="2.10.0"):
            response = app.get(
                toolkit.url_for(
                    'pages.blog_revision_restore',
                    page="blog_name",
                    revision=last_revision[0]),
                status=401)

            assert '<h1>401 Unauthorized</h1>' in response.body
        else:
            response = app.get(
                toolkit.url_for(
                    'pages.blog_revision_restore',
                    page="blog_name",
                    revision=last_revision[0]),
            )

            assert '<h1 class="page-heading">Login</h1>' in response.body
