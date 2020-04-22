from ckan.plugins.interfaces import Interface


class IPagesSchema(Interface):
    '''
    Interface to define custom schemas.
    '''

    def update_pages_schema(self, schema):
        u'''
        Return a schema with the fields of the pages.

        ckanext-pages will use the returned schema to define the fields of the
        pages and to validate them before storing them.

        Defaults to
        :py:func:`ckanext.pages.logic.schema.default_schema`, which
        will be passed to all extensions implementing this method, which can
        add or remove fields to it.

        :param schema: a dictionary mapping fields keys to lists
          of validator and converter functions to be applied to those keys
        :type schema: dictionary

        :returns: a dictionary mapping fields keys to lists of
          validator and converter functions to be applied to those keys
        :rtype: dictionary
        '''
        return schema
