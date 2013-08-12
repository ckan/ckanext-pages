import logging

import ckan.plugins as p

import actions
import auth

log = logging.getLogger(__name__)


class PagesPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IActions, inherit=True)
    p.implements(p.IAuthFunctions, inherit=True)

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'theme/templates')

    def configure(self, config):
        pass

    def get_helpers(self):
        return {
        }

    def after_map(self, map):
        controller = 'ckanext.pages.controller:PagesController'
        map.connect('organization_pages_delete', '/organization/pages_delete/{id}{page:/.*|}',
                    action='org_delete', ckan_icon='delete', controller=controller)
        map.connect('organization_pages_edit', '/organization/pages_edit/{id}{page:/.*|}',
                    action='org_edit', ckan_icon='edit', controller=controller)
        map.connect('organization_pages', '/organization/pages/{id}{page:/.*|}',
                    action='org_show', ckan_icon='file', controller=controller, highlight_actions='org_edit org_show')

        map.connect('group_pages_delete', '/group/pages_delete/{id}{page:/.*|}',
                    action='group_delete', ckan_icon='delete', controller=controller)
        map.connect('group_pages_edit', '/group/pages_edit/{id}{page:/.*|}',
                    action='group_edit', ckan_icon='edit', controller=controller)
        map.connect('group_pages', '/group/pages/{id}{page:/.*|}',
                    action='group_show', ckan_icon='file', controller=controller, highlight_actions='group_edit group_show')



        map.connect('pages_delete', '/pages_delete{page:/.*|}',
                    action='pages_delete', ckan_icon='delete', controller=controller)
        map.connect('pages_edit', '/pages_edit{page:/.*|}',
                    action='pages_edit', ckan_icon='edit', controller=controller)
        map.connect('pages_show', '/pages{page:/.*|}',
                    action='pages_show', ckan_icon='file', controller=controller, highlight_actions='pages_edit pages_show')
        return map

    def get_actions(self):
        return {
            'ckanext_pages_show': actions.pages_show,
            'ckanext_pages_update': actions.pages_update,
            'ckanext_pages_delete': actions.pages_delete,
            'ckanext_pages_list': actions.pages_list,
            'ckanext_org_pages_show': actions.org_pages_show,
            'ckanext_org_pages_update': actions.org_pages_update,
            'ckanext_org_pages_delete': actions.org_pages_delete,
            'ckanext_org_pages_list': actions.org_pages_list,
            'ckanext_group_pages_show': actions.group_pages_show,
            'ckanext_group_pages_update': actions.group_pages_update,
            'ckanext_group_pages_delete': actions.group_pages_delete,
            'ckanext_group_pages_list': actions.group_pages_list,
       }

    def get_auth_functions(self):
        return {
            'ckanext_pages_show': auth.pages_show,
            'ckanext_pages_update': auth.pages_update,
            'ckanext_pages_delete': auth.pages_delete,
            'ckanext_pages_list': auth.pages_list,
            'ckanext_org_pages_show': auth.org_pages_show,
            'ckanext_org_pages_update': auth.org_pages_update,
            'ckanext_org_pages_delete': auth.org_pages_delete,
            'ckanext_org_pages_list': auth.org_pages_list,
            'ckanext_group_pages_show': auth.group_pages_show,
            'ckanext_group_pages_update': auth.group_pages_update,
            'ckanext_group_pages_delete': auth.group_pages_delete,
            'ckanext_group_pages_list': auth.group_pages_list,
       }
