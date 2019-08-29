# Change log for ckanext-pages

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## 0.2.1 (2019-08-29)

### Fixed

- Added i18n folder to manifest
  ([97a15d9](https://github.com/ckan/ckanext-pages/commit/97a15d9))


## 0.2.0 (2019-08-29)

### Fixed

- Fixed support for CKAN 2.8 and CKAN 2.9
  ([d60ba49](https://github.com/ckan/ckanext-pages/commit/d60ba49))

- Order pages numerically in the header menu
  ([eb7d215](https://github.com/ckan/ckanext-pages/commit/eb7d215)

- Remove extraneous tags added by lxml that prevent proper rendering
  ([bf25e9](https://github.com/ckan/ckanext-pages/commit/bf25e9))

- Fix about menu not being hidden
  ([#83](https://github.com/ckan/ckanext-pages/pull/83))

- Fix group/org pages update permissions
  ([#84](https://github.com/ckan/ckanext-pages/pull/84))

- Fixed wrong redirects when using non-default language
  ([#60](https://github.com/ckan/ckanext-pages/issues/60))

- Group and organization pages could not be deleted
  ([#53](https://github.com/ckan/ckanext-pages/issues/53))

- Fixed crash when Unicode is used in a menu item
  ([#54](https://github.com/ckan/ckanext-pages/issues/54))


### Changed

- Upgrade to font-awesome 4 on CKAN 2.7 and later
  ([#51](https://github.com/ckan/ckanext-pages/pull/51))

- Honour ckan.max_images_size config option
  ([915028](https://github.com/ckan/ckanext-pages/commit/915028))


### Added

- Added information regarding the project's license
  ([#73](https://github.com/ckan/ckanext-pages/issues/73))

- Added option to edit source code in CKEditor
 ([c66e02f](https://github.com/ckan/ckanext-pages/commit/c66e02f))

- Added Spanish translation
 ([a426338](https://github.com/ckan/ckanext-pages/commit/a426338))


## 0.1.0 (2017-03-23)

First release following the [Semantic Versioning](http://semver.org/)
guidelines (*ckanext-pages* has been publicly available before without tagged
releases). This release captures the current state and serves as a baseline for
tracking future changes.


[Unreleased]: https://github.com/ckan/ckanext-pages/compare/release-v0.1.0...master

