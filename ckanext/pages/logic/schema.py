import ckan.plugins as p
from ckanext.pages.validators import page_name_validator, not_empty_if_blog
from ckanext.pages.interfaces import IPagesSchema

def default_pages_schema():
    return {
        'id': [p.toolkit.get_validator('ignore_empty'), unicode],
        'title': [p.toolkit.get_validator('not_empty'), unicode],
        'name': [p.toolkit.get_validator('not_empty'), unicode,
                p.toolkit.get_validator('name_validator'), page_name_validator],
        'content': [p.toolkit.get_validator('ignore_missing'), unicode],
        'page_type': [p.toolkit.get_validator('ignore_missing'), unicode],
        'order': [p.toolkit.get_validator('ignore_missing'), unicode],
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


def update_pages_schema():
    '''
    Returns the schema for the pages fields that can be added by other
    extensions.

    By default these are the keys of the
    :py:func:`ckanext.logic.schema.default_pages_schema`.
    Extensions can add or remove keys from this schema using the
    :py:meth:`ckanext.pages.interfaces.IPagesSchema.update_pages_schema`
    method.

    :returns: a dictionary mapping fields keys to lists of validator and
    converter functions to be applied to those fields
    :rtype: dictionary
    '''

    schema = default_pages_schema()
    for plugin in p.PluginImplementations(IPagesSchema):
        if hasattr(plugin, 'update_pages_schema'):
            schema = plugin.update_pages_schema(schema)

    return schema
