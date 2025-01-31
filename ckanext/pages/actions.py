import datetime
import json
import logging
from html.parser import HTMLParser

import ckan.lib.helpers as h
import ckan.lib.navl.dictization_functions as df
import ckan.lib.uploader as uploader
import ckan.plugins as p
from ckan import model
from ckan.lib.navl.dictization_functions import validate
from ckan.logic import ValidationError
from ckan.model import Session
from ckan.plugins import toolkit as tk
from ckan.plugins.toolkit import get_validator, _, h
from ckanext.pages import db
from ckanext.pages.db import MainPage, Page, Event, News, HeaderMainMenu, HeaderLogo, HeaderSecondaryMenu
from ckanext.pages.logic.schema import main_page_schema
from ckanext.pages.logic.schema import update_events_schema, update_pages_schema, update_news_schema

from .logic.schema import header_logo_schema, header_main_menu_schema, header_secondary_menu_schema
from .helpers import _validate_image_upload, _save_image

class HTMLFirstImage(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.first_image = None

    def handle_starttag(self, tag, attrs):
        if tag == 'img' and not self.first_image:
            self.first_image = dict(attrs)['src']


def patch_page(context, data_dict, updated_dict):
    page = (
        context["session"]
        .query(Page)
        .filter(Page.id == data_dict["id"])
        .one_or_none()
    )
    if page is None:
        raise tk.ObjectNotFound(_("Page not found"))

    page.patch_page(**updated_dict)

    context["session"].commit()

    data_dict = get_dictizer(type(page))(page, context)

    return data_dict


_ = tk._
_actions = {}

def action(func):
    func.__name__ = f"pages_{func.__name__}"
    _actions[func.__name__] = func
    return func
def get_actions():
    return _actions.copy()

def _pages_show(context, data_dict):
    org_id = data_dict.get('org_id')
    page = data_dict.get('page')
    out = db.Page.get(group_id=org_id, name=page)
    if out:
        out = db.table_dictize(out, context)
    return out

@action
def page_hide(context, data_dict):
    tk.check_access("pages_page_approve", context, data_dict)
    return patch_page(context, data_dict, {'hidden': True})


@action
def page_unhide(context, data_dict):
    tk.check_access("pages_page_approve", context, data_dict)
    return patch_page(context, data_dict, {'hidden': False})



def _pages_list(context, data_dict):
    print("DEBUG: Data dict received by _pages_list:", data_dict)

    query = model.Session.query(Page)

    sort = data_dict.get('sort', 'title_en asc')  # Default sorting
    if sort == 'created asc':
        query = query.order_by(Page.created.asc())
    elif sort == 'created desc':
        query = query.order_by(Page.created.desc())
    elif sort == 'title_en asc':
        query = query.order_by(Page.title_en.asc())
    elif sort == 'title_en desc':
        query = query.order_by(Page.title_en.desc())
    elif sort == 'publish_date asc':
        query = query.order_by(Page.publish_date.asc())
    elif sort == 'publish_date desc':
        query = query.order_by(Page.publish_date.desc())

    pages = query.all()

    # Log for debugging
    print("DEBUG: Pages fetched from database:", pages)

    out_list = []
    for pg in pages:
        out_list.append({
            'id':pg.id,
            'title_en': pg.title_en,
            'created': pg.created.isoformat(),
            'publish_date': pg.publish_date.isoformat() if pg.publish_date else None,
            'name': pg.name,
            'group_id': pg.group_id,
            'private': pg.private,
            'hidden': pg.hidden,
        })

    print("DEBUG: Final list of pages to return:", out_list)
    return out_list

def _news_list(context, data_dict):
    query = model.Session.query(News)

    sort = data_dict.get('sort', 'title_en asc')  # Default sorting
    if sort == 'created asc':
        query = query.order_by(News.created.asc())
    elif sort == 'created desc':
        query = query.order_by(News.created.desc())
    elif sort == 'title_en asc':
        query = query.order_by(News.title_en.asc())
    elif sort == 'title_en desc':
        query = query.order_by(News.title_en.desc())
    elif sort == 'news_date asc':
        query = query.order_by(News.news_date.asc())
    elif sort == 'news_date desc':
        query = query.order_by(News.news_date.desc())
    else:
        query = query.order_by(News.title_en.asc())

    news = query.all()
    today = datetime.datetime.now()
    out_list = []
    # Build the response list
    for pg in news:
        status = "Disabled"
        if not pg.hidden:
            status = "Upcoming" if pg.news_date > today else "Posted"
        news_dict = {
            'id': pg.id,
            'title_en': pg.title_en,
            'created': pg.created.isoformat(),
            'news_date': pg.news_date.isoformat() if pg.news_date else None,
            'name': pg.name,
            'status': status,
            'hidden': pg.hidden,
        }
        out_list.append(news_dict)

    return out_list


log = logging.getLogger(__name__)


def news_toggle_visibility(context, data_dict):
    news_id = data_dict.get('news_id')

    if not news_id:
        raise p.toolkit.ValidationError("Missing 'news_id' in request.")

    # Fetch the news entry from the database
    news = model.Session.query(News).filter(News.id == news_id).first()
    
    if not news:
        raise p.toolkit.ObjectNotFound(f"News with ID {news_id} not found.")

    # Toggle visibility
    news.hidden = not news.hidden
    model.Session.commit()

    return {'success': True, 'hidden': news.hidden}


def _events_list(context, data_dict):

    query = model.Session.query(Event)

    sort = data_dict.get('sort', 'title_en asc')  # Default sorting
    if sort == 'created asc':
        query = query.order_by(Event.created.asc())
    elif sort == 'created desc':
        query = query.order_by(Event.created.desc())
    elif sort == 'title_en asc':
        query = query.order_by(Event.title_en.asc())
    elif sort == 'title_en desc':
        query = query.order_by(Event.title_en.desc())
    elif sort == 'start_date asc':
        query = query.order_by(Event.start_date.asc())
    elif sort == 'start_date desc':
        query = query.order_by(Event.start_date.desc())
    elif sort == 'end_date asc':
        query = query.order_by(Event.end_date.asc())
    elif sort == 'end_date desc':
        query = query.order_by(Event.end_date.desc())    
    

    events = query.all()

    # Log for debugging

    out_list = []
    today = datetime.datetime.now()
    
    for pg in events:
        status = "Past Event"
        if pg.start_date <= today and pg.end_date > today:
            status = "Currently Happening"
        elif pg.start_date > today:
            status = "Upcoming"

        events_dict = ({
            'title_en': pg.title_en,
            'created': pg.created.isoformat(),
            'start_date': pg.start_date.isoformat() if pg.start_date else None,
            'end_date': pg.end_date.isoformat() if pg.end_date else None,
            'name': pg.name,
            'status': status,
        })
        out_list.append(events_dict)

    return out_list

def _event_edit(context ,data_dict):
    schema = update_events_schema()
    data, errors = df.validate(data_dict, schema, context)
    if errors:
        raise p.toolkit.ValidationError(errors)

    # Fetch or create Page object
    page_id = data_dict.get('id')
    page = model.Session.query(Event).get(page_id) if page_id else Event()

    # Update attributes
    for key, value in data_dict.items():
        if hasattr(page, key):
            setattr(page, key, value)

    # Save and commit
    if not page_id:
        page.created = datetime.datetime.utcnow()
    model.Session.add(page)
    model.Session.commit()

    # Return success with ID
    return {"success": True, "id": page.id}

def _new_edit(context ,data_dict):
    schema = update_news_schema()
    data, errors = df.validate(data_dict, schema, context)
    if errors:
        raise p.toolkit.ValidationError(errors)

    # Fetch or create Page object
    page_id = data_dict.get('id')
    page = model.Session.query(News).get(page_id) if page_id else News()

    # Update attributes
    for key, value in data_dict.items():
        if hasattr(page, key):
            setattr(page, key, value)

    # Save and commit
    if not page_id:
        page.created = datetime.datetime.utcnow()
    model.Session.add(page)
    model.Session.commit()

    # Return success with ID
    return {"success": True, "id": page.id}




def event_edit(context , data_dict):
    try:
        p.toolkit.check_access('ckanext_pages_update', context, data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    return _event_edit(context,data_dict)

def news_edit(context , data_dict):
    try:
        p.toolkit.check_access('ckanext_pages_update', context, data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    return _new_edit(context,data_dict)




def pages_edit_action(context, data_dict):

    schema = update_pages_schema()
    data, errors = df.validate(data_dict, schema, context)
    if errors:
        raise p.toolkit.ValidationError(errors)

    # Fetch or create Page object
    page_id = data_dict.get('id')
    page = model.Session.query(Page).get(page_id) if page_id else Page()

    # Update attributes
    for key, value in data_dict.items():
        if hasattr(page, key):
            setattr(page, key, value)

    # Save and commit
    if not page_id:
        page.created = datetime.datetime.utcnow()
    model.Session.add(page)
    model.Session.commit()

    # Return success with ID
    return {"success": True, "id": page.id}



def _pages_delete(context, data_dict):
    org_id = data_dict.get('org_id')
    page = data_dict.get('page')
    out = db.Page.get(group_id=org_id, name=page)
    if out:
        session = context['session']
        session.delete(out)
        session.commit()


def _pages_update(context, data_dict):
    org_id = data_dict.get('org_id')
    page = data_dict.get('page')
    # we need the page in the context for name validation
    context['page'] = page
    context['group_id'] = org_id
    schema = update_pages_schema()

    data, errors = df.validate(data_dict, schema, context)
    if errors:
        raise p.toolkit.ValidationError(errors)

    out = db.Page.get(group_id=org_id, name=page)
    if not out:
        out = db.Page()
        out.group_id = org_id
        out.name = page
    items = ['title_en', 'title_at', 'name', 'content_en', 'content_ar','image_url', 'lang',
             'order', 'page_type', 'publish_date', 'hidden']

    # backward compatible with older version where page_type does not exist
    for item in items:
        setattr(out, item, data.get(item, 'page' if item == 'page_type' else None))

    extras = {}

    extra_keys = set(schema.keys()) - set(items + ['id', 'created'])
    for key in extra_keys:
        if key in data:
            extras[key] = data.get(key)
    out.extras = json.dumps(extras)

    out.modified = datetime.datetime.utcnow()
    user = model.User.get(context['user'])
    out.user_id = user.id
    out.save()
    session = context['session']
    session.add(out)
    session.commit()


def pages_upload(context, data_dict):
    """ Upload a file to the CKAN server.

    This method implements the logic for file uploads used by CKEditor. For
    more details on implementation and expected return values see:
     - https://ckeditor.com/docs/ckeditor4/latest/guide/dev_file_upload.html#server-side-configuration

    """

    try:
        p.toolkit.check_access('ckanext_pages_upload', context, data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))

    upload = uploader.get_uploader('page_images')

    upload.update_data_dict(data_dict, 'image_url',
                            'image_upload', 'clear_upload')

    max_image_size = uploader.get_max_image_size()

    try:
        upload.upload(max_image_size)
    except p.toolkit.ValidationError:
        message = (
            "Can't upload the file, size is too large. "
            "(Max allowed is {0}mb)".format(max_image_size)
        )
        return {'uploaded': 0, 'error': {'message': message}}

    image_url = data_dict.get('image_url')
    if image_url and image_url[0:6] not in {'http:/', 'https:'}:
        image_url = h.url_for_static(
            'uploads/page_images/{}'.format(image_url),
            qualified=True
        )
    return {'url': image_url, 'fileName': upload.filename, 'uploaded': 1}


@tk.side_effect_free
def pages_show(context, data_dict):
    try:
        p.toolkit.check_access('ckanext_pages_show', context, data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    return _pages_show(context, data_dict)


def pages_update(context, data_dict):
    try:
        p.toolkit.check_access('ckanext_pages_update', context, data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    return _pages_update(context, data_dict)





@tk.side_effect_free
def pages_list(context, data_dict):
    try:
        p.toolkit.check_access('ckanext_pages_list', context, data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    
    # Log for debugging purposes
    print("DEBUG: Data dict received in pages_list:", data_dict)
    
    pages = _pages_list(context, data_dict)
    
    # Log the returned pages for debugging
    print("DEBUG: Pages returned by _pages_list:", pages)
    
    return pages
@tk.side_effect_free
def news_list(context, data_dict):
    try:
        p.toolkit.check_access('ckanext_pages_list', context, data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    news = _news_list(context, data_dict)
    
    return news

@tk.side_effect_free
def events_list(context, data_dict):
    try:
        p.toolkit.check_access('ckanext_pages_list', context, data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    events = _events_list(context, data_dict)
    
    return events

@action
def events_delete(context, data_dict):

    tk.check_access("ckanext_pages_delete", context, data_dict)
    event = context["session"].query(Event).filter(Event.name == data_dict["page"]).first()
    if not event:
        raise tk.ObjectNotFound(_("Event not found"))
    context["session"].delete(event)
    context["session"].commit()
    return {"success": True}

@action
def news_delete(context, data_dict):
    tk.check_access("ckanext_pages_delete", context, data_dict)
    new = context["session"].query(News).filter(News.name == data_dict["page"]).first()
    if not new:
        raise tk.ObjectNotFound(_("Event not found"))
    context["session"].delete(new)
    context["session"].commit()
    return {"success": True}

@action
def pages_delete(context, data_dict):
    tk.check_access("ckanext_pages_delete", context, data_dict)
    page = context["session"].query(Page).filter(Page.name == data_dict["page"]).first()
    if not page:
        raise tk.ObjectNotFound(_("Event not found"))
    context["session"].delete(page)
    context["session"].commit()
    return {"success": True}



@tk.side_effect_free
def org_pages_show(context, data_dict):
    try:
        p.toolkit.check_access('ckanext_org_pages_show', context, data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    return _pages_show(context, data_dict)


def org_pages_update(context, data_dict):
    try:
        p.toolkit.check_access('ckanext_org_pages_update', context,
                               data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    return _pages_update(context, data_dict)


def org_pages_delete(context, data_dict):
    try:
        p.toolkit.check_access('ckanext_org_pages_delete', context,
                               data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    return _pages_delete(context, data_dict)


@tk.side_effect_free
def org_pages_list(context, data_dict):
    try:
        p.toolkit.check_access('ckanext_org_pages_list', context, data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    return _pages_list(context, data_dict)


@tk.side_effect_free
def group_pages_show(context, data_dict):
    try:
        p.toolkit.check_access('ckanext_group_pages_show', context, data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    return _pages_show(context, data_dict)


def group_pages_update(context, data_dict):
    try:
        p.toolkit.check_access('ckanext_group_pages_update', context,
                               data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    return _pages_update(context, data_dict)


def group_pages_delete(context, data_dict):
    try:
        p.toolkit.check_access('ckanext_group_pages_delete', context,
                               data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    return _pages_delete(context, data_dict)


@tk.side_effect_free
def group_pages_list(context, data_dict):
    try:
        p.toolkit.check_access('ckanext_group_pages_list', context, data_dict)
    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    return _pages_list(context, data_dict)

def validate_main_page(section_id, data):
    # Get the schema for validation
    schema = main_page_schema()

    # Remove 'id' field if not required by schema
    data.pop('id', None)  # Prevent schema errors for 'id'

    # Validate the rest of the data
    errors = p.toolkit.navl_validate(data, schema)

    # Return validation result
    if errors:
        return False, errors
    return True, None



def get_main_page(section_id):
    return MainPage.get(id=section_id)

def update_main_page(section_id, data):
    section = MainPage.get(id=section_id)
    if section:
        section.main_title_1_ar = data.get('main_title_1_ar')
        section.main_title_1_en = data.get('main_title_1_en')
        section.main_title_2_ar = data.get('main_title_2_ar', '')
        section.main_title_2_en = data.get('main_title_2_en', '')
        section.main_brief_en = data.get('main_brief_en')
        section.main_brief_ar = data.get('main_brief_ar')
        model.Session.commit()
        return {"success": True}
    return {"success": False, "error": "Section not found"}


def main_page_edit(section_id):
    section_titles = {
        1: "Main Title & Brief",
        2: "Open Data Sector",
        3: "Indicators",
        4: "Open Data In Numbers",
        5: "Also Explore"
    }

    has_two_titles = True if int(section_id) == 1 else False

    section = MainPage.get(id=section_id)

    if not section:
        tk.h.flash_error('Section not found!')
        return tk.redirect_to('main_page')

    if tk.request.method == 'POST':
        action = tk.request.form.get('save') or tk.request.form.get('delete')

        if action == 'save':
            data = {
                "main_title_1_ar": tk.request.form['main_title_1_ar'],
                "main_title_1_en": tk.request.form['main_title_1_en'],
                "main_title_2_ar": tk.request.form.get('main_title_2_ar') if has_two_titles else None,
                "main_title_2_en": tk.request.form.get('main_title_2_en') if has_two_titles else None,
                "main_brief_en": tk.request.form['main_brief_en'],
                "main_brief_ar": tk.request.form['main_brief_ar'],
            }

            valid, errors = validate_main_page(section_id, data)
            if not valid:
                tk.h.flash_error(errors)
                return tk.redirect_to('pages.main_page_edit', section_id=section_id)

            update_main_page(section_id, data)
            tk.h.flash_success('Section updated successfully!')

        elif action == 'delete':
            tk.h.flash_error('Section deleted successfully!')
            return tk.redirect_to('main_page')

        return tk.redirect_to('main_page')

    return tk.render(
        'main_page/main_page_edit.html',
        section=section,
        has_two_titles=has_two_titles,
        section_title=section_titles.get(int(section_id), "Unknown Section")
    )

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

    return tk.render('main_page/main_page.html', sections=data)

def _main_page_show(context, data_dict):
    section_id = data_dict.get('section_id')

    out = db.MainPage.get(id=section_id)
    if out:
        out = db.table_dictize(out, context)
    return out


@tk.side_effect_free
def main_page_show(context, data_dict):
    try:
        tk.check_access('ckanext_pages_update', {'user': tk.g.user})

    except p.toolkit.NotAuthorized:
        p.toolkit.abort(401, p.toolkit._('Not authorized to see this page'))
    return _main_page_show(context, data_dict)

def pages_list(context, data_dict):
    query = model.Session.query(Page)
    sort = data_dict.get('sort', 'publish_date asc')
    if sort == 'publish_date asc':
        query = query.order_by(Page.publish_date.asc())
    elif sort == 'publish_date desc':
        query = query.order_by(Page.publish_date.desc())
    elif sort == 'title_en asc':
        query = query.order_by(Page.title_en.asc())
    elif sort == 'title_en desc':
        query = query.order_by(Page.title_en.desc())
    elif sort == 'created asc':
        query = query.order_by(Page.created.asc())
    else:
        query = query.order_by(Page.created.desc())

    return [page.as_dict() for page in query.all()]



def events_edit(context, data_dict):
    event_id = data_dict.get('id')
    if event_id:
        # Fetch the event from the database
        event = model.Session.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise p.toolkit.ObjectNotFound(f"Event with ID {event_id} not found.")
    else:
        # Creating a new event
        event = Event()

    # Update the fields
    event.title_en = data_dict.get('title_en', event.title_en)
    event.title_ar = data_dict.get('title_ar', event.title_ar)
    event.start_date = data_dict.get('start_date', event.start_date)
    event.end_date = data_dict.get('end_date', event.end_date)
    event.brief_en = data_dict.get('brief_en', event.brief_en)
    event.brief_ar = data_dict.get('brief_ar', event.brief_ar)
    event.content_en = data_dict.get('content_en', event.content_en)
    event.content_ar = data_dict.get('content_ar', event.content_ar)
    event.image_url = data_dict.get('image_url', event.image_url)
    event.lang = data_dict.get('lang', event.lang)

    # Save the changes to the database
    model.Session.add(event)
    model.Session.commit()
    return event.as_dict()


def news_edit(context, data_dict):
    news_id = data_dict.get('id')
    if news_id:
        # Fetch the news entry from the database
        news = model.Session.query(News).filter(News.id == news_id).first()
        if not news:
            raise p.toolkit.ObjectNotFound(f"News with ID {news_id} not found.")
    else:
        # Creating a new news entry
        news = News()

    # Update the fields
    news.title_en = data_dict.get('title_en', news.title_en)
    news.title_ar = data_dict.get('title_ar', news.title_ar)
    news.news_date = data_dict.get('news_date', news.news_date)
    news.brief_en = data_dict.get('brief_en', news.brief_en)
    news.brief_ar = data_dict.get('brief_ar', news.brief_ar)
    news.content_en = data_dict.get('content_en', news.content_en)
    news.content_ar = data_dict.get('content_ar', news.content_ar)
    news.image_url = data_dict.get('image_url', news.image_url)
    news.lang = data_dict.get('lang', news.lang)
    # Save the changes to the database
    model.Session.add(news)
    model.Session.commit()
    return news.as_dict()

# Create Actions
def header_logo_create(context, data_dict):
    schema = header_logo_schema()
    data, errors = validate(data_dict, schema)
    if errors:
        raise ValidationError(errors)

    # Handle logo_en upload
    logo_en_file = request.files.get('logo_en')
    logo_en_filename = _validate_image_upload(logo_en_file)
    logo_en_path = _save_image(logo_en_file, logo_en_filename)

    # Handle logo_ar upload
    logo_ar_file = request.files.get('logo_ar')
    logo_ar_filename = _validate_image_upload(logo_ar_file)
    logo_ar_path = _save_image(logo_ar_file, logo_ar_filename)

    logo = HeaderLogo()
    logo.logo_en = logo_en_path
    logo.logo_ar = logo_ar_path
    logo.is_visible = data.get('is_visible', True)
    Session.add(logo)
    Session.commit()
    return logo.id


def header_main_menu_create(context, data_dict):
    schema = header_main_menu_schema()
    data, errors = validate_dict(data_dict, schema)

    if not data.get('parent_id'):
        count = Session.query(HeaderMainMenu).filter_by(parent_id=None).count()
        if count >= 6:
            errors['max_items'] = _('Not More Than 6 Items Can Be Added In The Header Menu Without Any Parent.')

    if errors:
        raise ValidationError(errors)

    menu = HeaderMainMenu()
    menu.title_en = data['title_en']
    menu.title_ar = data['title_ar']
    menu.link_en = data['link_en']
    menu.link_ar = data['link_ar']
    menu.menu_type = data['menu_type']
    menu.parent_id = data.get('parent_id')
    menu.order = data.get('order', 0)
    menu.is_visible = data.get('is_visible', True)
    Session.add(menu)
    Session.commit()
    return menu.id

def header_secondary_menu_create(context, data_dict):
    schema = header_secondary_menu_schema()
    data, errors = validate(data_dict, schema)
    if errors:
        raise ValidationError(errors)

    menu = HeaderSecondaryMenu()
    menu.title_en = data['title_en']
    menu.title_ar = data['title_ar']
    menu.link_en = data['link_en']
    menu.link_ar = data['link_ar']
    menu.order = data.get('order', 0)
    menu.is_visible = data.get('is_visible', True)
    Session.add(menu)
    Session.commit()
    return menu.id

# Update Actions
def header_logo_update(context, data_dict):
    schema = header_logo_schema()
    data, errors = validate(data_dict, schema)
    if errors:
        raise ValidationError(errors)

    logo = Session.query(HeaderLogo).get(data['id'])
    if not logo:
        raise ValidationError({'id': _('Logo not found')})

    # Handle logo_en upload
    if 'logo_en' in request.files:
        logo_en_file = request.files['logo_en']
        logo_en_filename = _validate_image_upload(logo_en_file)
        logo.logo_en = _save_image(logo_en_file, logo_en_filename)

    # Handle logo_ar upload
    if 'logo_ar' in request.files:
        logo_ar_file = request.files['logo_ar']
        logo_ar_filename = _validate_image_upload(logo_ar_file)
        logo.logo_ar = _save_image(logo_ar_file, logo_ar_filename)

    logo.is_visible = data.get('is_visible', True)
    logo.modified = datetime.datetime.utcnow()
    Session.commit()
    return logo.id


def header_main_menu_update(context, data_dict):
    schema = header_main_menu_schema()
    data, errors = validate_dict(data_dict, schema)
    if errors:
        raise ValidationError(errors)

    menu = Session.query(HeaderMainMenu).get(data['id'])
    if not menu:
        raise ValidationError({'id': _('Menu item not found')})

    if not data.get('parent_id'):
        count = Session.query(HeaderMainMenu).filter_by(parent_id=None).count()
        if count >= 6:
            errors['max_items'] = _('Not More Than 6 Items Can Be Added In The Header Menu Without Any Parent.')

    if errors:
        raise ValidationError(errors)

    menu.title_en = data['title_en']
    menu.title_ar = data['title_ar']
    menu.link_en = data['link_en']
    menu.link_ar = data['link_ar']
    menu.menu_type = data['menu_type']
    menu.parent_id = data.get('parent_id')
    menu.order = data.get('order', 0)
    menu.is_visible = data.get('is_visible', True)
    menu.modified = datetime.datetime.utcnow()
    Session.commit()
    return menu.id

def header_secondary_menu_update(context, data_dict):
    schema = header_secondary_menu_schema()
    data, errors = validate(data_dict, schema)
    if errors:
        raise ValidationError(errors)

    menu = Session.query(HeaderSecondaryMenu).get(data['id'])
    if not menu:
        raise ValidationError({'id': _('Menu item not found')})

    menu.title_en = data['title_en']
    menu.title_ar = data['title_ar']
    menu.link_en = data['link_en']
    menu.link_ar = data['link_ar']
    menu.order = data.get('order', 0)
    menu.is_visible = data.get('is_visible', True)
    menu.modified = datetime.datetime.utcnow()
    Session.commit()
    return menu.id

# Delete Actions
def header_logo_delete(context, data_dict):
    logo = Session.query(HeaderLogo).get(data_dict['id'])
    if not logo:
        raise ValidationError({'id': _('Logo not found')})

    Session.delete(logo)
    Session.commit()
    return True

def header_main_menu_delete(context, data_dict):
    menu = Session.query(HeaderMainMenu).get(data_dict['id'])
    if not menu:
        raise ValidationError({'id': _('Menu item not found')})

    Session.delete(menu)
    Session.commit()
    return True

def header_secondary_menu_delete(context, data_dict):
    menu = Session.query(HeaderSecondaryMenu).get(data_dict['id'])
    if not menu:
        raise ValidationError({'id': _('Menu item not found')})

    Session.delete(menu)
    Session.commit()
    return True

# Toggle Visibility Actions
def header_logo_toggle_visibility(context, data_dict):
    logo = Session.query(HeaderLogo).get(data_dict['id'])
    if not logo:
        raise ValidationError({'id': _('Logo not found')})

    logo.is_visible = not logo.is_visible
    logo.modified = datetime.datetime.utcnow()
    Session.commit()
    return logo.is_visible

def header_main_menu_toggle_visibility(context, data_dict):
    menu = Session.query(HeaderMainMenu).get(data_dict['id'])
    if not menu:
        raise ValidationError({'id': _('Menu item not found')})

    menu.is_visible = not menu.is_visible
    menu.modified = datetime.datetime.utcnow()
    Session.commit()
    return menu.is_visible

def header_secondary_menu_toggle_visibility(context, data_dict):
    menu = Session.query(HeaderSecondaryMenu).get(data_dict['id'])
    if not menu:
        raise ValidationError({'id': _('Menu item not found')})

    menu.is_visible = not menu.is_visible
    menu.modified = datetime.datetime.utcnow()
    Session.commit()
    return menu.is_visible