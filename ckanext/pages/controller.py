import ckan.plugins as p
import ckan.lib.helpers as helpers
from pylons import config
import ckan.lib.helpers as h

_ = p.toolkit._

class PagesController(p.toolkit.BaseController):
    controller = 'ckanext.pages.controller:PagesController'

    def _get_group_dict(self, id):
        ''' returns the result of group_show action or aborts if there is a
        problem '''

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
        if page is '':
            return self._org_list_pages(id)
        _page = p.toolkit.get_action('ckanext_pages_show')(
            data_dict={'org_id': p.toolkit.c.group_dict['id'],
                       'page': page,}
        )
        if _page is None:
            return self._org_list_pages(id)
        p.toolkit.c.page = _page
        return p.toolkit.render('ckanext_pages/organization_page.html')

    def _org_list_pages(self, id):
        p.toolkit.c.pages_dict = p.toolkit.get_action('ckanext_pages_list')(
            data_dict={'org_id': p.toolkit.c.group_dict['id']}
        )
        return p.toolkit.render('ckanext_pages/organization_page_list.html')


    def org_delete(self, id, page):
        self._template_setup_org(id)
        page = page[1:]
        if 'cancel' in p.toolkit.request.params:
            p.toolkit.redirect_to(controller=self.controller, action='org_edit', id=p.toolkit.c.group_dict['name'], page='/' + page)

  ##      try:
  ##          self._check_access('group_delete', {}, {'id': id})
  ##      except p.toolkit.NotAuthorized:
  ##          p.toolkit.abort(401, _('Unauthorized to delete page'))

        try:
            if p.toolkit.request.method == 'POST':
                p.toolkit.get_action('ckanext_pages_delete')({}, {'org_id': p.toolkit.c.group_dict['id'], 'page': page})
                p.toolkit.redirect_to('organization_pages_index', id=id)
            else:
                p.toolkit.abort(404, _('Page Not Found'))
        except p.toolkit.NotAuthorized:
            p.toolkit.abort(401, _('Unauthorized to delete page'))
        except p.toolkit.ObjectNotFound:
            p.toolkit.abort(404, _('Group not found'))
        return p.toolkit.render('ckanext_pages/confirm_delete.html', {'page': page})


    def org_edit(self, id, page=None, data=None, errors=None, error_summary=None):
        self._template_setup_org(id)
        if page:
            page = page[1:]
        _page = p.toolkit.get_action('ckanext_pages_show')(
            data_dict={'org_id': p.toolkit.c.group_dict['id'],
                       'page': page,}
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
            _page['org_id'] = p.toolkit.c.group_dict['id'],
            _page['page'] = page
            try:
                junk = p.toolkit.get_action('ckanext_pages_update')(
                    data_dict=_page
                )
            except p.toolkit.ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary
                return self.org_edit(id, '/' + page, data,
                                 errors, error_summary)
            p.toolkit.redirect_to('organization_pages', id=id, page='/' + _page['name'])

        if not data:
            data = _page

        errors = errors or {}
        error_summary = error_summary or {}

        vars = {'data': data, 'errors': errors,
                'error_summary': error_summary, 'page': page}

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
        if page is '':
            return self._group_list_pages(id)
        _page = p.toolkit.get_action('ckanext_pages_show')(
            data_dict={'org_id': p.toolkit.c.group_dict['id'],
                       'page': page,}
        )
        if _page is None:
            return self._group_list_pages(id)
        p.toolkit.c.page = _page
        return p.toolkit.render('ckanext_pages/group_page.html')

    def _group_list_pages(self, id):
        p.toolkit.c.pages_dict = p.toolkit.get_action('ckanext_pages_list')(
            data_dict={'org_id': p.toolkit.c.group_dict['id']}
        )
        return p.toolkit.render('ckanext_pages/group_page_list.html')

    def group_edit(self, id, page=None, data=None, errors=None, error_summary=None):
        self._template_setup_group(id)
        if page:
            page = page[1:]
        _page = p.toolkit.get_action('ckanext_pages_show')(
            data_dict={'org_id': p.toolkit.c.group_dict['id'],
                       'page': page,}
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
                junk = p.toolkit.get_action('ckanext_pages_update')(
                    data_dict=_page
                )
            except p.toolkit.ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary
                return self.group_edit(id, '/' + page, data,
                                 errors, error_summary)
            p.toolkit.redirect_to('group_pages', id=id, page='/' + _page['name'])

        if not data:
            data = _page

        errors = errors or {}
        error_summary = error_summary or {}

        vars = {'data': data, 'errors': errors,
                'error_summary': error_summary, 'page': page}

        return p.toolkit.render('ckanext_pages/group_page_edit.html',
                               extra_vars=vars)

    def blog_index(self):
        return self._pages_list_pages('blog')

    def blog_show(self, page=None):
        return self.pages_show(page, page_type='blog')

    def _inject_views_into_page(self, _page):
        # this is a good proxy to a version of CKAN with views enabled.
        if not p.plugin_loaded('image_view'):
            return
        try:
            import lxml
            import lxml.html
        except ImportError:
            return

        try:
            root = lxml.html.fromstring(_page['content'])
        # Return if any errors are found while parsing the content
        except (lxml.etree.XMLSyntaxError,
                lxml.etree.ParserError):
            return

        for element in root.findall('.//iframe'):
            embed_element = element.attrib.pop('data-ckan-view-embed', None)
            if not embed_element:
                continue
            element.tag = 'div'
            error = None

            try:
                iframe_src = element.attrib.pop('src', '')
                width = element.attrib.pop('width', '80')
                if not width.endswith('%') and not width.endswith('px'):
                    width = width + 'px'
                height = element.attrib.pop('height', '80')
                if not height.endswith('%') and not height.endswith('px'):
                    height = height + 'px'
                align = element.attrib.pop('align', 'none')
                style = "width: %s; height: %s; float: %s; overflow: auto; vertical-align:middle; position:relative" % (width, height, align)
                element.attrib['style'] = style
                element.attrib['class'] = 'pages-embed'
                view = p.toolkit.get_action('resource_view_show')({}, {'id': iframe_src[-36:]})
                context = {}
                resource = p.toolkit.get_action('resource_show')(context, {'id': view['resource_id']})
                package_id = context['resource'].resource_group.package_id
                package = p.toolkit.get_action('package_show')(context, {'id': package_id})
            except p.toolkit.ObjectNotFound:
                error = _('ERROR: View not found {view_id}'.format(view_id=iframe_src ))

            if error:
                resource_view_html = '<h4> %s </h4>' % error
            elif not helpers.resource_view_is_iframed(view):
                resource_view_html = helpers.rendered_resource_view(view, resource, package)
            else:
                src = helpers.url_for(qualified=True, controller='package', action='resource_view', id=package['name'], resource_id=resource['id'], view_id=view['id'])
                message = _('Your browser does not support iframes.')
                resource_view_html = '<iframe src="{src}" frameborder="0" width="100%" height="100%" style="display:block"> <p>{message}</p> </iframe>'.format(src=src, message=message)

            view_element = lxml.html.fromstring(resource_view_html)
            element.append(view_element)

        _page['content'] = lxml.html.tostring(root)



    def pages_show(self, page=None, page_type='page'):
        p.toolkit.c.page_type = page_type
        if page:
            page = page[1:]
        if not page:
            return self._pages_list_pages(page_type)
        _page = p.toolkit.get_action('ckanext_pages_show')(
            data_dict={'org_id': None,
                       'page': page}
        )
        if _page is None:
            return self._pages_list_pages(page_type)
        p.toolkit.c.page = _page
        self._inject_views_into_page(_page)

        return p.toolkit.render('ckanext_pages/%s.html' % page_type)

    def pages_index(self):
        return self._pages_list_pages('page')

    def _pages_list_pages(self, page_type):
        lang = h.lang()
        data_dict={'org_id': None, 'page_type': page_type}
        if lang != "en":
            data_dict["lang"] = lang
        if page_type == 'blog':
            data_dict['order_publish_date'] = True
        p.toolkit.c.pages_dict = p.toolkit.get_action('ckanext_pages_list')(
            data_dict=data_dict
        )
        p.toolkit.c.page = helpers.Page(
            collection=p.toolkit.c.pages_dict,
            page=p.toolkit.request.params.get('page', 1),
            url=helpers.pager_url,
            items_per_page=21
        )

        if page_type == 'blog':
            return p.toolkit.render('ckanext_pages/blog_list.html')
        return p.toolkit.render('ckanext_pages/pages_list.html')

    def blog_delete(self, page):
        return self.pages_delete(page, page_type='blog')

    def pages_delete(self, page, page_type='pages'):
        page = page[1:]
        if 'cancel' in p.toolkit.request.params:
            p.toolkit.redirect_to(controller=self.controller, action='%s_edit' % page_type, page='/' + page)

        try:
            if p.toolkit.request.method == 'POST':
                p.toolkit.get_action('ckanext_pages_delete')({}, {'page': page})
                p.toolkit.redirect_to('%s_index' % page_type)
            else:
                p.toolkit.abort(404, _('Page Not Found'))
        except p.toolkit.NotAuthorized:
            p.toolkit.abort(401, _('Unauthorized to delete page'))
        except p.toolkit.ObjectNotFound:
            p.toolkit.abort(404, _('Group not found'))
        return p.toolkit.render('ckanext_pages/confirm_delete.html', {'page': page})


    def blog_edit(self, page=None, data=None, errors=None, error_summary=None):
        return self.pages_edit(page=page, data=data, errors=errors, error_summary=error_summary, page_type='blog')

    def pages_edit(self, page=None, data=None, errors=None, error_summary=None, page_type='pages'):
        if page:
            page = page[1:]
        _page = p.toolkit.get_action('ckanext_pages_show')(
            data_dict={'org_id': None,
                       'page': page,}
        )
        if _page is None:
            _page = {}

        if p.toolkit.request.method == 'POST' and not data:
            data = dict(p.toolkit.request.POST)

            _page.update(data)

            _page['org_id'] = None
            _page['page'] = page
            _page['page_type'] = 'page' if page_type == 'pages' else page_type

            try:
                junk = p.toolkit.get_action('ckanext_pages_update')(
                    data_dict=_page
                )
            except p.toolkit.ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary
                return self.pages_edit('/' + page, data,
                                       errors, error_summary, page_type=page_type)
            p.toolkit.redirect_to('%s_show' % page_type, page='/' + _page['name'])

        try:
            p.toolkit.check_access('ckanext_pages_update', {'user': p.toolkit.c.user or p.toolkit.c.author})
        except p.toolkit.NotAuthorized:
            p.toolkit.abort(401, _('Unauthorized to create or edit a page'))

        if not data:
            data = _page

        errors = errors or {}
        error_summary = error_summary or {}

        form_snippet = config.get('ckanext.pages.form', 'ckanext_pages/base_form.html')

        vars = {'data': data, 'errors': errors,
                'error_summary': error_summary, 'page': page,
                'form_snippet': form_snippet}

        return p.toolkit.render('ckanext_pages/%s_edit.html' % page_type,
                                extra_vars=vars)

    def pages_upload(self):
        if not p.toolkit.request.method == 'POST':
            p.toolkit.abort(409, _('Only Posting is availiable'))

        try:
            url = p.toolkit.get_action('ckanext_pages_upload')(None, dict(p.toolkit.request.POST))
        except p.toolkit.NotAuthorized:
            p.toolkit.abort(401, _('Unauthorized to upload file %s') % id)

        return """<script type='text/javascript'>
                      window.parent.CKEDITOR.tools.callFunction(%s, '%s');
                  </script>""" % (p.toolkit.request.GET['CKEditorFuncNum'], url['url'])
