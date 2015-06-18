[![Build Status](https://travis-ci.org/pages/ckanext-pages.svg?branch=master)](https://travis-ci.org/ckan/ckanext-pages)
[![Coverage Status](https://coveralls.io/repos/pages/ckanext-pages/badge.svg)](https://coveralls.io/r/ckan/ckanext-pages)
ckanext-pages
=============

This extension gives you an easy way to add simple pages to CKAN.

By default you can add pages to the main CKAN menu.



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
