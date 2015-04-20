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
