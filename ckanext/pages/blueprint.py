from flask import Blueprint

import ckanext.pages.utils as utils

pages = Blueprint('pages', __name__)


def index():
    return utils.pages_list_pages('page')


def blog_index():
    return utils.pages_list_pages('blog')


def show(page):
    return utils.pages_show(page, page_type='page')


def blog_show(page):
    return utils.pages_show(page, page_type='blog')


def pages_edit(page=None, data=None, errors=None, error_summary=None):
    return utils.pages_edit(page, data, errors, error_summary, 'page')


def blog_edit(page=None, data=None, errors=None, error_summary=None):
    return utils.pages_edit(page, data, errors, error_summary, 'blog')


def pages_delete(page):
    return utils.pages_delete(page, page_type='pages')


def blog_delete(page):
    return utils.pages_delete(page, page_type='blog')


def upload():
    return utils.pages_upload()


pages.add_url_rule("/pages", view_func=index)
pages.add_url_rule("/pages/<page>", view_func=show)

pages.add_url_rule("/pages_edit", view_func=pages_edit, endpoint='new', methods=['GET', 'POST'])
pages.add_url_rule("/pages_edit/", view_func=pages_edit, endpoint='new', methods=['GET', 'POST'])
pages.add_url_rule("/pages_edit/<page>", view_func=pages_edit, endpoint='edit', methods=['GET', 'POST'])

pages.add_url_rule("/pages_delete/<page>", view_func=pages_delete, endpoint='delete', methods=['GET', 'POST'])

pages.add_url_rule("/pages_upload", view_func=upload, methods=['GET', 'POST'])


pages.add_url_rule("/blog", view_func=blog_index)
pages.add_url_rule("/blog/<page>", view_func=blog_show)

pages.add_url_rule("/blog_edit", view_func=blog_edit, endpoint='blog_new', methods=['GET', 'POST'])
pages.add_url_rule("/blog_edit/", view_func=blog_edit, endpoint='blog_new', methods=['GET', 'POST'])
pages.add_url_rule("/blog_edit/<page>", view_func=blog_edit, endpoint='blog_edit', methods=['GET', 'POST'])

pages.add_url_rule("/blog_delete/<page>", view_func=blog_delete, endpoint='blog_delete', methods=['GET', 'POST'])
