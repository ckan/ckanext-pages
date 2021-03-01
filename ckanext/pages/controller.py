import ckantoolkit

import ckan.plugins as p
import ckan.lib.helpers as helpers

import ckanext.pages.utils as utils

config = ckantoolkit.config

_ = p.toolkit._

class PagesController(p.toolkit.BaseController):
    controller = 'ckanext.pages.controller:PagesController'

    def _template_setup_org(self, id):
        if not id:
            return
        # we need the org for the rest of the page
        context = {'for_view': True}
        try:
            p.toolkit.c.group_dict = p.toolkit.get_action('organization_show')(context, {'id': id})
        except p.toolkit.ObjectNotFound:
            p.toolkit.abort(404, _('Organization not found'))
        except p.toolkit.NotAuthorized:
            p.toolkit.abort(401, _('Unauthorized to read organization %s') % id)

    def org_show(self, id, page=None):
        if page:
            page = page[1:]
        self._template_setup_org(id)

        context = {'for_view': True}
        org_dict = p.toolkit.get_action('organization_show')(context, {'id': id})

        if page is '':
            return self._org_list_pages(id, org_dict)
        _page = p.toolkit.get_action('ckanext_pages_show')(
            data_dict={'org_id': p.toolkit.c.group_dict['id'],
                       'page': page,}
        )
        if _page is None:
            return self._org_list_pages(id, org_dict)
        p.toolkit.c.page = _page

        return p.toolkit.render('ckanext_pages/organization_page.html',
                                {'group_type': 'organization',
                                 'group_dict': org_dict})

    def _org_list_pages(self, id, org_dict=None):
        p.toolkit.c.pages_dict = p.toolkit.get_action('ckanext_pages_list')(
            data_dict={'org_id': p.toolkit.c.group_dict['id']}
        )
        return p.toolkit.render('ckanext_pages/organization_page_list.html',
                                {'group_type': 'organization',
                                 'group_dict': org_dict})


    def org_delete(self, id, page):
        self._template_setup_org(id)
        page = page[1:]
        if 'cancel' in p.toolkit.request.params:
            p.toolkit.redirect_to(controller=self.controller,
                                  action='org_edit',
                                  id=p.toolkit.c.group_dict['name'],
                                  page='/' + page)
        try:
            if p.toolkit.request.method == 'POST':
                action = p.toolkit.get_action('ckanext_org_pages_delete')
                action({}, {'org_id': p.toolkit.c.group_dict['id'],
                       'page': page})
                p.toolkit.redirect_to('organization_pages_index', id=id)
            else:
                p.toolkit.abort(404, _('Page Not Found'))
        except p.toolkit.NotAuthorized:
            p.toolkit.abort(401, _('Unauthorized to delete page'))
        except p.toolkit.ObjectNotFound:
            p.toolkit.abort(404, _('Organization not found'))
        context = {'for_view': True}
        org_dict = p.toolkit.get_action('organization_show')(context, {'id': id})

        return p.toolkit.render('ckanext_pages/confirm_delete.html',
                                {'page': page, 'group_type': 'organization',
                                 'group_dict': org_dict})


    def org_edit(self, id, page=None, data=None, errors=None, error_summary=None):
        self._template_setup_org(id)
        if page:
            page = page[1:]
        _page = p.toolkit.get_action('ckanext_pages_show')(
            data_dict={'org_id': p.toolkit.c.group_dict['id'],
                       'page': page}
        )
        if _page is None:
            _page = {}

        if p.toolkit.request.method == 'POST' and not data:
            data = p.toolkit.request.POST
            items = ['title', 'name', 'content', 'private']
            # update config from form
            for item in items:
                if item in data:
                    _page[item] = data[item]
            _page['org_id'] = p.toolkit.c.group_dict['id']
            _page['page'] = page
            try:
                junk = p.toolkit.get_action('ckanext_org_pages_update')(
                    data_dict=_page
                )
            except p.toolkit.ValidationError as e:
                errors = e.error_dict
                error_summary = e.error_summary
                return self.org_edit(id, '/' + page, data,
                                 errors, error_summary)
            p.toolkit.redirect_to('organization_pages', id=id, page='/' + _page['name'])

        if not data:
            data = _page

        errors = errors or {}
        error_summary = error_summary or {}

        context = {'for_view': True}
        org_dict = p.toolkit.get_action('organization_show')(context, {'id': id})

        vars = {'data': data, 'errors': errors,
                'error_summary': error_summary, 'page': page,
                'group_type': 'organization', 'group_dict': org_dict}

        return p.toolkit.render('ckanext_pages/organization_page_edit.html',
                               extra_vars=vars)

    def _template_setup_group(self, id):
        if not id:
            return
        # we need the org for the rest of the page
        context = {'for_view': True}
        try:
            p.toolkit.c.group_dict = p.toolkit.get_action('group_show')(context, {'id': id})
        except p.toolkit.ObjectNotFound:
            p.toolkit.abort(404, _('Group not found'))
        except p.toolkit.NotAuthorized:
            p.toolkit.abort(401, _('Unauthorized to read group %s') % id)


    def group_show(self, id, page=None):
        if page:
            page = page[1:]
        self._template_setup_group(id)

        context = {'for_view': True}
        group_dict = p.toolkit.get_action('group_show')(context, {'id': id})
        if page is '':
            return self._group_list_pages(id, group_dict)
        _page = p.toolkit.get_action('ckanext_pages_show')(
            data_dict={'org_id': p.toolkit.c.group_dict['id'],
                       'page': page}
        )
        if _page is None:
            return self._group_list_pages(id, group_dict)
        p.toolkit.c.page = _page
        return p.toolkit.render('ckanext_pages/group_page.html',
                                {'group_type': 'group',
                                 'group_dict': group_dict})


    def group_delete(self, id, page):
        self._template_setup_group(id)
        page = page[1:]
        if 'cancel' in p.toolkit.request.params:
            p.toolkit.redirect_to(controller=self.controller,
                                  action='group_edit',
                                  id=p.toolkit.c.group_dict['name'],
                                  page='/' + page)
        try:
            if p.toolkit.request.method == 'POST':
                action = p.toolkit.get_action('ckanext_group_pages_delete')
                action({}, {'org_id': p.toolkit.c.group_dict['id'],
                       'page': page})
                p.toolkit.redirect_to('group_pages_index', id=id)
            else:
                p.toolkit.abort(404, _('Page Not Found'))
        except p.toolkit.NotAuthorized:
            p.toolkit.abort(401, _('Unauthorized to delete page'))
        except p.toolkit.ObjectNotFound:
            p.toolkit.abort(404, _('Group not found'))

        context = {'for_view': True}
        group_dict = p.toolkit.get_action('group_show')(context, {'id': id})

        return p.toolkit.render('ckanext_pages/confirm_delete.html',
                                {'page': page, 'group_type': 'group',
                                 'group_dict': group_dict})


    def _group_list_pages(self, id, group_dict=None):
        p.toolkit.c.pages_dict = p.toolkit.get_action('ckanext_pages_list')(
            data_dict={'org_id': p.toolkit.c.group_dict['id']}
        )
        return p.toolkit.render('ckanext_pages/group_page_list.html',
                                extra_vars={
                                    'group_type': 'group',
                                    'group_dict': group_dict
                                })

    def group_edit(self, id, page=None, data=None, errors=None, error_summary=None):
        self._template_setup_group(id)
        if page:
            page = page[1:]
        _page = p.toolkit.get_action('ckanext_pages_show')(
            data_dict={'org_id': p.toolkit.c.group_dict['id'],
                       'page': page}
        )
        if _page is None:
            _page = {}

        if p.toolkit.request.method == 'POST' and not data:
            data = p.toolkit.request.POST
            items = ['title', 'name', 'content', 'private']
            # update config from form
            for item in items:
                if item in data:
                    _page[item] = data[item]
            _page['org_id'] = p.toolkit.c.group_dict['id']
            _page['page'] = page
            try:
                junk = p.toolkit.get_action('ckanext_group_pages_update')(
                    data_dict=_page
                )
            except p.toolkit.ValidationError as e:
                errors = e.error_dict
                error_summary = e.error_summary
                return self.group_edit(id, '/' + page, data,
                                 errors, error_summary)
            p.toolkit.redirect_to('group_pages', id=id, page='/' + _page['name'])

        if not data:
            data = _page

        errors = errors or {}
        error_summary = error_summary or {}

        context = {'for_view': True}
        group_dict = p.toolkit.get_action('group_show')(context, {'id': id})

        vars = {'data': data, 'errors': errors,
                'error_summary': error_summary, 'page': page,
                'group_type': 'group', 'group_dict': group_dict}

        return p.toolkit.render('ckanext_pages/group_page_edit.html',
                               extra_vars=vars)

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

    def pages_edit(self, page=None, data=None, errors=None, error_summary=None, page_type='pages'):
        return utils.pages_edit(page, data, errors, error_summary, page_type)

    def pages_upload(self):
        return utils.pages_upload()
