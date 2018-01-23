# encoding: utf-8

import io
import os.path
import re

from setuptools import setup, find_packages


# Extract version
HERE = os.path.abspath(os.path.dirname(__file__))
INIT_PY = os.path.join(HERE, 'ckanext', 'pages', '__init__.py')
version = None
with io.open(INIT_PY) as f:
    for line in f:
        m = re.match(r'__version__\s*=\s*u?[\'"](.*)[\'"]', line)
        if m:
            version = m.groups()[0]
            break
if version is None:
    raise RuntimeError('Could not extract version from "{}".'.format(INIT_PY))


setup(
    name='ckanext-pages',
    version=version,
    description='Basic CMS extension for ckan',
    long_description='',
    classifiers=[
        # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System',
    ],
    keywords='CKAN CMS',
    author='David Raznick',
    author_email='david.raznick@gokfn.org',
    url='https://github.com/ckan/ckanext-pages',
    license='GNU Affero General Public License (AGPL) v3.0',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext'],
    include_package_data=True,
    package_data={
            '': ['theme/*/*.html', 'theme/*/*/*.html', 'theme/*/*/*/*.html'],
    },
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points=\
    """
        [ckan.plugins]
        pages=ckanext.pages.plugin:PagesPlugin
        textboxview=ckanext.pages.plugin:TextBoxView
        [babel.extractors]
        ckan = ckan.lib.extract:extract_ckan
    """,
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/pages/theme/**.html', 'ckan', None),
        ],
    },
)
