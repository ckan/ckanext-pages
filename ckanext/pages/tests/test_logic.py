# encoding: utf-8

from ckan.plugins import toolkit
from nose.tools import assert_in, assert_not_in, assert_equals
import mock
import ckan.model as model
try:
    from ckan.tests import factories, helpers
except ImportError:
    from ckan.new_tests import factories, helpers

from ckanext.pages import db
from ckanext.pages.logic import schema


class TestPages(helpers.FunctionalTestBase):
    def setup(self):
        super(TestPages, self).setup()
        if db.pages_table is None:
            db.init_db(model)
        self.user = factories.Sysadmin()
        self.app = self._get_test_app()

    def teardown(self):
        helpers.reset_db()

    def test_create_page(self):
        env = {'REMOTE_USER': self.user['name'].encode('ascii')}
        response = self.app.post(
            url=toolkit.url_for('pages_edit', page='/test_page'),
            params={
                'title': 'Page Title',
                'name': 'page_name',
            },
            extra_environ=env,
        )
        response = response.follow(extra_environ=env)
        assert_in('<h1 class="page-heading">Page Title</h1>', response.body)

    @helpers.change_config('ckanext.pages.allow_html', 'True')
    def test_rendering_with_html_allowed(self):
        env = {'REMOTE_USER': self.user['name'].encode('ascii')}
        response = self.app.post(
            url=toolkit.url_for('pages_edit', page='/test_html_page'),
            params={
                'title': 'Allowed',
                'name': 'page_html_allowed',
                'content': '<a href="/test">Test Link</a>',
            },
            extra_environ=env,
        )
        response = response.follow(extra_environ=env)
        assert_in('<h1 class="page-heading">Allowed</h1>', response.body)
        if toolkit.check_ckan_version(min_version='2.3'):
            assert_in('<a href="/test">Test Link</a>', response.body)
        else:
            assert_in('Test Link', response.body)

    @helpers.change_config('ckanext.pages.allow_html', False)
    def test_rendering_with_html_disallowed(self):
        env = {'REMOTE_USER': self.user['name'].encode('ascii')}
        response = self.app.post(
            url=toolkit.url_for('pages_edit', page='/test_html_page'),
            params={
                'title': 'Disallowed',
                'name': 'page_html_disallowed',
                'content': '<a href="/test">Test Link</a>',
            },
            extra_environ=env,
        )
        response = response.follow(extra_environ=env)
        assert_in('<h1 class="page-heading">Disallowed</h1>', response.body)
        assert_in('Test Link', response.body)
        assert_not_in('<a href="/test">Test Link</a>', response.body)

    @helpers.change_config('ckanext.pages.allow_html', False)
    def test_rendering_no_p_tags_added_with_html_disallowed(self):
        env = {'REMOTE_USER': self.user['name'].encode('ascii')}
        response = self.app.post(
            url=toolkit.url_for('pages_edit', page='/test_html_page_p'),
            params={
                'title': 'Disallowed',
                'name': 'page_html_disallowed_p',
                'content': 'Hi there **you**',
            },
            extra_environ=env,
        )
        response = response.follow(extra_environ=env)
        assert_in('<p>Hi there <strong>you</strong></p>', response.body)

    @helpers.change_config('ckanext.pages.allow_html', True)
    def test_rendering_no_div_tags_added_with_html_allowed(self):
        env = {'REMOTE_USER': self.user['name'].encode('ascii')}
        response = self.app.post(
            url=toolkit.url_for('pages_edit', page='/test_html_page_div'),
            params={
                'title': 'Disallowed',
                'name': 'page_html_allowed_div',
                'content': '<p>Hi there</p>',
            },
            extra_environ=env,
        )
        response = response.follow(extra_environ=env)
        assert_in('<p>Hi there</p>', response.body)
        assert_not_in('<div><p>Hi there</p></div>', response.body)

    def test_pages_index(self):
        env = {'REMOTE_USER': self.user['name'].encode('ascii')}
        url = toolkit.url_for('pages_index')
        response = self.app.get(url, status=200, extra_environ=env)
        assert_in('<h2>Pages</h2>', response.body)
        assert_in('Add page</a>', response.body)

    def test_blog_index(self):
        env = {'REMOTE_USER': self.user['name'].encode('ascii')}
        url = toolkit.url_for('blog_index')
        response = self.app.get(url, status=200, extra_environ=env)
        assert_in('<h2>Blog</h2>', response.body)
        assert_in('Add Article</a>', response.body)

    def test_organization_pages_index(self):
        env = {'REMOTE_USER': self.user['name'].encode('ascii')}
        org = factories.Organization()
        url = toolkit.url_for('organization_pages_index', id=org['id'])
        response = self.app.get(url, status=200, extra_environ=env)
        assert_in('<h2>Pages</h2>', response.body)
        assert_in('Add page</a>', response.body)

    def test_group_pages_index(self):
        env = {'REMOTE_USER': self.user['name'].encode('ascii')}
        group = factories.Group()
        url = toolkit.url_for('group_pages_index', id=group['id'])
        response = self.app.get(url, status=200, extra_environ=env)
        assert_in('<h2>Pages</h2>', response.body)
        assert_in('Add page</a>', response.body)

    def test_unicode(self):
        env = {'REMOTE_USER': self.user['name'].encode('ascii')}
        response = self.app.post(
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
        assert_in(u'<title>Tïtlé - CKAN</title>', response.unicode_body)
        assert_in(u'<a href="/pages/page_unicode">Tïtlé</a>', response.unicode_body)
        assert_in(u'<h1 class="page-heading">Tïtlé</h1>', response.unicode_body)
        if toolkit.check_ckan_version(min_version='2.8.0'):
            assert_in(u'<p>&#199;&#246;&#241;t&#233;&#241;t</p>', response.unicode_body)
        else:
            assert_in(u'<p>Çöñtéñt</p>', response.unicode_body)

    def test_pages_saves_custom_schema_fields(self):
        context = {'user': self.user['name']}

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
        assert_equals(pages[0]['new_field'], 'new_field_value')
