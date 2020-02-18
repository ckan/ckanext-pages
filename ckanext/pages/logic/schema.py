import ckan.plugins as p
from ckanext.pages.validators import page_name_validator, not_empty_if_blog

def default_pages_schema():
    return {
        'id': [p.toolkit.get_validator('ignore_empty'), unicode],
        'title': [p.toolkit.get_validator('not_empty'), unicode],
        'name': [p.toolkit.get_validator('not_empty'), unicode,
                p.toolkit.get_validator('name_validator'), page_name_validator],
        'content': [p.toolkit.get_validator('ignore_missing'), unicode],
        'page_type': [p.toolkit.get_validator('ignore_missing'), unicode],
        'order': [p.toolkit.get_validator('ignore_missing'),
                unicode],
        'private': [p.toolkit.get_validator('ignore_missing'),
                    p.toolkit.get_validator('boolean_validator')],
        'group_id': [p.toolkit.get_validator('ignore_missing'), unicode],
        'user_id': [p.toolkit.get_validator('ignore_missing'), unicode],
        'created': [p.toolkit.get_validator('ignore_missing'),
                    p.toolkit.get_validator('isodate')],
        'publish_date': [not_empty_if_blog,
                        p.toolkit.get_validator('ignore_missing'),
                        p.toolkit.get_validator('isodate')],
    }