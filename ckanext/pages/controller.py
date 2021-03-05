import ckantoolkit

import ckan.plugins as p

import ckanext.pages.utils as utils

config = ckantoolkit.config

_ = p.toolkit._


class PagesController(p.toolkit.BaseController):

    def org_show(self, id, page=None):
        return utils.group_show(id, 'organization', page)

    def org_delete(self, id, page):
        return utils.group_delete(id, 'organization', page)

    def org_edit(self, id, page=None, data=None, errors=None, error_summary=None):
        return utils.group_edit(id, 'organization', page, data, errors, error_summary)

    def group_show(self, id, page=None):
        return utils.group_show(id, 'group', page)

    def group_delete(self, id, page):
        return utils.group_delete(id, 'group', page)

    def group_edit(self, id, page=None, data=None, errors=None, error_summary=None):
        return utils.group_edit(id, 'group', page, data, errors, error_summary)

    def blog_index(self):
        return utils.pages_list_pages('blog')

    def blog_show(self, page=None):
        return utils.pages_show(page, page_type='blog')

    def pages_show(self, page=None, page_type='page'):
        return utils.pages_show(page, page_type=page_type)

    def pages_index(self):
        return utils.pages_list_pages('page')

    def blog_delete(self, page):
        return utils.pages_delete(page, page_type='blog')

    def pages_delete(self, page, page_type='pages'):
        return utils.pages_delete(page, page_type='blog')

    def blog_edit(self, page=None, data=None, errors=None, error_summary=None):
        return utils.pages_edit(page, data, errors, error_summary, page_type='blog')

    def pages_edit(self, page=None, data=None, errors=None, error_summary=None, page_type='page'):
        return utils.pages_edit(page, data, errors, error_summary, page_type)

    def pages_upload(self):
        return utils.pages_upload()
