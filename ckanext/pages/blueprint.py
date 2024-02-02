import ckanext.pages.utils as utils
from ckan import model
from ckanext.pages.db import MainPage
from ckanext.pages.db import Page
from flask import Blueprint, render_template, request, redirect, url_for
from flask import g
from flask import jsonify
from ckan.plugins import toolkit as tk
import ckan.lib.helpers as h

pages = Blueprint('pages', __name__)
header_management = Blueprint('header_management', __name__, url_prefix='/header-management')


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


def _get_context():
    return {
        'user': tk.g.user,
        'auth_user_obj': tk.g.userobj,
    }


@header_management.route('/', methods=['GET'])
def index():
    context = _get_context()

    try:
        tk.check_access('ckanext_header_management_access', context)

        menu_type = tk.request.args.get('menu_type')

        main_menu = tk.get_action('ckanext_header_main_menu_list')(
            context, {'menu_type': menu_type}
        )
        secondary_menu = tk.get_action('ckanext_header_secondary_menu_list')(
            context, {}
        )
        logo = tk.get_action('ckanext_header_logo_get')(context, {})

        extra_vars = {
            'main_menu': main_menu,
            'secondary_menu': secondary_menu,
            'logo': logo,
            'menu_type': menu_type
        }

        return tk.render('ckanext_pages/header_management/index.html', extra_vars)
    except tk.NotAuthorized:
        tk.abort(403, tk._('Not authorized to manage headers'))


@header_management.route('/main-menu/toggle-visibility/<id>', methods=['POST'])
def toggle_main_menu_visibility(id):
    context = _get_context()

    try:
        tk.get_action('ckanext_header_main_menu_toggle_visibility')(
            context, {'id': id}
        )
        h.flash_success(tk._('Menu item visibility updated'))
    except tk.NotAuthorized:
        h.flash_error(tk._('Not authorized to update menu items'))
    except tk.ObjectNotFound:
        h.flash_error(tk._('Menu item not found'))

    return h.redirect_to('header_management.index')


@header_management.route('/main-menu/delete/<id>', methods=['POST'])
def delete_main_menu(id):
    context = _get_context()

    try:
        tk.get_action('ckanext_header_main_menu_delete')(
            context, {'id': id}
        )
        h.flash_success(tk._('Menu item deleted'))
    except tk.NotAuthorized:
        h.flash_error(tk._('Not authorized to delete menu items'))
    except tk.ObjectNotFound:
        h.flash_error(tk._('Menu item not found'))
    except tk.ValidationError as e:
        h.flash_error(e.error_dict['id'])

    return h.redirect_to('header_management.index')


@header_management.route('/secondary-menu/toggle-visibility/<id>', methods=['POST'])
def toggle_secondary_menu_visibility(id):
    context = _get_context()

    try:
        tk.get_action('ckanext_header_secondary_menu_toggle_visibility')(
            context, {'id': id}
        )
        h.flash_success(tk._('Menu item visibility updated'))
    except tk.NotAuthorized:
        h.flash_error(tk._('Not authorized to update menu items'))
    except tk.ObjectNotFound:
        h.flash_error(tk._('Menu item not found'))

    return h.redirect_to('header_management.index')


@header_management.route('/logo/delete/<id>', methods=['POST'])
def delete_logo(id):
    context = _get_context()

    try:
        tk.get_action('ckanext_header_logo_delete')(
            context, {'id': id}
        )
        h.flash_success(tk._('Logo deleted'))
    except tk.NotAuthorized:
        h.flash_error(tk._('Not authorized to delete logo'))
    except tk.ObjectNotFound:
        h.flash_error(tk._('Menu item not found'))

    return h.redirect_to('header_management.index')


@header_management.route('/logo/toggle-visibility/<id>', methods=['POST'])
def toggle_logo_visibility(id):
    context = _get_context()

    try:
        tk.get_action('ckanext_header_logo_toggle_visibility')(
            context, {'id': id}
        )
        h.flash_success(tk._('Logo visibility updated'))
    except tk.NotAuthorized:
        h.flash_error(tk._('Not authorized to update logo'))
    except tk.ObjectNotFound:
        h.flash_error(tk._('Logo not found'))

    return h.redirect_to('header_management.index')


@header_management.route('/logo/edit/<id>', methods=['GET', 'POST'])
def edit_logo(id):
    context = _get_context()

    try:
        tk.check_access('ckanext_header_management_access', context)

        if tk.request.method == 'POST':
            data_dict = dict(tk.request.form)
            data_dict.update(tk.request.files.to_dict())
            data_dict['id'] = id

            try:
                tk.get_action('ckanext_header_logo_update')(context, data_dict)
                h.flash_success(tk._('Logo updated successfully'))
                return h.redirect_to('header_management.index')
            except tk.ValidationError as e:
                errors = e.error_dict
                error_summary = e.error_summary

                return tk.render(
                    'ckanext_pages/header_management/edit_header_logo.html',
                    extra_vars={
                        'data': data_dict,
                        'errors': errors,
                        'error_summary': error_summary
                    }
                )

        logo = tk.get_action('ckanext_header_logo_get')(context, {'id': id})
        return tk.render(
            'ckanext_pages/header_management/edit_header_logo.html',
            extra_vars={
                'data': logo,
                'errors': {},
                'error_summary': {}
            }
        )

    except tk.NotAuthorized:
        tk.abort(403, tk._('Not authorized to edit logo'))


@header_management.route('/main-menu/new', methods=['GET', 'POST'])
def new_main_menu():
    context = _get_context()

    try:
        tk.check_access('ckanext_header_management_access', context)

        if tk.request.method == 'POST':
            data_dict = dict(tk.request.form)
            data_dict.update(tk.request.files.to_dict())

            try:
                tk.get_action('ckanext_header_main_menu_create')(context, data_dict)
                h.flash_success(tk._('Menu item created successfully'))
                return h.redirect_to('header_management.index')
            except tk.ValidationError as e:
                h.flash_error(e.error_summary)

        return tk.render('header_management/edit_header_main_menu.html')

    except tk.NotAuthorized:
        tk.abort(403, tk._('Not authorized to create menu items'))


@header_management.route('/main-menu/new', methods=['GET', 'POST'])
def new_secondary_menu():
    context = _get_context()

    try:
        tk.check_access('ckanext_header_management_access', context)

        if tk.request.method == 'POST':
            data_dict = dict(tk.request.form)
            data_dict.update(tk.request.files.to_dict())

            try:
                tk.get_action('ckanext_header_secondary_menu_create')(context, data_dict)
                h.flash_success(tk._('Menu item created successfully'))
                return h.redirect_to('header_management.index')
            except tk.ValidationError as e:
                h.flash_error(e.error_summary)

        return tk.render('header_management/edit_header_secondary_menu.html')

    except tk.NotAuthorized:
        tk.abort(403, tk._('Not authorized to create menu items'))


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
pages.add_url_rule("/news_toggle_visibility/<news_id>", view_func=news_toggle_visibility,
                   endpoint='news_toggle_visibility', methods=['POST'])

pages.add_url_rule("/main_page/edit/<section_id>", view_func=main_page_edit, endpoint="main_page_edit",
                   methods=['GET', 'POST'])

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
pages.add_url_rule("/pages_toggle_visibility/<page>", view_func=pages_toggle_visibility, endpoint='toggle_visibility',
                   methods=['POST'])

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
pages.add_url_rule("/organization/pages_edit/<id>", view_func=org_edit, endpoint='organization_pages_new',
                   methods=['GET', 'POST'])
pages.add_url_rule("/organization/pages_edit/<id>/", view_func=org_edit, endpoint='organization_pages_new',
                   methods=['GET', 'POST'])
pages.add_url_rule("/organization/pages_edit/<id>/<page>", view_func=org_edit, endpoint='organization_pages_edit',
                   methods=['GET', 'POST'])

# Organization Page Deletion
pages.add_url_rule("/organization/pages_delete/<id>/<page>", view_func=org_delete, endpoint='organization_pages_delete',
                   methods=['GET', 'POST'])

# Group Pages
pages.add_url_rule("/group/pages/<id>", view_func=group_show, endpoint='group_pages_index')
pages.add_url_rule("/group/pages/<id>/<page>", view_func=group_show, endpoint='group_pages_show')

# Group Page Editing
pages.add_url_rule("/group/pages_edit/<id>", view_func=group_edit, endpoint='group_pages_new', methods=['GET', 'POST'])
pages.add_url_rule("/group/pages_edit/<id>/", view_func=group_edit, endpoint='group_pages_new', methods=['GET', 'POST'])
pages.add_url_rule("/group/pages_edit/<id>/<page>", view_func=group_edit, endpoint='group_pages_edit',
                   methods=['GET', 'POST'])

# Group Page Deletion
pages.add_url_rule("/group/pages_delete/<id>/<page>", view_func=group_delete, endpoint='group_pages_delete',
                   methods=['GET', 'POST'])


# blueprints

def get_blueprints():
    return [pages, header_management]
