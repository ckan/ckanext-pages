# Change log for ckanext-pages

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## 0.3.3 (2021-07-20)

## Fixed

- Fix content styles ([1d96e35](https://github.com/ckan/ckanext-pages/commit/1d96e35))


## 0.3.2 (2021-07-19)

## Fixed

- Fix predefined styles in CKeditor ([#113](https://github.com/ckan/ckanext-pages/pull/113))

## Added

- Move DB tables initialization to CLI commands ([#112](https://github.com/ckan/ckanext-pages/pull/112))
- Allow other plugins to customize CKEditor ([#113](https://github.com/ckan/ckanext-pages/pull/113))
- Add font plugin to CKEditor ([#113](https://github.com/ckan/ckanext-pages/pull/113))

## 0.3.1 (2021-04-07)

## Fixed

- Fix links in blog page ([#111](https://github.com/ckan/ckanext-pages/pull/111))

## Added

- Wrap form fields in blocks for easier extending ([3618dd7](https://github.com/ckan/ckanext-pages/commit/3618dd7))



## 0.3.0 (2021-03-05)

## Added

- CKAN 2.9 and Python 3 support ([#109](https://github.com/ckan/ckanext-pages/pull/109))
- Upgrade CKEditor version ([97a3ecc](ehttps://github.com/ckan/ckanext-pages/commit/97a3ecce))

## 0.2.4 (2021-02-17)


### Fixed

- Do not prefix absolute HTTP URLs of uploaded image 
  ([#107](https://github.com/ckan/ckanext-pages/pull/107))


## 0.2.3 (2020-09-24)

### Added

- Add blocks to main page template
  ([bf9f3c0](https://github.com/ckan/ckanext-pages/commit/bf9f3c0))

### Fixed

- Adding flash_error message in case of missing values
  ([#97](https://github.com/ckan/ckanext-pages/pull/97))


## 0.2.2 (2020-02-28)

### Added

- Allow customizatin of the pages schema from another extension
  ([#95](https://github.com/ckan/ckanext-pages/pull/95))


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

