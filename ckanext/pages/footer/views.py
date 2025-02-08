# encoding: utf-8
from __future__ import annotations

from flask import Blueprint, request
from ckan.lib.helpers import helper_functions as h


import logging
import ckan.lib.base as base
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.logic as logic
import ckan.plugins.toolkit as tk
import ckan.model as model


from typing import Any, Optional, Union, cast
from flask import Blueprint
from flask.views import MethodView
from ckan.common import current_user, _, request

from ckan.views.home import CACHE_PARAMETERS
from ckan.types import Context, Response
from flask import request
from functools import partial
from ckan.lib.helpers import Page


_get_action = logic.get_action
_tuplize_dict = logic.tuplize_dict
_clean_dict = logic.clean_dict
_parse_params = logic.parse_params


log = logging.getLogger(__name__)

blueprint = Blueprint('cms_footer', __name__, url_prefix='/footer-management')


class IndexView(MethodView):
    def _prepare(self) -> Context:
        context = cast(Context, {
            u'model': model,
            u'session': model.Session,
            u'user': current_user.name,
            u'auth_user_obj': current_user,
        })

        try:
            tk.check_access(u'is_content_editor', context)
        except tk.NotAuthorized:
            return base.abort(403, _(u'Unauthorized to update CMS footer'))
        return context

    def post(self) -> Union[Response, str]:
        context = self._prepare()

        data_dict = _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(_parse_params(tk.request.form))))


        try:
            column_titles = tk.get_action('footer_column_titles_update')(context, data_dict)

        except tk.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.get(data_dict, errors, error_summary)

        return self.get()


    def get(self, data: Optional[dict[str, Any]] = None,
            errors: Optional[dict[str, Any]] = None,
            error_summary: Optional[dict[str, Any]] = None) -> str:

        context = self._prepare()
        
        data = data or _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(
                    _parse_params(request.args, ignore_keys=CACHE_PARAMETERS)
                )
            )
        )

        previous_column_titles_data = tk.get_action('footer_column_titles_show')(context, {})

        data = {**previous_column_titles_data, **data}

        column1 = tk.get_action('footer_main_show')(context, {})

        column2 = tk.get_action('footer_column_links_search')(context, {'column_number': 2})
        column3 = tk.get_action('footer_column_links_search')(context, {'column_number': 3})
        column4 = {
            'social_media': tk.get_action('footer_social_media_items_search')(context, {}),
            'banner': tk.get_action('footer_banner_item_list')(context, {})
            }


        errors = errors or {}
        error_summary = error_summary or {}

        errors_json = h.dump_json(errors)

        return base.render(
            'footer-management/index.html', 
            extra_vars={
                u'errors_json': errors_json,
                u'data': data,
                u'column1': column1,
                u'column2': column2,
                u'column3': column3,
                u'column4': column4,
                u'errors': errors,
                u'error_summary': error_summary,
            }
        )


class Column1Edit(MethodView):
    def _prepare(self) -> Context:
        context = cast(Context, {
            u'model': model,
            u'session': model.Session,
            u'user': current_user.name,
            u'auth_user_obj': current_user,
        })

        try:
            tk.check_access(u'is_content_editor', context)
        except tk.NotAuthorized:
            return base.abort(403, _(u'Unauthorized to update CMS footer'))
        return context


    def post(self) -> Union[Response, str]:
        context = self._prepare()

        data_dict = _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(_parse_params(tk.request.form))))

        data_dict.update(
            _clean_dict(dict_fns.unflatten(
                    _tuplize_dict(_parse_params(tk.request.files))
                    )))

        try:
            column1_data = tk.get_action('footer_main_update')(context, data_dict)

        except tk.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.get(data_dict, errors, error_summary)

        url = 'cms_footer.index_main'
        return h.redirect_to(url)


    def get(self, data: Optional[dict[str, Any]] = None,
            errors: Optional[dict[str, Any]] = None,
            error_summary: Optional[dict[str, Any]] = None) -> str:

        context = self._prepare()
        
        data = data or _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(
                    _parse_params(request.args, ignore_keys=CACHE_PARAMETERS)
                )
            )
        )

        previous_column_titles_data = tk.get_action('footer_main_show')(context, {})

        data = {**previous_column_titles_data, **data}


        errors = errors or {}
        error_summary = error_summary or {}

        errors_json = h.dump_json(errors)

        return base.render(
            'footer-management/column1_edit.html', 
            extra_vars={
                u'errors_json': errors_json,
                u'data': data,
                u'errors': errors,
                u'error_summary': error_summary,
            }
        )


class ColumnLinkEdit(MethodView):
    def _prepare(self, col) -> Context:
        context = cast(Context, {
            u'model': model,
            u'session': model.Session,
            u'user': current_user.name,
            u'auth_user_obj': current_user,
        })

        try:
            if request.endpoint == 'cms_footer.link_add':
                tk.check_access(u'footer_column_link_create', context, {'column_number': col})
            else:
                tk.check_access(u'is_content_editor', context)
        except tk.NotAuthorized:
            return base.abort(403, _(u'Unauthorized to Add/update this footer Item'))
        return context


    def post(self, col, id=None) -> Union[Response, str]:
        context = self._prepare(col)

        data_dict = _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(_parse_params(tk.request.form))))

        data_dict.update({'column_number': col})
        try:
            if request.endpoint == 'cms_footer.link_add':
                link_data = tk.get_action('footer_column_link_create')(context, data_dict)
            else:
                data_dict.update({'id': id})
                link_data = tk.get_action('footer_column_link_update')(context, data_dict)

        except tk.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.get(col, id, data_dict, errors, error_summary)

        url = 'cms_footer.index_main'
        return h.redirect_to(url)


    def get(self, col, id=None, data: Optional[dict[str, Any]] = None,
            errors: Optional[dict[str, Any]] = None,
            error_summary: Optional[dict[str, Any]] = None) -> str:

        context = self._prepare(col)
        
        data = data or _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(
                    _parse_params(request.args, ignore_keys=CACHE_PARAMETERS)
                )
            )
        )

        previous_data = tk.get_action('footer_column_link_show')(context, {'id': id}) if request.endpoint == 'cms_footer.link_edit' else {}

        data = {**previous_data, **data, 'column_number': col}


        errors = errors or {}
        error_summary = error_summary or {}

        errors_json = h.dump_json(errors)

        return base.render(
            'footer-management/column_link_edit.html', 
            extra_vars={
                u'errors_json': errors_json,
                u'data': data,
                u'errors': errors,
                u'error_summary': error_summary,
                u'action': 'new' if not id else 'edit',
            }
        )


class SocialMediaItemEdit(MethodView):
    def _prepare(self) -> Context:
        context = cast(Context, {
            u'model': model,
            u'session': model.Session,
            u'user': current_user.name,
            u'auth_user_obj': current_user,
        })

        try:
            if request.endpoint == 'cms_footer.social_media_add':
                tk.check_access(u'footer_social_media_item_create', context)
            else:
                tk.check_access(u'is_content_editor', context)
        except tk.NotAuthorized:
            return base.abort(403, _(u'Unauthorized to Add/update this footer Item'))
        return context


    def post(self, id=None) -> Union[Response, str]:
        context = self._prepare()

        data_dict = _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(_parse_params(tk.request.form))))
        data_dict.update(
            _clean_dict(dict_fns.unflatten(
                    _tuplize_dict(_parse_params(tk.request.files))
                    )))


        try:
            if request.endpoint == 'cms_footer.social_media_add':
                link_data = tk.get_action('footer_social_media_item_create')(context, data_dict)
            else:
                data_dict.update({'id': id})
                link_data = tk.get_action('footer_social_media_item_update')(context, data_dict)

        except tk.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.get(id, data_dict, errors, error_summary)

        url = 'cms_footer.index_main'
        return h.redirect_to(url)


    def get(self, id=None, data: Optional[dict[str, Any]] = None,
            errors: Optional[dict[str, Any]] = None,
            error_summary: Optional[dict[str, Any]] = None) -> str:

        context = self._prepare()
        
        data = data or _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(
                    _parse_params(request.args, ignore_keys=CACHE_PARAMETERS)
                )
            )
        )

        previous_data = tk.get_action('footer_social_media_item_show')(context, {'id': id}) if request.endpoint == 'cms_footer.social_media_edit' else {}

        data = {**previous_data, **data}


        errors = errors or {}
        error_summary = error_summary or {}

        errors_json = h.dump_json(errors)

        return base.render(
            'footer-management/social_media_edit.html', 
            extra_vars={
                u'errors_json': errors_json,
                u'data': data,
                u'errors': errors,
                u'error_summary': error_summary,
                u'action': 'new' if not id else 'edit',
            }
        )


class BannerItemEdit(MethodView):
    def _prepare(self) -> Context:
        context = cast(Context, {
            u'model': model,
            u'session': model.Session,
            u'user': current_user.name,
            u'auth_user_obj': current_user,
        })

        try:
            if request.endpoint == 'cms_footer.banner_add':
                tk.check_access(u'footer_banner_item_create', context)
            else:
                tk.check_access(u'is_content_editor', context)
        except tk.NotAuthorized:
            return base.abort(403, _(u'Unauthorized to Add/update this footer Item'))
        return context


    def post(self, id=None) -> Union[Response, str]:
        context = self._prepare()

        data_dict = _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(_parse_params(tk.request.form))))
        data_dict.update(
            _clean_dict(dict_fns.unflatten(
                    _tuplize_dict(_parse_params(tk.request.files))
                    )))

        try:
            if request.endpoint == 'cms_footer.banner_add':
                link_data = tk.get_action('footer_banner_item_create')(context, data_dict)
            else:
                data_dict.update({'id': id})
                link_data = tk.get_action('footer_banner_item_update')(context, data_dict)

        except tk.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.get(id, data_dict, errors, error_summary)

        url = 'cms_footer.index_main'
        return h.redirect_to(url)


    def get(self, id=None, data: Optional[dict[str, Any]] = None,
            errors: Optional[dict[str, Any]] = None,
            error_summary: Optional[dict[str, Any]] = None) -> str:

        context = self._prepare()
        
        data = data or _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(
                    _parse_params(request.args, ignore_keys=CACHE_PARAMETERS)
                )
            )
        )

        previous_data = tk.get_action('footer_banner_item_show')(context, {'id': id}) if request.endpoint == 'cms_footer.banner_edit' else {}

        data = {**previous_data, **data}


        errors = errors or {}
        error_summary = error_summary or {}

        errors_json = h.dump_json(errors)

        return base.render(
            'footer-management/banner_edit.html', 
            extra_vars={
                u'errors_json': errors_json,
                u'data': data,
                u'errors': errors,
                u'error_summary': error_summary,
            }
        )


class ColumnLinkDelete(MethodView):
    def _prepare(self) -> Context:
        if 'cancel' in tk.request.args:
            tk.redirect_to('cms_footer.index_main')
    
        context = cast(Context, {
            u'model': model,
            u'session': model.Session,
            u'user': current_user.name,
            u'auth_user_obj': current_user,
        })

        try:
            tk.check_access(u'is_content_editor', context)
        except tk.NotAuthorized:
            return base.abort(403, _(u'Unauthorized to delete this footer Item'))
        return context


    def post(self, id) -> Union[Response, str]:
        context = self._prepare()

        data_dict = _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(_parse_params(tk.request.form))))

        try:
            link_data = tk.get_action('footer_column_link_delete')(context, {'id': id})

        except tk.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.get(id, data_dict, errors, error_summary)

        url = 'cms_footer.index_main'
        return h.redirect_to(url)


    def get(self, id, data: Optional[dict[str, Any]] = None,
            errors: Optional[dict[str, Any]] = None,
            error_summary: Optional[dict[str, Any]] = None) -> str:

        context = self._prepare()
        
        data = data or _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(
                    _parse_params(request.args, ignore_keys=CACHE_PARAMETERS)
                )
            )
        )

        item = tk.get_action('footer_column_link_show')(context, {'id': id})

        data = {**item, **data}

        errors = errors or {}
        error_summary = error_summary or {}

        errors_json = h.dump_json(errors)

        return base.render(
            'footer-management/confirm_delete.html', 
            extra_vars={
                u'errors_json': errors_json,
                u'data': data,
                u'item': item,
                u'type': 'Column Link',
                u'errors': errors,
                u'error_summary': error_summary,
            }
        )

class SocialMediaItemDelete(MethodView):
    def _prepare(self) -> Context:
        if 'cancel' in tk.request.args:
            tk.redirect_to('cms_footer.index_main')
    
        context = cast(Context, {
            u'model': model,
            u'session': model.Session,
            u'user': current_user.name,
            u'auth_user_obj': current_user,
        })

        try:
            tk.check_access(u'is_content_editor', context)
        except tk.NotAuthorized:
            return base.abort(403, _(u'Unauthorized to delete this footer Item'))
        return context


    def post(self, id) -> Union[Response, str]:
        context = self._prepare()

        data_dict = _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(_parse_params(tk.request.form))))

        try:
            link_data = tk.get_action('footer_social_media_item_delete')(context, {'id': id})

        except tk.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.get(id, data_dict, errors, error_summary)

        url = 'cms_footer.index_main'
        return h.redirect_to(url)


    def get(self, id, data: Optional[dict[str, Any]] = None,
            errors: Optional[dict[str, Any]] = None,
            error_summary: Optional[dict[str, Any]] = None) -> str:

        context = self._prepare()
        
        data = data or _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(
                    _parse_params(request.args, ignore_keys=CACHE_PARAMETERS)
                )
            )
        )

        item = tk.get_action('footer_social_media_item_show')(context, {'id': id})

        data = {**item, **data}

        errors = errors or {}
        error_summary = error_summary or {}

        errors_json = h.dump_json(errors)

        return base.render(
            'footer-management/confirm_delete.html', 
            extra_vars={
                u'errors_json': errors_json,
                u'data': data,
                u'item': item,
                u'type': 'Social Media',
                u'errors': errors,
                u'error_summary': error_summary,
            }
        )


class BannerItemDelete(MethodView):
    def _prepare(self) -> Context:
        if 'cancel' in tk.request.args:
            tk.redirect_to('cms_footer.index_main')
    
        context = cast(Context, {
            u'model': model,
            u'session': model.Session,
            u'user': current_user.name,
            u'auth_user_obj': current_user,
        })

        try:
            tk.check_access(u'is_content_editor', context)
        except tk.NotAuthorized:
            return base.abort(403, _(u'Unauthorized to delete this footer Item'))
        return context


    def post(self, id) -> Union[Response, str]:
        context = self._prepare()

        data_dict = _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(_parse_params(tk.request.form))))

        try:
            link_data = tk.get_action('footer_banner_item_delete')(context, {'id': id})

        except tk.ValidationError as e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.get(id, data_dict, errors, error_summary)

        url = 'cms_footer.index_main'
        return h.redirect_to(url)


    def get(self, id, data: Optional[dict[str, Any]] = None,
            errors: Optional[dict[str, Any]] = None,
            error_summary: Optional[dict[str, Any]] = None) -> str:

        context = self._prepare()
        
        data = data or _clean_dict(
            dict_fns.unflatten(
                _tuplize_dict(
                    _parse_params(request.args, ignore_keys=CACHE_PARAMETERS)
                )
            )
        )

        item = tk.get_action('footer_banner_item_show')(context, {'id': id})

        data = {**item, **data}

        errors = errors or {}
        error_summary = error_summary or {}

        errors_json = h.dump_json(errors)

        return base.render(
            'footer-management/confirm_delete.html', 
            extra_vars={
                u'errors_json': errors_json,
                u'data': data,
                u'item': item,
                u'type': 'Footer Banner',
                u'errors': errors,
                u'error_summary': error_summary,
            }
        )



blueprint.add_url_rule('/', view_func=IndexView.as_view('index_main'), endpoint='index_main')

blueprint.add_url_rule('/column/1/update', view_func=Column1Edit.as_view('column1_edit'), endpoint='column1_edit')

blueprint.add_url_rule('/column/<col>/add', view_func=ColumnLinkEdit.as_view('link_add'), endpoint='link_add')
blueprint.add_url_rule('/column/<col>/edit/<id>', view_func=ColumnLinkEdit.as_view('link_edit'), endpoint='link_edit')
blueprint.add_url_rule('/column/link/delete/<id>', view_func=ColumnLinkDelete.as_view('link_delete'), endpoint='link_delete')


blueprint.add_url_rule('/social-media/add', view_func=SocialMediaItemEdit.as_view('social_media_add'), endpoint='social_media_add')
blueprint.add_url_rule('/social-media/edit/<id>', view_func=SocialMediaItemEdit.as_view('social_media_edit'), endpoint='social_media_edit')
blueprint.add_url_rule('/social-media/delete/<id>', view_func=SocialMediaItemDelete.as_view('social_media_delete'), endpoint='social_media_delete')

blueprint.add_url_rule('/banner/add', view_func=BannerItemEdit.as_view('banner_add'), endpoint='banner_add')
blueprint.add_url_rule('/banner/edit/<id>', view_func=BannerItemEdit.as_view('banner_edit'), endpoint='banner_edit')
blueprint.add_url_rule('/banner/delete/<id>', view_func=BannerItemDelete.as_view('banner_delete'), endpoint='banner_delete')

def get_blueprints():
    return [blueprint]