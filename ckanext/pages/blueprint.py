from flask import Blueprint
from ckan import model
import ckanext.pages.utils as utils
from ckanext.pages.utils import validate_main_page, update_main_page
from ckanext.pages.db import MainPage, Page
from flask import request
from slugify import slugify
import os
import ckan.plugins.toolkit as tk 
from ckanext.pages.db import Page
from werkzeug.utils import secure_filename
import os



pages = Blueprint('pages', __name__)

def index(page_type='page'):
    return utils.pages_list_pages(page_type)


def show(page, page_type='page'):
    return utils.pages_show(page, page_type)




def pages_edit(page=None, data=None, errors=None, error_summary=None, page_type='page'):
    return utils.pages_edit(page, data, errors, error_summary, page_type)


def pages_delete(page):
    return utils.pages_delete(page, page_type='page')

def upload():
    return utils.pages_upload()

def blog_index():
    return utils.pages_list_pages('blog')

def blog_show(page):
    return utils.pages_show(page, page_type='blog')

def blog_edit(page=None, data=None, errors=None, error_summary=None):
    return utils.pages_edit(page, data, errors, error_summary, 'blog')

def blog_delete(page):
    return utils.pages_delete(page, page_type='blog')

def org_show(id, page=None):
    return utils.group_show(id, 'organization', page)

def org_edit(id, page=None, data=None, errors=None, error_summary=None):
    return utils.group_edit(id, 'organization', page, data, errors, error_summary)

def org_delete(id, page):
    return utils.group_delete(id, 'organization', page)

def group_show(id, page=None):
    return utils.group_show(id, 'group', page)

def group_edit(id, page=None, data=None, errors=None, error_summary=None):
    return utils.group_edit(id, 'group', page, data, errors, error_summary)

def group_delete(id, page):
    return utils.group_delete(id, 'group', page)

def main_page():
    return utils.main_page()

def main_page_edit(section_id, data=None, errors=None, error_summary=None):
    return utils.main_page_edit(section_id, data, errors, error_summary)

def get_main_page(section_id):
    return MainPage.get(id=section_id)

def events():
    return utils.events_list()

def events_edit(page=None):
    return utils.pages_show(page, 'event')

def news():
    return utils.news_list()

def news_edit(page=None):
    return utils.pages_show(page, 'news')


# Event Editing
pages.add_url_rule('/events_edit', view_func=events_edit, endpoint='events_new', methods=['GET', 'POST'])
pages.add_url_rule('/events_edit/', view_func=events_edit, endpoint='events_new', methods=['GET', 'POST'])
pages.add_url_rule('/events_edit/<event_id>', view_func=events_edit, endpoint='events_edit', methods=['GET', 'POST'])

# News Editing
pages.add_url_rule('/news_edit', view_func=news_edit, endpoint='news_new', methods=['GET', 'POST'])
pages.add_url_rule('/news_edit/', view_func=news_edit, endpoint='news_new', methods=['GET', 'POST'])
pages.add_url_rule('/news_edit/<news_id>', view_func=news_edit, endpoint='news_edit', methods=['GET', 'POST'])



pages.add_url_rule('/events', view_func=events, methods=['GET'])
pages.add_url_rule('/news', view_func=news, methods=['GET'])


# News
pages.add_url_rule("/news", view_func=index, endpoint="news_index")
pages.add_url_rule("/news/<page>", view_func=show, endpoint="news_show")

# News Deletion
pages.add_url_rule("/news_delete/<page>", view_func=pages_delete, endpoint='news_delete', methods=['GET', 'POST'])



pages.add_url_rule("/main_page/edit/<section_id>", view_func=main_page_edit, endpoint="main_page_edit", methods=['GET', 'POST'])

pages.add_url_rule("/main_page", view_func=main_page, endpoint="main_page")

# General Pages
pages.add_url_rule("/pages", view_func=index, endpoint="pages_index")
pages.add_url_rule("/pages/<page>", view_func=show)

# General Page Editing
pages.add_url_rule("/pages_edit", view_func=pages_edit, endpoint='new', methods=['GET', 'POST'])
pages.add_url_rule("/pages_edit/", view_func=pages_edit, endpoint='new', methods=['GET', 'POST'])
pages.add_url_rule("/pages_edit/<page>", view_func=pages_edit, endpoint='edit', methods=['GET', 'POST'])

# General Page Deletion
pages.add_url_rule("/pages_delete/<page>", view_func=pages_delete, endpoint='delete', methods=['GET', 'POST'])

# File Uploads
pages.add_url_rule("/pages_upload", view_func=upload, methods=['POST'])

# Blog Pages
pages.add_url_rule("/blog", view_func=blog_index)
pages.add_url_rule("/blog/<page>", view_func=blog_show)

# Blog Editing
pages.add_url_rule("/blog_edit", view_func=blog_edit, endpoint='blog_new', methods=['GET', 'POST'])
pages.add_url_rule("/blog_edit/", view_func=blog_edit, endpoint='blog_new', methods=['GET', 'POST'])
pages.add_url_rule("/blog_edit/<page>", view_func=blog_edit, endpoint='blog_edit', methods=['GET', 'POST'])

# Blog Deletion
pages.add_url_rule("/blog_delete/<page>", view_func=blog_delete, endpoint='blog_delete', methods=['GET', 'POST'])

# Organization Pages
pages.add_url_rule("/organization/pages/<id>", view_func=org_show, endpoint='organization_pages_index')
pages.add_url_rule("/organization/pages/<id>/<page>", view_func=org_show, endpoint='organization_pages_show')

# Organization Page Editing
pages.add_url_rule("/organization/pages_edit/<id>", view_func=org_edit, endpoint='organization_pages_new', methods=['GET', 'POST'])
pages.add_url_rule("/organization/pages_edit/<id>/", view_func=org_edit, endpoint='organization_pages_new', methods=['GET', 'POST'])
pages.add_url_rule("/organization/pages_edit/<id>/<page>", view_func=org_edit, endpoint='organization_pages_edit', methods=['GET', 'POST'])

# Organization Page Deletion
pages.add_url_rule("/organization/pages_delete/<id>/<page>", view_func=org_delete, endpoint='organization_pages_delete', methods=['GET', 'POST'])

# Group Pages
pages.add_url_rule("/group/pages/<id>", view_func=group_show, endpoint='group_pages_index')
pages.add_url_rule("/group/pages/<id>/<page>", view_func=group_show, endpoint='group_pages_show')

# Group Page Editing
pages.add_url_rule("/group/pages_edit/<id>", view_func=group_edit, endpoint='group_pages_new', methods=['GET', 'POST'])
pages.add_url_rule("/group/pages_edit/<id>/", view_func=group_edit, endpoint='group_pages_new', methods=['GET', 'POST'])
pages.add_url_rule("/group/pages_edit/<id>/<page>", view_func=group_edit, endpoint='group_pages_edit', methods=['GET', 'POST'])

# Group Page Deletion
pages.add_url_rule("/group/pages_delete/<id>/<page>", view_func=group_delete, endpoint='group_pages_delete', methods=['GET', 'POST'])

