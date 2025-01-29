from ckan import model
import ckanext.pages.utils as utils
from ckanext.pages.db import MainPage
from ckanext.pages.db import Page
from ckan.plugins.toolkit import get_action, check_access, NotAuthorized
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import jsonify
from ckan.common import _
from ckan import model
from ckan.lib import base
from flask import g


pages = Blueprint('pages', __name__)
header_management = Blueprint('header_management', __name__, url_prefix='/header_management')

@pages.before_request
def set_current_section():
    if request.endpoint == 'pages.pages_index' or request.endpoint == 'pages.new' or request.endpoint == 'pages.edit':
        g.current_section = 'pages'
    elif request.endpoint == 'pages.news' or request.endpoint == 'pages.news_new':
        g.current_section = 'news'
    elif request.endpoint == 'pages.events' or request.endpoint == 'pages.events_new':
        g.current_section = 'events'
    elif request.endpoint == 'pages.main_page' or request.endpoint == 'pages.main_page_edit':
        g.current_section = 'main_page'

@header_management.route('/')
def index():
    """Display the header management page."""
    # try:
    #     check_access('sysadmin', {})
    # except NotAuthorized:
    #     return base.abort(401, _(u'Unauthorized to access'))

    header_logo = utils.get_header_logo()
    main_menu = utils.get_main_menu()
    secondary_menu = utils.get_secondary_menu()

    return render_template(
        'ckanext_pages/header_management/index.html',
        header_logo=header_logo,
        main_menu=main_menu,
        secondary_menu=secondary_menu
    )

@header_management.route('/header_logo/edit/<id>', methods=['GET', 'POST'])
def edit_header_logo(id=None):
    """Edit or create a header logo."""
    try:
        check_access('sysadmin', {})
    except NotAuthorized:
        return base.abort(403, _(u'Unauthorized to access'))

    if request.method == 'POST':
        data = {
            'title_en': request.form.get('title_en'),
            'title_ar': request.form.get('title_ar'),
            'image_url': request.form.get('image_url'),
            'is_visible': request.form.get('is_visible') == 'on',
            'page_type': 'header_logo'
        }

        if id:
            # Update existing header logo
            utils.update_header_logo(id, data)
            flash('Header logo updated successfully!', 'success')
        else:
            # Create new header logo
            utils.create_header_logo(data)
            flash('Header logo created successfully!', 'success')

        return redirect(url_for('header_management.index'))

    header_logo = None
    if id:
        header_logo = utils.get_header_logo(id)

    return render_template('ckanext_pages/header_management/edit_header_logo.html', header_logo=header_logo)

@header_management.route('/header_logo/delete/<id>', methods=['POST'])
def delete_header_logo(id):
    """Delete a header logo."""
    try:
        check_access('sysadmin', {})
    except NotAuthorized:
        return render_template('403.html')

    utils.delete_header_logo(id)
    flash('Header logo deleted successfully!', 'success')

    return redirect(url_for('header_management.index'))

@header_management.route('/header_logo/toggle_visibility/<id>', methods=['POST'])
def toggle_header_logo_visibility(id):
    """Toggle visibility of a header logo."""
    try:
        check_access('sysadmin', {})
    except NotAuthorized:
        return render_template('403.html')

    utils.toggle_header_logo_visibility(id)
    return redirect(url_for('header_management.index'))

@header_management.route('/main_menu/edit/<id>', methods=['GET', 'POST'])
def edit_main_menu(id=None):
    """Edit or create a main menu item."""
    try:
        check_access('sysadmin', {})
    except NotAuthorized:
        return render_template('403.html')

    if request.method == 'POST':
        data = {
            'title_en': request.form.get('title_en'),
            'title_ar': request.form.get('title_ar'),
            'link_en': request.form.get('link_en'),
            'link_ar': request.form.get('link_ar'),
            'type': request.form.get('type'),
            'parent_id': request.form.get('parent_id'),
            'order': request.form.get('order'),
            'is_visible': request.form.get('is_visible') == 'on',
            'page_type': 'main_menu'
        }

        if id:
            # Update existing main menu item
            utils.update_main_menu(id, data)
            flash('Main menu item updated successfully!', 'success')
        else:
            # Create new main menu item
            utils.create_main_menu(data)
            flash('Main menu item created successfully!', 'success')

        return redirect(url_for('header_management.index'))

    # Fetch main menu data for editing
    main_menu = None
    if id:
        main_menu = utils.get_main_menu(id)

    return render_template('ckanext_pages/header_management/edit_main_menu.html', main_menu=main_menu)

@header_management.route('/main_menu/delete/<id>', methods=['POST'])
def delete_main_menu(id):
    """Delete a main menu item."""
    try:
        check_access('sysadmin', {})
    except NotAuthorized:
        return render_template('403.html')

    utils.delete_main_menu(id)
    flash('Main menu item deleted successfully!', 'success')

    return redirect(url_for('header_management.index'))

@header_management.route('/main_menu/toggle_visibility/<id>', methods=['POST'])
def toggle_main_menu_visibility(id):
    """Toggle visibility of a main menu item."""
    try:
        check_access('sysadmin', {})
    except NotAuthorized:
        return render_template('403.html')

    utils.toggle_main_menu_visibility(id)
    return redirect(url_for('header_management.index'))

@header_management.route('/secondary_menu/edit/<id>', methods=['GET', 'POST'])
def edit_secondary_menu(id=None):
    """Edit or create a secondary menu item."""
    try:
        check_access('sysadmin', {})
    except NotAuthorized:
        return render_template('403.html')

    if request.method == 'POST':
        data = {
            'title_en': request.form.get('title_en'),
            'title_ar': request.form.get('title_ar'),
            'link_en': request.form.get('link_en'),
            'link_ar': request.form.get('link_ar'),
            'type': request.form.get('type'),
            'parent_id': request.form.get('parent_id'),
            'order': request.form.get('order'),
            'is_visible': request.form.get('is_visible') == 'on',
            'page_type': 'secondary_menu'
        }

        if id:
            # Update existing secondary menu item
            utils.update_secondary_menu(id, data)
            flash('Secondary menu item updated successfully!', 'success')
        else:
            # Create new secondary menu item
            utils.create_secondary_menu(data)
            flash('Secondary menu item created successfully!', 'success')

        return redirect(url_for('header_management.index'))

    # Fetch secondary menu data for editing
    secondary_menu = None
    if id:
        secondary_menu = utils.get_secondary_menu(id)

    return render_template('ckanext_pages/header_management/edit_secondary_menu.html', secondary_menu=secondary_menu)

@header_management.route('/secondary_menu/delete/<id>', methods=['POST'])
def delete_secondary_menu(id):
    """Delete a secondary menu item."""
    try:
        check_access('sysadmin', {})
    except NotAuthorized:
        return render_template('403.html')

    utils.delete_secondary_menu(id)
    flash('Secondary menu item deleted successfully!', 'success')

    return redirect(url_for('header_management.index'))

@header_management.route('/secondary_menu/toggle_visibility/<id>', methods=['POST'])
def toggle_secondary_menu_visibility(id):
    """Toggle visibility of a secondary menu item."""
    try:
        check_access('sysadmin', {})
    except NotAuthorized:
        return render_template('403.html')

    utils.toggle_secondary_menu_visibility(id)
    return redirect(url_for('header_management.index'))


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

