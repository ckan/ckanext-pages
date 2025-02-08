import ckan.plugins as p
from ckanext.pages.footer import validators
tk = p.toolkit

ignore_empty = tk.get_validator('ignore_empty')
empty = tk.get_validator('empty')
ignore_missing = tk.get_validator('ignore_missing')
not_empty = tk.get_validator('not_empty')
isodate = tk.get_validator('isodate')
unicode_safe = tk.get_validator('unicode_safe')
convert_to_extras = tk.get_converter('convert_to_extras')
natural_number_validator = tk.get_converter('natural_number_validator')
url_validator = tk.get_validator("url_validator")


def _base_simple_link_schema():
    return {
        'id': [not_empty, unicode_safe],
        'title_en': [not_empty, unicode_safe],
        'title_ar': [not_empty, unicode_safe],
        'link_en': [not_empty, url_validator],
        'link_ar': [not_empty, url_validator],
        'target': [not_empty, unicode_safe, validators.link_target_validator],
        'order': [not_empty, unicode_safe],
        'column_number': [not_empty, natural_number_validator, validators.column_number_validator],
    }


def column_link_create_schema():
    schema = _base_simple_link_schema().copy()
    schema['id'] = [empty]
    return schema

def column_link_update_schema():
    schema = _base_simple_link_schema().copy()
    schema['id'].append(validators.column_link_id_validator)
    return schema


def column_links_search_schema():
    return {
        'column_number': [not_empty, natural_number_validator, validators.column_number_validator],
    } 


def _base_image_link_schema():
    return {
        'id': [not_empty, unicode_safe],
        'title_en': [not_empty, unicode_safe],
        'title_ar': [not_empty, unicode_safe],
        'link_en': [not_empty, url_validator],
        'link_ar': [not_empty, url_validator],
        'image_url': [not_empty, unicode_safe],
        'order': [not_empty, unicode_safe],
    }


def social_media_create_schema():
    schema = _base_image_link_schema().copy()
    schema['id'] = [empty]
    return schema

def social_media_update_schema():
    schema = _base_image_link_schema().copy()
    schema['id'].append(validators.social_media_id_validator)
    return schema

def banner_create_schema():
    schema = _base_image_link_schema().copy()
    schema['id'] = [empty]
    return schema

def banner_update_schema():
    schema = _base_image_link_schema().copy()
    schema['id'].append(validators.banner_id_validator)
    return schema



def column_link_get_schema():
    return {
        'id': [not_empty, unicode_safe, validators.column_link_id_validator]
    }


def social_media_get_schema():
    return {
        'id': [not_empty, unicode_safe, validators.social_media_id_validator]
    }


def banner_get_schema():
    return {
        'id': [not_empty, unicode_safe, validators.banner_id_validator]
    }


def column1_update_schema():
    return {
        'logo_en': [ignore_missing, unicode_safe],
        'logo_ar': [ignore_missing, unicode_safe],
        'phone_number': [ignore_missing, unicode_safe],
    }


def column_titles_update_schema():
    return {
        'column2_en': [ignore_missing, unicode_safe],
        'column2_ar': [ignore_missing, unicode_safe],
        'column3_en': [ignore_missing, unicode_safe],
        'column3_ar': [ignore_missing, unicode_safe],
    }