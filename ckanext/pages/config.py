from __future__ import annotations

import ckan.plugins.toolkit as tk

ABOUT_MENU = "ckanext.pages.about_menu"
GROUP_MENU = "ckanext.pages.group_menu"
ORGANIZATION_MENU = "ckanext.pages.organization_menu"
ALLOW_HTML = "ckanext.pages.allow_html"
EDITOR = "ckanext.pages.editor"
ENABLE_ORGANIZATION_PAGES = "ckanext.pages.organization"
ENABLE_GROUP_PAGES = "ckanext.pages.group"
REVISIONS_LIMIT = "ckanext.pages.revisions_limit"
FORCE_REVISIONS_LIMIT = "ckanext.pages.revisions_force_limit"
FORM = "ckanext.pages.form"


def about_menu() -> bool:
    return tk.config[ABOUT_MENU]


def group_menu() -> bool:
    return tk.config[GROUP_MENU]


def organization_menu() -> bool:
    return tk.config[ORGANIZATION_MENU]


def allow_html() -> bool:
    return tk.config[ALLOW_HTML]


def editor() -> str:
    return tk.config[EDITOR]


def enable_organization_pages() -> bool:
    return tk.config[ENABLE_ORGANIZATION_PAGES]


def enable_group_pages() -> bool:
    return tk.config[ENABLE_GROUP_PAGES]


def revisions_limit() -> int:
    return tk.config[REVISIONS_LIMIT]


def force_revisions_limit() -> bool:
    return tk.config[FORCE_REVISIONS_LIMIT]


def form() -> str:
    return tk.config[FORM]
