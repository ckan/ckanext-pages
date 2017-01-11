from setuptools import setup, find_packages

version = '0.1'

setup(
	name='ckanext-pages',
	version=version,
	description='Basic CMS extension for ckan',
	long_description='',
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='David Raznick',
	author_email='david.raznick@gokfn.org',
	url='',
	license='',
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
