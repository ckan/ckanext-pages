from flask import Blueprint
from ckan import model
import ckanext.pages.utils as utils
from ckanext.pages.utils import validate_main_page, update_main_page
from ckanext.pages.db import MainPage, Page
from flask import jsonify

import ckan.plugins.toolkit as tk 
from ckanext.pages.db import Page



pages = Blueprint('pages', __name__)

def index(page_type='page'):
    return utils.pages_list_pages(page_type)


def show(page, page_type='page'):
    return utils.pages_show(page, page_type)




def pages_edit(page=None, data=None, errors=None, error_summary=None, page_type='page'):
    return utils.pages_edit(page, data, errors, error_summary, page_type)

def pages_toggle_visibility(page):
    try:
        page_data = model.Session.query(Page).filter_by(id=page).first()
        if not page_data:
            return jsonify({'error': 'The requested page does not exist'}), 404

        page_data.hidden = not page_data.hidden
        model.Session.commit()

        return jsonify({'hidden': page_data.hidden}), 200
    except Exception as e:
        import logging
        logging.error(f"Error toggling visibility for page {page}: {str(e)}")

        model.Session.rollback()

        return jsonify({'error': 'An error occurred while processing your request. Please try again later.'}), 500

def upload():
    return utils.pages_upload()

def blog_index():
    return utils.pages_list_pages('blog')

def blog_show(page):
    return utils.pages_show(page, page_type='blog')

def blog_edit(page=None, data=None, errors=None, error_summary=None):
    return utils.pages_edit(page, data, errors, error_summary, 'blog')

def blog_delete(page):
    return utils.blog_delete(page, page_type='blog')

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

def events_edit(page=None, data=None, errors=None, error_summary=None):
    return utils.events_edit(page, data, errors, error_summary)

def events_delete(id):
    return utils.events_delete(id)

def news():
    return utils.news_list()

def news_edit(page=None, data=None, errors=None, error_summary=None):
    return utils.news_edit(page, data, errors, error_summary)

def news_delete(id):
    return utils.news_delete(id)

def news_toggle_visibility(news_id):
    return utils.news_toggle_visibility(news_id)

def pages_delete(id):
    return utils.pages_delete(id)


pages.add_url_rule('/events_edit', view_func=events_edit, endpoint='events_new', methods=['GET', 'POST'])
pages.add_url_rule('/events_edit/', view_func=events_edit, endpoint='events_new', methods=['GET', 'POST'])
pages.add_url_rule('/events_edit/<page>', view_func=events_edit, endpoint='events_edit', methods=['GET', 'POST'])

pages.add_url_rule('/events_delete/<id>', view_func=events_delete, endpoint='events_delete', methods=['POST', 'GET'])

# News Editing
pages.add_url_rule('/news_edit', view_func=news_edit, endpoint='news_new', methods=['GET', 'POST'])
pages.add_url_rule('/news_edit/', view_func=news_edit, endpoint='news_new', methods=['GET', 'POST'])
pages.add_url_rule('/news_edit/<page>', view_func=news_edit, endpoint='news_edit', methods=['GET', 'POST'])
pages.add_url_rule('/news_delete/<id>', view_func=news_delete, endpoint='news_delete', methods=['POST', 'GET'])



pages.add_url_rule('/events', view_func=events, methods=['GET'])
pages.add_url_rule('/news', view_func=news, methods=['GET'])


# News
pages.add_url_rule("/news", view_func=index, endpoint="news_index")
pages.add_url_rule("/news/<page>", view_func=show, endpoint="news_show")
pages.add_url_rule("/news_toggle_visibility/<news_id>",view_func=news_toggle_visibility,endpoint='news_toggle_visibility',methods=['POST'])



pages.add_url_rule("/main_page/edit/<section_id>", view_func=main_page_edit, endpoint="main_page_edit", methods=['GET', 'POST'])

pages.add_url_rule("/main_page", view_func=main_page, endpoint="main_page")

# General Pages
pages.add_url_rule("/pages", view_func=index, endpoint="pages_index", methods=['GET'])
pages.add_url_rule("/pages/<page>", view_func=show)

# General Page Editing
pages.add_url_rule("/pages_edit", view_func=pages_edit, endpoint='new', methods=['GET', 'POST'])
pages.add_url_rule("/pages_edit/", view_func=pages_edit, endpoint='new', methods=['GET', 'POST'])
pages.add_url_rule("/pages_edit/<page>", view_func=pages_edit, endpoint='edit', methods=['GET', 'POST'])

# General Page Deletion
pages.add_url_rule('/pages_delete/<id>', view_func=pages_delete, endpoint='pages_delete', methods=['GET', 'POST'])

# Toggle Page Visibility
pages.add_url_rule("/pages_toggle_visibility/<page>",view_func=pages_toggle_visibility,endpoint='toggle_visibility',methods=['POST'])


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

