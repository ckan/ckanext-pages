# -*- coding: utf-8 -*-

import ckan.plugins as p


class MixinPlugin(p.SingletonPlugin):

    p.implements(p.IRoutes, inherit=True)

    def after_map(self, map):
        controller = 'ckanext.pages.controller:PagesController'

        if self.organization_pages:
            map.connect('organization_pages_delete', '/organization/pages_delete/{id}{page:/.*|}',
                        action='org_delete', ckan_icon='delete', controller=controller)
            map.connect('organization_pages_edit', '/organization/pages_edit/{id}{page:/.*|}',
                        action='org_edit', ckan_icon='edit', controller=controller)
            map.connect('organization_pages_index', '/organization/pages/{id}',
                        action='org_show', ckan_icon='file', controller=controller,
                        highlight_actions='org_edit org_show', page='')
            map.connect('organization_pages', '/organization/pages/{id}{page:/.*|}',
                        action='org_show', ckan_icon='file', controller=controller,
                        highlight_actions='org_edit org_show')

        if self.group_pages:
            map.connect('group_pages_delete', '/group/pages_delete/{id}{page:/.*|}',
                        action='group_delete', ckan_icon='delete', controller=controller)
            map.connect('group_pages_edit', '/group/pages_edit/{id}{page:/.*|}',
                        action='group_edit', ckan_icon='edit', controller=controller)
            map.connect('group_pages_index', '/group/pages/{id}',
                        action='group_show', ckan_icon='file', controller=controller,
                        highlight_actions='group_edit group_show', page='')
            map.connect('group_pages', '/group/pages/{id}{page:/.*|}',
                        action='group_show', ckan_icon='file', controller=controller,
                        highlight_actions='group_edit group_show')

        map.connect('pages_delete', '/pages_delete{page:/.*|}',
                    action='pages_delete', ckan_icon='delete', controller=controller)
        map.connect('pages_edit', '/pages_edit{page:/.*|}',
                    action='pages_edit', ckan_icon='edit', controller=controller)
        map.connect('pages_index', '/pages',
                    action='pages_index', ckan_icon='file', controller=controller,
                    highlight_actions='pages_edit pages_index pages_show')
        map.connect('pages_show', '/pages{page:/.*|}',
                    action='pages_show', ckan_icon='file', controller=controller,
                    highlight_actions='pages_edit pages_index pages_show')
        map.connect('pages_upload', '/pages_upload',
                    action='pages_upload', controller=controller)

        map.connect('blog_delete', '/blog_delete{page:/.*|}',
                    action='blog_delete', ckan_icon='delete', controller=controller)
        map.connect('blog_edit', '/blog_edit{page:/.*|}',
                    action='blog_edit', ckan_icon='edit', controller=controller)
        map.connect('blog_index', '/blog',
                    action='blog_index', ckan_icon='file', controller=controller,
                    highlight_actions='blog_edit blog_index blog_show')
        map.connect('blog_show', '/blog{page:/.*|}',
                    action='blog_show', ckan_icon='file', controller=controller,
                    highlight_actions='blog_edit blog_index blog_show')
        return map
