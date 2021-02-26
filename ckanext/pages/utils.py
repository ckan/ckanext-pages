import ckantoolkit
import ckan.plugins as p
import ckan.lib.helpers as helpers

config = ckantoolkit.config
_ = ckantoolkit._


def pages_list_pages(page_type):
    data_dict = {'org_id': None, 'page_type': page_type}
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


def pages_edit(page=None, data=None, errors=None, error_summary=None, page_type='pages'):

    page_dict = None
    if page:
        page = page[1:]
        page_dict = p.toolkit.get_action('ckanext_pages_show')(
            data_dict={'org_id': None, 'page': page}
        )
    if page_dict is None:
        page_dict = {}

    if p.toolkit.request.method == 'POST' and not data:
        data = dict(p.toolkit.request.POST)

        page_dict.update(data)

        page_dict['org_id'] = None
        page_dict['page'] = page
        page_dict['page_type'] = 'page' if page_type == 'pages' else page_type

        try:
            p.toolkit.get_action('ckanext_pages_update')(
                data_dict=page_dict
            )
        except p.toolkit.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            p.toolkit.h.flash_error(error_summary)
            return pages_edit(
                '/' + page, data, errors, error_summary, page_type=page_type)
        p.toolkit.redirect_to('%s_show' % page_type, page='/' + page_dict['name'])

    try:
        p.toolkit.check_access('ckanext_pages_update', {'user': p.toolkit.c.user or p.toolkit.c.author})
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, _('Unauthorized to create or edit a page'))

    if not data:
        data = page_dict

    errors = errors or {}
    error_summary = error_summary or {}

    form_snippet = config.get('ckanext.pages.form', 'ckanext_pages/base_form.html')

    vars = {'data': data, 'errors': errors,
            'error_summary': error_summary, 'page': page or '',
            'form_snippet': form_snippet}

    return p.toolkit.render('ckanext_pages/%s_edit.html' % page_type,
                            extra_vars=vars)
