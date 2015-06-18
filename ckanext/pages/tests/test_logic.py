from ckan.plugins import toolkit
from ckan.new_tests import factories, helpers
from nose.tools import assert_in, assert_not_in
import ckan.model as model

from ckanext.pages import db


class TestUpdate(helpers.FunctionalTestBase):
    def setup(self):
        super(TestUpdate, self).setup()
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
                'content': '<a href="/test">Test</a>',
            },
            extra_environ=env,
        )
        response = response.follow(extra_environ=env)
        assert_in('<h1 class="page-heading">Allowed</h1>', response.body)
        if toolkit.check_ckan_version(min_version='2.3'):
            assert_in('<p><a href="/test">Test</a>', response.body)
        else:
            assert_in('<p>Test', response.body)

    @helpers.change_config('ckanext.pages.allow_html', 'False')
    def test_rendering_with_html_disallowed(self):
        env = {'REMOTE_USER': self.user['name'].encode('ascii')}
        response = self.app.post(
            url=toolkit.url_for('pages_edit', page='/test_html_page'),
            params={
                'title': 'Disallowed',
                'name': 'page_html_disallowed',
                'content': '<a href="/test">Test</a>',
            },
            extra_environ=env,
        )
        response = response.follow(extra_environ=env)
        assert_in('<h1 class="page-heading">Disallowed</h1>', response.body)
        assert_in('<p>Test', response.body)
        assert_not_in('<p><a href="/test">Test</a>', response.body)
