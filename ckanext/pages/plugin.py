import logging
from html import escape as html_escape
from six.moves.urllib.parse import quote
from ckan.plugins import toolkit as tk
import ckan.plugins as p
from ckan.lib.helpers import build_nav_main as core_build_nav_main
from ckanext.pages import actions
from ckanext.pages import auth
from ckanext.pages import blueprint
from ckan.lib.plugins import DefaultTranslation
from ckan.plugins import SingletonPlugin, implements, IConfigurer
from ckanext.pages import cli
from ckanext.pages.db import MainPage


log = logging.getLogger(__name__)

# Helper function to fetch sections dynamically
def get_main_page_sections(lang='en'):
    sections = MainPage.all()
    section_data = []
    for section in sections:
        section_data.append({
            'id': section.id,
            'title_1': section.main_title_1_ar if lang == 'ar' else section.main_title_1_en,
            'title_2': section.main_title_2_ar if lang == 'ar' else section.main_title_2_en,
            'brief': section.main_brief_ar if lang == 'ar' else section.main_brief_en
        })
    return section_data



# Navigation customization
def build_pages_nav_main(*args):
    about_menu = tk.asbool(tk.config.get('ckanext.pages.about_menu', True))
    group_menu = tk.asbool(tk.config.get('ckanext.pages.group_menu', True))
    org_menu = tk.asbool(tk.config.get('ckanext.pages.organization_menu', True))
    new_args = []
    for arg in args:
        if arg[0] in 'home.about' and not about_menu:
            continue
        if arg[0] in 'home.group_index' and not org_menu:
            continue
        if arg[0] in 'home.organizations_index' and not group_menu:
            continue
        new_args.append(arg)
    output = core_build_nav_main(*new_args)

    pages_list = tk.get_action('ckanext_pages_list')(None, {'order': True, 'private': False})
    page_name = ''
    is_current_page = tk.get_endpoint() in (('pages', 'show'), ('pages', 'blog_show'))
    if is_current_page:
        page_name = tk.request.path.split('/')[-1]
    for page in pages_list:
        type_ = 'blog' if page['page_type'] == 'blog' else 'pages'
        name = quote(page['name'])
        title = html_escape(page['title'])
        link = tk.h.literal(u'<a href="/{}/{}">{}</a>'.format(type_, name, title))
        if page['name'] == page_name:
            li = tk.literal('<li class="active">') + link + tk.literal('</li>')
        else:
            li = tk.literal('<li>') + link + tk.literal('</li>')
        output = output + li
    return output

# Render HTML content
def render_content(content):
    allow_html = tk.asbool(tk.config.get('ckanext.pages.allow_html', False))
    return tk.h.render_markdown(content, allow_html=allow_html)

# WYSIWYG editor helper
def get_wysiwyg_editor():
    return tk.config.get('ckanext.pages.editor', '')

# Get recent blog posts
def get_recent_blog_posts(number=5, exclude=None):
    blog_list = tk.get_action('ckanext_pages_list')(
        None, {'order_publish_date': True, 'private': False,
               'page_type': 'blog'}
    )
    new_list = []
    for blog in blog_list:
        if exclude and blog['name'] == exclude:
            continue
        new_list.append(blog)
        if len(new_list) == number:
            break
    return new_list

# CKAN Plugin configuration
class PagesPluginBase(p.SingletonPlugin, DefaultTranslation):
    p.implements(p.ITranslation, inherit=True)

class PagesPlugin(PagesPluginBase):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IActions, inherit=True)
    p.implements(p.IAuthFunctions, inherit=True)
    p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IBlueprint)

    def get_blueprint(self):
        return [blueprint.pages, blueprint.header_management]

    def update_config(self, config):
        self.organization_pages = tk.asbool(config.get('ckanext.pages.organization', False))
        self.group_pages = tk.asbool(config.get('ckanext.pages.group', False))
        tk.add_template_directory(config, 'theme/templates_main')
        if self.group_pages:
            tk.add_template_directory(config, 'theme/templates_group')
        if self.organization_pages:
            tk.add_template_directory(config, 'theme/templates_organization')
        tk.add_resource('assets', 'pages')
        tk.add_public_directory(config, 'assets/')
        tk.add_public_directory(config, 'assets/vendor/ckeditor/')

    def get_actions(self):
        actions_dict = {
            'ckanext_pages_show': actions.pages_show,
            'ckanext_pages_update': actions.pages_update,
            'ckanext_pages_delete': actions.pages_delete,
            'ckanext_pages_list': actions.pages_list,
            'ckanext_pages_upload': actions.pages_upload,
            'ckanext_main_page_show': actions.main_page_show,
            'ckanext_event_edit':actions.event_edit,
            'ckanext_news_edit':actions.news_edit,
            # Header Management Actions
            'ckanext_header_main_menu_create': actions.header_main_menu_create,
            'ckanext_header_secondary_menu_create': actions.header_secondary_menu_create,
            'ckanext_header_main_menu_list': actions.header_main_menu_list,
            'ckanext_header_main_menu_parent_list': actions.header_main_menu_parent_list,
            'ckanext_header_secondary_menu_parent_list': actions.header_secondary_menu_parent_list,
            'ckanext_header_secondary_menu_list': actions.header_secondary_menu_list,
            'ckanext_header_logo_get': actions.header_logo_get,
            'ckanext_header_main_menu_show': actions.header_main_menu_show,
            'ckanext_header_main_menu_toggle_visibility': actions.header_main_menu_toggle_visibility,
            'ckanext_header_main_menu_delete': actions.header_main_menu_delete,
            'ckanext_header_main_menu_edit': actions.header_main_menu_edit,
            'ckanext_header_secondary_menu_toggle_visibility': actions.header_secondary_menu_toggle_visibility,
            'ckanext_header_logo_update': actions.header_logo_update,
            'ckanext_header_logo_delete': actions.header_logo_delete,
            'ckanext_header_logo_toggle_visibility': actions.header_logo_toggle_visibility,
            'ckanext_header_secondary_menu_show': actions.header_secondary_menu_show,
            'ckanext_header_secondary_menu_edit': actions.header_secondary_menu_edit,
            'ckanext_header_secondary_menu_delete': actions.header_secondary_menu_delete
        }
        return actions_dict

    def get_auth_functions(self):
        return {
            'ckanext_pages_show': auth.pages_show,
            'ckanext_pages_update': auth.pages_update,
            'ckanext_pages_delete': auth.pages_delete,
            'ckanext_pages_list': auth.pages_list,
            'ckanext_pages_upload': auth.pages_upload,
            # Header Management Auth Functions
            'ckanext_header_management_access': auth.header_management_access
        }
