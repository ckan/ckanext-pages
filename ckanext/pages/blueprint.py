from flask import Blueprint

import ckanext.pages.utils as utils

pages = Blueprint('pages', __name__)


def index():
    return utils.pages_list_pages('page')


def pages_edit(page=None, data=None, errors=None, error_summary=None, page_type='pages'):
    return utils.pages_edit(page, data, errors, error_summary, page_type)


pages.add_url_rule(
    "/pages",
    view_func=index,
)

pages.add_url_rule("/pages_edit", view_func=pages_edit, endpoint='new')
pages.add_url_rule("/pages_edit/<page>", view_func=pages_edit, endpoint='edit')



'''
        map.connect('pages_delete', '/pages_delete{page:/.*|}',
                    action='pages_delete', ckan_icon='delete', controller=controller)
        map.connect('pages_edit', '/pages_edit{page:/.*|}',
                    action='pages_edit', ckan_icon='edit', controller=controller)
        map.connect('pages_index', '/pages',
                    action='pages_index', ckan_icon='file', controller=controller, highlight_actions='pages_edit pages_index pages_show')
        map.connect('pages_show', '/pages{page:/.*|}',
                    action='pages_show', ckan_icon='file', controller=controller, highlight_actions='pages_edit pages_index pages_show')
        map.connect('pages_upload', '/pages_upload',
                    action='pages_upload', controller=controller)

        map.connect('blog_delete', '/blog_delete{page:/.*|}',
                    action='blog_delete', ckan_icon='delete', controller=controller)
        map.connect('blog_edit', '/blog_edit{page:/.*|}',
                    action='blog_edit', ckan_icon='edit', controller=controller)
        map.connect('blog_index', '/blog',
                    action='blog_index', ckan_icon='file', controller=controller, highlight_actions='blog_edit blog_index blog_show')
        map.connect('blog_show', '/blog{page:/.*|}',
                    action='blog_show', ckan_icon='file', controller=controller, highlight_actions='blog_edit blog_index blog_show')
'''
