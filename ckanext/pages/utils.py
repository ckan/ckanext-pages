import six
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckan.logic as logic
import ckan.lib.helpers as helpers
import ckan.model as model
from ckanext.pages.db import MainPage,Page , News, Event, HeaderMainMenu, HeaderLogo, HeaderSecondaryMenu
from ckanext.pages.logic.schema import main_page_schema, update_pages_schema
import ckan.lib.navl.dictization_functions as df
from flask import request, flash

config = tk.config
_ = tk._


def _parse_form_data(request):
    return logic.clean_dict(
        dict_fns.unflatten(
            logic.tuplize_dict(
                logic.parse_params(request.form)
            )
        )
    )


def pages_list_pages(page_type):
    data_dict = {'org_id': None, 'page_type': page_type,
                 'sort': request.args.get('sort', 'title_en asc')
                 }
    if page_type == 'blog':
        data_dict['order_publish_date'] = True
    tk.g.pages_dict = tk.get_action('ckanext_pages_list')(
        context={}, data_dict=data_dict
    )

    tk.g.page = helpers.Page(
        collection=tk.g.pages_dict,
        page=tk.request.args.get('page', 1),
        url=helpers.pager_url,
        items_per_page=21
    )
    
    print("DEBUG: Pages dict passed to template:", tk.g.pages_dict)  # Debug

    return tk.render('ckanext_pages/pages_list.html', extra_vars={"pages": tk.g.pages_dict})

def news_list():
    data_dict = {
        'org_id': None,
        'sort': request.args.get('sort', 'title_en asc')  # Default sorting
    }

    # Fetch news items
    news_list = tk.get_action('ckanext_news_list')(
        context={}, data_dict=data_dict
    )

    print(f"DEBUG: News items sent to template: {news_list}")
    # Paginate results
    tk.g.page = helpers.Page(
        collection=news_list,
        page=tk.request.args.get('page', 1),
        url=helpers.pager_url,
        items_per_page=21
    )


    return tk.render('ckanext_pages/news.html', extra_vars={"pages": news_list})

def news_toggle_visibility(news_id):
    data_dict = {'news_id': news_id}
    return tk.get_action('ckanext_news_toggle_visibility')({}, data_dict)  #

def events_list():

    data_dict = {
        'org_id': None,
        'sort': request.args.get('sort', 'title_en asc')  # Default to 'title_en asc'
    }

    events_list = tk.get_action('ckanext_events_list')(
        context={}, data_dict=data_dict
    )

    tk.g.page = helpers.Page(
        collection=events_list,
        page=tk.request.args.get('page', 1),
        url=helpers.pager_url,
        items_per_page=21
    )

    return tk.render('ckanext_pages/events.html', extra_vars={"pages": events_list})


class HeaderLogoUtils:
    @classmethod
    def get_all(cls):
        return HeaderLogo.get_all()

    @classmethod
    def create(cls, data):
        logo = HeaderLogo(**data)
        logo.save()
        return logo

    @classmethod
    def update(cls, logo_id, data):
        logo = HeaderLogo.get(logo_id)
        for key, value in data.items():
            setattr(logo, key, value)
        logo.save()
        return logo

    @classmethod
    def delete(cls, logo_id):
        logo = HeaderLogo.get(logo_id)
        if logo:
            logo.delete()
        return logo

    @classmethod
    def toggle_visibility(cls, logo_id):
        logo = HeaderLogo.get(logo_id)
        if logo:
            logo.is_visible = not logo.is_visible
            logo.save()
        return logo

class HeaderMainMenuUtils:
    @classmethod
    def get_all(cls):
        return HeaderMainMenu.get_all()

    @classmethod
    def get_top_level(cls):
        return HeaderMainMenu.get_top_level()

    @classmethod
    def create(cls, data):
        menu = HeaderMainMenu(**data)
        menu.save()
        return menu

    @classmethod
    def update(cls, menu_id, data):
        menu = HeaderMainMenu.get(menu_id)
        for key, value in data.items():
            setattr(menu, key, value)
        menu.save()
        return menu

    @classmethod
    def delete(cls, menu_id):
        menu = HeaderMainMenu.get(menu_id)
        if menu:
            menu.delete()
        return menu

    @classmethod
    def toggle_visibility(cls, menu_id):
        menu = HeaderMainMenu.get(menu_id)
        if menu:
            menu.is_visible = not menu.is_visible
            menu.save()
        return menu

class HeaderSecondaryMenuUtils:
    @classmethod
    def get_all(cls):
        return HeaderSecondaryMenu.get_all()

    @classmethod
    def create(cls, data):
        menu = HeaderSecondaryMenu(**data)
        menu.save()
        return menu

    @classmethod
    def update(cls, menu_id, data):
        menu = HeaderSecondaryMenu.get(menu_id)
        for key, value in data.items():
            setattr(menu, key, value)
        menu.save()
        return menu

    @classmethod
    def delete(cls, menu_id):
        menu = HeaderSecondaryMenu.get(menu_id)
        if menu:
            menu.delete()
        return menu

    @classmethod
    def toggle_visibility(cls, menu_id):
        menu = HeaderSecondaryMenu.get(menu_id)
        if menu:
            menu.is_visible = not menu.is_visible
            menu.save()
        return menu

class Form:
    # Input field method
    def input(self, name, **kwargs):
        value = kwargs.get('value', '')
        label = kwargs.get('label', '')
        error = kwargs.get('error', '')
        css_class = ' '.join(kwargs.get('classes', []))
        return f'''
            <div class="mb-3">
                <label for="{name}" class="form-label">{label}</label>
                <input type="text" id="{name}" name="{name}" value="{value}" class="{css_class}">
                <div class="text-danger">{error}</div>
            </div>
        '''

    # Checkbox method
    def checkbox(self, name, **kwargs):
        checked = 'checked' if kwargs.get('checked') else ''
        label = kwargs.get('label', '')
        error = kwargs.get('error', '')
        return f'''
            <div class="mb-3 form-check">
                <input type="checkbox" id="{name}" name="{name}" {checked} class="form-check-input">
                <label for="{name}" class="form-check-label">{label}</label>
                <div class="text-danger">{error}</div>
            </div>
        '''

    # Textarea method
    def textarea(self, name, **kwargs):
        value = kwargs.get('value', '')
        label = kwargs.get('label', '')
        error = kwargs.get('error', '')
        css_class = ' '.join(kwargs.get('classes', []))
        return f'''
            <div class="mb-3">
                <label for="{name}" class="form-label">{label}</label>
                <textarea id="{name}" name="{name}" class="{css_class}">{value}</textarea>
                <div class="text-danger">{error}</div>
            </div>
        '''




def validate_page_data(data):

    schema = update_pages_schema()
    return df.validate(data, schema)

def news_edit(page=None, data=None, errors=None, error_summary=None):
    if request.method == 'POST':
        form_data = _parse_form_data(request)
        try:
            # Generate a slug for the 'name' field if it's missing
            if not form_data.get('name'):
                form_data['name'] = form_data.get('title_en', '').strip().lower().replace(' ', '-')[:50]

            # Check if this is an update or a new entry
            news_id = form_data.get('id')  # Retrieve the id from the form data
            if news_id:
                # Update the existing news
                existing_news = model.Session.query(News).get(news_id)
                if not existing_news:
                    raise tk.ObjectNotFound(_("News not found"))
                for key, value in form_data.items():
                    setattr(existing_news, key, value)
                model.Session.commit()
            else:
                # Create a new news entry
                new_news = News(**form_data)
                model.Session.add(new_news)
                model.Session.commit()
                news_id = new_news.id  # Retrieve the newly created ID

            # Redirect back to the news edit page
            return tk.redirect_to('pages.news_index')
        except tk.ValidationError as e:
            model.Session.rollback()
            return tk.render(
                'ckanext_pages/news_edit.html',
                extra_vars={
                    'data': form_data,
                    'errors': e.error_dict,
                    'error_summary': e.error_summary,
                },
            )
    else:
        news_data = model.Session.query(News).get(page) if page else News()

        if news_data.content_en is None:
            news_data.content_en = ""
        if news_data.content_ar is None:
            news_data.content_ar = ""

        return tk.render(
            'ckanext_pages/news_edit.html',
            extra_vars={
                'data': news_data,
                'errors': errors or {},
                'error_summary': error_summary or {},
            },
        )




def events_edit(page=None, data=None, errors=None, error_summary=None):
    if request.method == 'POST':
        form_data =_parse_form_data(request)
        print(form_data)
        try:
            result = tk.get_action("ckanext_event_edit")({}, form_data)
            page_id = result.get("id")
            if not page_id:
                raise ValueError("Page ID is missing for redirect")
            return tk.redirect_to("pages.events_edit", page=page_id)

        except tk.ValidationError as e:
            return tk.render(
                "ckanext_pages/page_edit.html",
                extra_vars={
                    "data": form_data,
                    "errors": e.error_dict,
                    "error_summary": {"summary": "Validation failed"},
                },
            )
    else:
        page_data = model.Session.query(Event).get(page) if page else Event()

        if page_data.content_en is None:
            page_data.content_en = ""
        if page_data.content_ar is None:
            page_data.content_ar = ""

        return tk.render(
            "ckanext_pages/events_edit.html",
            extra_vars={
                "data": page_data,
                "errors": errors or {},
                "error_summary": error_summary or {},
            },
        )
    
def pages_edit(page=None, data=None, errors=None, error_summary=None, page_type='pages'):
    if request.method == 'POST':
        form_data = _parse_form_data(request)

        try:
            result = tk.get_action("ckanext_pages_edit")({}, form_data)
            page_id = result.get("id")
            if not page_id:
                raise ValueError("Page ID is missing for redirect")
            return tk.redirect_to("pages.pages_index")

        except tk.ValidationError as e:
            return tk.render(
                "ckanext_pages/page_edit.html",
                extra_vars={
                    "data": form_data,
                    "errors": e.error_dict,
                    "error_summary": {"summary": "Validation failed"},
                },
            )
    else:
        page_data = model.Session.query(Page).get(page) if page else Page()

        if page_data.content_en is None:
            page_data.content_en = ""
        if page_data.content_ar is None:
            page_data.content_ar = ""

        return tk.render(
            "ckanext_pages/page_edit.html",
            extra_vars={
                "data": page_data,
                "errors": errors or {},
                "error_summary": error_summary or {},
            },
        )

def events_delete(id):

    if request.method == 'POST':
        if 'cancel' in request.form:
            return tk.redirect_to('pages.events')

        if 'confirm' in request.form:
            try:
                event = model.Session.query(Event).filter(Event.id == id).first()
                if not event:
                    raise tk.ObjectNotFound(_("Event not found"))

                model.Session.delete(event)
                model.Session.commit()

                flash(_('Event deleted successfully!'), 'success')
                return tk.redirect_to('pages.events')
            except tk.NotAuthorized:
                return tk.abort(401, _('Unauthorized to delete event'))
            except tk.ObjectNotFound:
                return tk.abort(404, _('Event not found'))

    event = model.Session.query(Event).filter(Event.id == id).first()
    if not event:
        return tk.abort(404, _('Event not found'))
    return tk.render('ckanext_pages/confirm_delete.html', {'page': event})

def news_delete(id):

    if request.method == 'POST':
        if 'cancel' in request.form:
            return tk.redirect_to('pages.news')

        if 'confirm' in request.form:
            try:
                new = model.Session.query(News).filter(News.id == id).first()
                if not new:
                    raise tk.ObjectNotFound(_("New not found"))

                model.Session.delete(new)
                model.Session.commit()

                flash(_('New deleted successfully!'), 'success')
                return tk.redirect_to('pages.news')
            except tk.NotAuthorized:
                return tk.abort(401, _('Unauthorized to delete new'))
            except tk.ObjectNotFound:
                return tk.abort(404, _('Event not found'))

    new = model.Session.query(News).filter(News.id == id).first()
    if not new:
        return tk.abort(404, _('Event not found'))
    return tk.render('ckanext_pages/confirm_delete.html', {'page': new})


def _inject_views_into_page(_page):
    if not p.plugin_loaded('image_view'):
        return
    try:
        import lxml
        import lxml.html
    except ImportError:
        return

    try:
        root = lxml.html.fromstring(_page['content'])
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
            style = "width: %s; height: %s; float: %s; overflow: auto; vertical-align:middle; position:relative" \
                    % (width, height, align)
            element.attrib['style'] = style
            element.attrib['class'] = 'pages-embed'
            view = tk.get_action('resource_view_show')({}, {'id': iframe_src[-36:]})
            context = {}
            resource = tk.get_action('resource_show')(context, {'id': view['resource_id']})
            package_id = context['resource'].resource_group.package_id
            package = tk.get_action('package_show')(context, {'id': package_id})
        except tk.ObjectNotFound:
            error = _('ERROR: View not found {view_id}'.format(view_id=iframe_src))

        if error:
            resource_view_html = '<h4> %s </h4>' % error
        elif not helpers.resource_view_is_iframed(view):
            resource_view_html = helpers.rendered_resource_view(view, resource, package)
        else:
            src = helpers.url_for(
                'resource.view', id=package['name'], resource_id=resource['id'],
                view_id=view['id'], _external=True
            )
            message = _('Your browser does not support iframes.')
            resource_view_html = '<iframe src="{src}" frameborder="0" width="100%" height="100%" ' \
                                 'style="display:block"> <p>{message}</p> </iframe>'.format(src=src, message=message)

        view_element = lxml.html.fromstring(resource_view_html)
        element.append(view_element)

    new_content = six.ensure_text(lxml.html.tostring(root))
    if new_content.startswith('<div>') and new_content.endswith('</div>'):

        new_content = new_content[5:-6]
    elif new_content.startswith('<p>') and new_content.endswith('</p>'):

        new_content = new_content[3:-4]
    _page['content'] = new_content


def pages_show(page=None, page_type='page'):
    tk.c.page_type = page_type
    if page.startswith('/'):
        page = page[1:]
    if not page:
        return pages_list_pages(page_type)
    _page = tk.get_action('ckanext_pages_show')(
        context={},
        data_dict={
            'org_id': None, 'page': page}
    )
    if _page is None:
        return pages_list_pages(page_type)
    tk.c.page = _page
    _inject_views_into_page(_page)

    return tk.render('ckanext_pages/%s.html' % page_type)

def blog_delete(page, page_type):
    pass

def pages_delete(id):


    if request.method == 'POST':
        if 'cancel' in request.form:
            # Redirect back to the pages index if the cancel button is clicked
            return tk.redirect_to('pages.pages_index')

        if 'confirm' in request.form:
            try:
                # Query for the page by ID
                page = model.Session.query(Page).filter(Page.id == id).first()
                if not page:
                    raise tk.ObjectNotFound(_("Page not found"))

                # Delete the page from the database
                model.Session.delete(page)
                model.Session.commit()

                # Flash success message and redirect
                flash(_('Page deleted successfully!'), 'success')
                return tk.redirect_to('pages.pages_index')

            except tk.NotAuthorized:
                # Unauthorized access
                return tk.abort(401, _('Unauthorized to delete page'))
            except tk.ObjectNotFound:
                # Page not found
                return tk.abort(404, _('Page not found'))

    # Render the confirmation template for GET requests
    page = model.Session.query(Page).filter(Page.id == id).first()
    if not page:
        return tk.abort(404, _('Page not found'))

    # Render the confirmation delete template with page details
    return tk.render('ckanext_pages/confirm_delete.html', {'page': page})


def pages_upload():
    if not tk.request.method == 'POST':
        tk.abort(409, _('Only Posting is availiable'))
    data_dict = logic.clean_dict(
        dict_fns.unflatten(
            logic.tuplize_dict(
                logic.parse_params(tk.request.files)
            )
        )
    )
    try:
        upload_info = tk.get_action('ckanext_pages_upload')(None, data_dict)
    except tk.NotAuthorized:
        return tk.abort(401, _('Unauthorized to upload file %s') % id)

    return upload_info


def group_list_pages(id, group_type, group_dict=None):
    tk.c.pages_dict = tk.get_action('ckanext_pages_list')(
        context={}, data_dict={'org_id': tk.c.group_dict['id']}
    )
    return tk.render(
        'ckanext_pages/{}_page_list.html'.format(group_type),
        extra_vars={
            'group_type': group_type,
            'group_dict': group_dict
        })


def _template_setup_group(id, group_type):
    if not id:
        return
    context = {'for_view': True}
    action = 'organization_show' if group_type == 'organization' else 'group_show'
    try:
        tk.c.group_dict = tk.get_action(action)(context, {'id': id})
    except tk.ObjectNotFound:
        tk.abort(404, _('{} not found'.format(group_type.title())))
    except tk.NotAuthorized:
        tk.abort(401, _('Unauthorized to read {} {}'.format(group_type, id)))


def group_show(id, group_type, page=None):

    if page and page.startswith('/'):
        page = page[1:]

    _template_setup_group(id, group_type)

    context = {'for_view': True}

    action = 'organization_show' if group_type == 'organization' else 'group_show'

    group_dict = tk.get_action(action)(context, {'id': id})

    if not page:
        return group_list_pages(id, group_type, group_dict)

    _page = tk.get_action('ckanext_pages_show')(
        context={},
        data_dict={
            'org_id': tk.c.group_dict['id'], 'page': page}
    )
    if _page is None:
        return group_list_pages(id, group_type, group_dict)

    tk.c.page = _page

    return tk.render(
        'ckanext_pages/{}_page.html'.format(group_type),
        {
            'group_type': group_type,
            'group_dict': group_dict
        }
    )


def group_edit(id, group_type, page=None, data=None, errors=None, error_summary=None):

    _template_setup_group(id, group_type)

    page_dict = None
    if page:
        if page.startswith('/'):
            page = page[1:]
        page_dict = tk.get_action('ckanext_pages_show')(
            context={}, data_dict={'org_id': tk.c.group_dict['id'], 'page': page}
        )
    if page_dict is None:
        page_dict = {}

    if tk.request.method == 'POST' and not data:

        data = _parse_form_data(tk.request)

        page_dict.update(data)

        data = _parse_form_data(tk.request)
        page_dict['org_id'] = tk.c.group_dict['id']
        page_dict['page'] = page
        try:
            tk.get_action('ckanext_org_pages_update')(
                context={}, data_dict=page_dict
            )
        except tk.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            return group_edit(id, group_type, page, data, errors, error_summary)

        endpoint = 'pages.{}_pages_show'.format(group_type)
        return tk.redirect_to(endpoint, id=id, page=page_dict['name'])

    if not data:
        data = page_dict

    errors = errors or {}
    error_summary = error_summary or {}

    context = {'for_view': True}

    action = 'organization_show' if group_type == 'organization' else 'group_show'
    group_dict = tk.get_action(action)(context, {'id': id})

    vars = {'data': data, 'errors': errors,
            'error_summary': error_summary, 'page': page,
            'group_type': group_type, 'group_dict': group_dict}

    return tk.render(
        'ckanext_pages/{}_page_edit.html'.format(group_type), extra_vars=vars)


def group_delete(id, group_type, page):

    _template_setup_group(id, group_type)

    if page.startswith('/'):
        page = page[1:]

    if 'cancel' in tk.request.args:
        return tk.redirect_to('pages.%s_edit' % group_type, id=tk.c.group_dict['name'], page=page)

    try:
        if tk.request.method == 'POST':
            action = 'ckanext_org_pages_delete' if group_type == 'organization' else 'ckanext_group_pages_delete'
            action = tk.get_action(action)
            action({}, {'org_id': tk.c.group_dict['id'], 'page': page})
            endpoint = 'pages.{}_pages_index'.format(group_type)
            return tk.redirect_to(endpoint, id=id)
        else:
            tk.abort(404, _('Page Not Found'))
    except tk.NotAuthorized:
        tk.abort(401, _('Unauthorized to delete page'))
    except tk.ObjectNotFound:
        tk.abort(404, _('{} not found'.format(group_type.title())))

    context = {'for_view': True}

    action = 'organization_show' if group_type == 'organization' else 'group_show'
    group_dict = tk.get_action(action)(context, {'id': id})

    return tk.render(
        'ckanext_pages/confirm_delete.html',
        {'page': page, 'group_type': group_type, 'group_dict': group_dict}
    )


def _has_user_role_for_some_org(user: model.User, role):
    q = model.Session.query(model.Member)\
        .filter(model.Member.table_id == user.id)\
        .filter(model.Member.state == 'active')\
        .filter(model.Member.capacity.in_(['admin'] + [role]))

    return bool(q.count())

def is_data_coordinator(context):
    user = context.get('user')
    model = context['model']
    user_obj = model.User.get(user)

    return _has_user_role_for_some_org(user_obj, 'member')


def get_main_page(section_id):
    return MainPage.get(id=section_id)

def validate_main_page(section_id, data):
    schema = main_page_schema(id=section_id)
    try:
        errors = p.toolkit.navl_validate(data, schema)
        if errors:
            print("Validation Errors:", errors)  # Debugging
            return False, errors
        return True, None
    except Exception as e:
        print("Validation Exception:", str(e))  # Debugging
        return False, {'error': str(e)}


def update_main_page(section_id, data):
    section = get_main_page(section_id)
    if section:
        section.main_title_1_ar = data.get('main_title_1_ar')
        section.main_title_1_en = data.get('main_title_1_en')
        section.main_title_2_ar = data.get('main_title_2_ar')
        section.main_title_2_en = data.get('main_title_2_en')
        section.main_brief_en = data.get('main_brief_en')
        section.main_brief_ar = data.get('main_brief_ar')
        model.Session.commit()
        return {"success": True}
    return {"success": False, "error": "Section not found"}


def main_page_edit(section_id, data=None, errors=None, error_summary=None):
    section_titles = {
        1: "Main Title & Brief",
        2: "Open Data Sector",
        3: "Indicators",
        4: "Open Data In Numbers",
        5: "Also Explore"
    }
    section = get_main_page(section_id)

    has_two_titles = True if int(section_id) == 1 else False
    main_page_dict = tk.get_action('ckanext_main_page_show')(
        context={}, data_dict={'section_id': section_id}
    )
    if main_page_dict is None:
        main_page_dict = {}

    # Handle POST (save or delete)
    if tk.request.method == 'POST':
        action = tk.request.form.get('save') or tk.request.form.get('delete')

        data = _parse_form_data(tk.request)
        data['id'] = section_id  # Explicitly set ID

        if action == 'save':
            schema = main_page_schema(id=int(section_id))
            validated_data, errors = df.validate(data, schema, context={})

            if errors:
                tk.h.flash_error(errors)
                return tk.redirect_to('pages.main_page_edit', section_id=section_id)

            # Update section

            section.main_title_1_ar = validated_data.get('main_title_1_ar')
            section.main_title_1_en = validated_data.get('main_title_1_en')
            section.main_title_2_ar = validated_data.get('main_title_2_ar', None)
            section.main_title_2_en = validated_data.get('main_title_2_en', None)
            section.main_brief_en = validated_data.get('main_brief_en')
            section.main_brief_ar = validated_data.get('main_brief_ar')
            section.save()
            model.Session.commit()

            tk.h.flash_success('Section updated successfully!')

        return tk.redirect_to('pages.main_page')

    # Prepare variables for rendering the form
    vars = {
        'has_two_titles': has_two_titles,
        'section_title': section_titles.get(int(section_id), "Unknown Section"),
        'data': main_page_dict or {},
        'errors': errors or {},
        'error_summary': error_summary or {}
    }

    return tk.render('main_page/main_page_edit.html', extra_vars=vars)



    

def main_page():
    sections = MainPage.all()

    section_titles = {
        1: "Title & Brief",
        2: "Open Data Sector",
        3: "Indicators",
        4: "Open Data In Numbers",
        5: "Also Explore"
    }
    data = []
    for section in sections:
        data.append({
            'id': section.id,
            'name': f"Section {section.id}: {section_titles.get(section.id)}",
            'last_update': "25/09/2024"
        })

    return tk.render('main_page/main_page.html', extra_vars={'sections': data})
