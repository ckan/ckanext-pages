# Change log for ckanext-pages

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

# Cambios

## Poncho theme

Se baja el theme de poncho.
En principio se utilizará el css, en el futuro se implementará sass.
[Repositorio github de poncho] (https://argob.github.io/poncho/)

### Modificaciones realizadas para el blog

En poncho.css se agrega mas espacio entre parrafo y parrafo y en el interlineado.
Y también entre la lista de items.

Para las noticicas se usará la clase article-news
´´´
.article-news article section {
  font-family: "Droid Serif", serif;
}

.article-news p {
  font-size: 18px;
  margin-bottom: 25px;
  line-height: 1.528;
}
.article-news li {
  font-size: 18px;
  margin-bottom: 25px;
}
´´´

### Copia de css
Es necesario copiar todos los css de poncho en los recursos de pages. A futuro si el theme se extiende al ckan entero habrá que incluirlo
en el ckan default.

Directorio donde copiar los css:
**ckan-desa:/usr/lib/ckan/default/src/ckan/ckanext/src/ckanext-pages/ckanext/pages/theme/resources/styles**

## Template
Es necesario modificar el template especifico relacionado a blog para por un lado incluir el theme de Poncho, y por el otro modificar el grid html de blog.

El template a modificar es el especifico del blog:
**/usr/lib/ckan/default/src/ckan/ckanext/src/ckanext-pages/ckanext/pages/theme/templates_main/ckanext_pages/blog.html**

## [Unreleased]

### Fixed

- Fixed wrong redirects when using non-default language
  ([#60](https://github.com/ckan/ckanext-pages/issues/60))

- Group and organization pages could not be deleted
  ([#53](https://github.com/ckan/ckanext-pages/issues/53))

- Fixed crash when Unicode is used in a menu item
  ([#54](https://github.com/ckan/ckanext-pages/issues/54))


### Changed

- Upgrade to font-awesome 4 on CKAN 2.7 and later
  ([#51](https://github.com/ckan/ckanext-pages/pull/51))


### Added

- Added information regarding the project's license
  ([#73](https://github.com/ckan/ckanext-pages/issues/73))

## 0.1.0 (2017-03-23)

First release following the [Semantic Versioning](http://semver.org/)
guidelines (*ckanext-pages* has been publicly available before without tagged
releases). This release captures the current state and serves as a baseline for
tracking future changes.


[Unreleased]: https://github.com/ckan/ckanext-pages/compare/release-v0.1.0...master

