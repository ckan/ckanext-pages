import ckan.plugins as p
import ckan.lib.navl.dictization_functions as df
from ckanext.pages import db


def page_name_validator(key, data, errors, context):
    session = context['session']
    page = context.get('page')
    group_id = context.get('group_id')
    if page and page == data[key]:
        return

    query = session.query(db.Page.name).filter_by(name=data[key], group_id=group_id)
    result = query.first()
    if result:
        errors[key].append(
            p.toolkit._('Page name already exists in database'))


def not_empty_if_blog(key, data, errors, context):
    value = data.get(key)
    if data.get(('page_type',), '') == 'blog':
        if value is df.missing or not value:
            errors[key].append('Publish Date Must be supplied')


def validate_logo_upload(key, data, errors, context, file_size=2):
    """Validator for logo uploads."""
    value = data.get(key)
    if not value:
        return

    # Check file type
    if value.type not in ['image/jpeg', 'image/png', 'image/gif']:
        errors[key].append(
            'File must be a valid image file (JPEG, PNG, or GIF)'
        )
        return

    # Check file size (2MB max)
    if value.content_length > file_size * 1024 * 1024:
        errors[key].append(
            'File size must be less than 2MB'
        )
        return
