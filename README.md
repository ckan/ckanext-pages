[![Build Status](https://travis-ci.org/ckan/ckanext-pages.svg?branch=master)](https://travis-ci.org/ckan/ckanext-pages)
[![Coverage Status](https://coveralls.io/repos/ckan/ckanext-pages/badge.svg?branch=master&service=github)](https://coveralls.io/github/ckan/ckanext-pages?branch=master)
ckanext-pages
=============

This extension gives you an easy way to add simple pages to CKAN.

By default you can add pages to the main CKAN menu.

Works for ckan>=2.3

## Installation

Use `pip` to install this plugin. This example installs it in `/home/www-data/pyenv`, assuming you have [setup a virtualenv](http://docs.ckan.org/en/latest/maintaining/installing/install-from-source.html#install-ckan-into-a-python-virtual-environment) there:

```
source /home/www-data/pyenv/bin/activate
pip install -e 'git+https://github.com/ckan/ckanext-pages.git#egg=ckanext-pages'
```

Make sure to add `pages` to `ckan.plugins` in your config file:

```
ckan.plugins = pages
```

## Configuration


Extra config options allow you to control the creation of extra pages against groups and organizations.

To swich on this behaviour, to your config add:

```
ckanext.pages.organization = True
ckanext.pages.group = True
```

These options are False by default and this feature is experimental.


This module also gives you a quick way to remove default elements from the CKAN menu and you may need todo this
in order for you to have space for the new items you add.  These options are:

```
ckanext.pages.about_menu = False
ckanext.pages.group_menu = False
ckanext.pages.organization_menu = False
```

By default these are all set to True, like on a default install.

To enable HTML output for the pages (along with Markdown), add the following to your config:

```
ckanext.pages.allow_html = True
```

By default this option is set to False. Note that this feature is only available for CKAN >= 2.3. For older versions of CKAN, this option has no effect.
Use this option with care and only allow this if you trust the input of your users.

If you want to use the WYSIWYG editor instead of Markdown:
```
ckanext.pages.editor = medium
```
or
```
ckanext.pages.editor = ckeditor
```
This enables either the [medium](https://jakiestfu.github.io/Medium.js/docs/) or [ckeditor](http://ckeditor.com/)

## Extending ckanext-pages schema

This extension defines an `IPagesSchema` interface that allows other extensions to update the pages schema and add custom fields.

To do so, you can implement the method `update_pages_schema` in your extension:

```
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.pages.interfaces import IPagesSchema

class MyextPlugin(plugins.SingletonPlugin):
    plugins.implements(IPagesSchema)

    #IPagesSchema
    def update_pages_schema(self, schema):
        schema.update({
            'new_field': [
                toolkit.get_validator('not_empty'),
                toolkit.get_validator('boolean_validator')]
            })
        return schema
```

and also extends `ckanext_pages/base_form.html` and override the `extra_pages_form` block to add it to the form:

```
{% ckan_extends %}

{% set options = [{'value': True, 'text': _('Yes')}, {'value': False, 'text': _('No')}]%}
{% block extra_pages_form %}
    {{ form.select('new_field', id = 'new_field', label = 'New Field', options=options, selected=data.testing) }}
{% endblock extra_pages_form %}
```

If you want to override, make sure your extension is added before `pages` in the `ckan.plugins` config.

## Dependencies

* lxml


## License

Released under the GNU Affero General Public License (AGPL) v3.0. See the file `LICENSE` for details.


## History

See the file [CHANGELOG.md](CHANGELOG.md).

