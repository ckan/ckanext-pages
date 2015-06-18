from ckan.plugins import toolkit
from ckan.new_tests import factories, helpers


class TestUpdate(helpers.FunctionalTestBase):
    def setup(self):
        super(TestUpdate, self).setup()
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
        assert '<h1 class="page-heading">Page Title</h1>' in response.body

    @helpers.change_config('ckanext.pages.allow_html', 'True')
    def test_rendering_with_html_allowed(self):
        env = {'REMOTE_USER': self.user['name'].encode('ascii')}
        response = self.app.post(
            url=toolkit.url_for('pages_edit', page='/test_html_page'),
            params={
                'title': 'HTML allowed',
                'name': 'page_html_allowed',
                'content': '<a href="/test">Test</a>',
            },
            extra_environ=env,
        )
        response = response.follow(extra_environ=env)
        if toolkit.check_ckan_version(min_version='2.3'):
            assert '<h1 class="page-heading">HTML allowed</h1><a href="/test">Test</a>' in response.body
        else:
            assert '<h1 class="page-heading">HTML allowed</h1>Test' in response.body

    @helpers.change_config('ckanext.pages.allow_html', 'False')
    def test_rendering_with_html_disallowed(self):
        env = {'REMOTE_USER': self.user['name'].encode('ascii')}
        response = self.app.post(
            url=toolkit.url_for('pages_edit', page='/test_html_page'),
            params={
                'title': 'HTML disallowed',
                'name': 'page_html_disallowed',
                'content': '<a href="/test">Test</a>',
            },
            extra_environ=env,
        )
        response = response.follow(extra_environ=env)
        assert '<h1 class="page-heading">HTML disallowed</h1>Test' in response.body
