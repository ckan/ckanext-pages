
![Tests](https://github.com/ckan/ckanext-pages/workflows/Tests/badge.svg?branch=master)

ckanext-pages
=============

This extension gives you an easy way to add simple pages to CKAN.

By default you can add pages to the main CKAN menu.

Tested on CKAN 2.7, 2.8 and 2.9.

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

## Database initialization

You need to initialize database from command line with the following commands:

ON CKAN >= 2.9:
```
(pyenv) $ ckan --config=/etc/ckan/default/ckan.ini pages initdb
```

ON CKAN <= 2.8:
```
(pyenv) $ paster --plugin=ckanext-pages pages initdb --config=/etc/ckan/default/production.ini
```

## Configuration


Extra config options allow you to control the creation of extra pages against groups and organizations.

To swich on this behaviour, to your config add:

```
ckanext.pages.organization = True
ckanext.pages.group = True
```

These options are False by default.


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

## Extending the default CKEditor configuration

The default configuration used by the CKEditor widget is defined in the [`ckanext/pages/assets/js/ckedit.js`](https://github.com/ckan/ckanext-pages/blob/master/ckanext/pages/assets/js/ckedit.js) file. This configuration can be overriden from your own plugin setting the `window.ckan.pages.override_config` variable. For example, create the following script in your extension:

    ```js
    this.ckan = this.ckan || {};
    this.ckan.pages = this.ckan.pages || {};

    $(document).ready(function() {

      window.ckan.pages.override_config = {
          toolbarGroups: [
            //... your custom toolbar
          ],
          extraPlugins: '', // Add extra plugins here (make sure to also load their js/css assets from your plugin)
          // ...

      }

    });
    ```

Configure your [plugin assets](https://docs.ckan.org/en/2.9/theming/webassets.html) to serve the script above, and extend the `ckanext_pages/base_form.html` template to add the asset to the ckanext-pages form page:

    ```
    {% ckan_extends %}

    {% asset 'my-plugin/pages-extra-config.js' %}

    ```

## Dependencies

* lxml (optional, only used for injecting resource views into pages)


## License

Released under the GNU Affero General Public License (AGPL) v3.0. See the file `LICENSE` for details.


## History

See the file [CHANGELOG.md](CHANGELOG.md).

