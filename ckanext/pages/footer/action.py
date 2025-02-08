import datetime
import json
import logging

import ckan.lib.navl.dictization_functions as df
import ckan.lib.uploader as uploader
import ckan.plugins as p
from ckan import model
from ckan.logic import ValidationError
from ckan.plugins import toolkit as tk
from ckan.plugins.toolkit import _, h

from ckanext.pages.footer.model.footer import FooterBanner, FooterColumnLinks, FooterColumnTitles, FooterMain, FooterSocialMedia
import ckanext.pages.footer.schema as schema
from flask import  has_request_context
from ckan.logic import validate as validate_decorator


def get_actions():
    return {
        #GET
        'footer_main_show': footer_main_show,
        'footer_column_titles_show': footer_column_titles_show,
        'footer_column_link_show': footer_column_link_show,
        'footer_column_links_search': footer_column_links_search,
        'footer_social_media_item_show': footer_social_media_item_show,
        'footer_social_media_items_search': footer_social_media_items_search,
        'footer_banner_item_show': footer_banner_item_show,
        'footer_banner_item_list': footer_banner_item_list,
        
        #CREATE
        'footer_column_link_create': footer_column_link_create,
        'footer_social_media_item_create': footer_social_media_item_create,
        'footer_banner_item_create': footer_banner_item_create,
        
        #UPDATE
        'footer_main_update': footer_main_update,
        'footer_column_titles_update': footer_column_titles_update,
        'footer_column_link_update': footer_column_link_update,
        'footer_social_media_item_update': footer_social_media_item_update,
        'footer_banner_item_update': footer_banner_item_update,
        
        #DELETE
        'footer_column_link_delete': footer_column_link_delete,
        'footer_social_media_item_delete': footer_social_media_item_delete,
        'footer_banner_item_delete': footer_banner_item_delete,
    }


# GET

@tk.side_effect_free
def footer_main_show(context, data_dict):
    tk.check_access('is_content_editor', context)

    record = FooterMain.get()
    if record:
        result = record.as_dict()
    else:
        result = {
            'logo_en': FooterMain.DEFAULT_LOGO_EN,
            'logo_ar': FooterMain.DEFAULT_LOGO_AR,
            'phone_number': FooterMain.DEFAULT_PHONE_NUMBER,
            'modified': ''
        
        }

    if has_request_context:
        result.update({
            'display_logo': result.get('logo_ar') if h.lang() == 'ar' else  result.get('logo_en')
            })
        image_url = result.get('display_logo')
        result.update({
            'display_logo_url': h.url_for_static(
                'uploads/footer/{}'.format(image_url),
                qualified=True
                ) if image_url and image_url[0:6] not in {'http:/', 'https:'}  else image_url,
            })
    return result


@tk.side_effect_free
def footer_column_titles_show(context, data_dict):
    tk.check_access('is_content_editor', context)

    record = FooterColumnTitles.get()
    if record:
        result = record.as_dict()
    else:
        result = {
            'column2_en': FooterColumnTitles.DEFAULT_COLUMN2_EN,
            'column2_ar': FooterColumnTitles.DEFAULT_COLUMN2_AR,
            'column3_en': FooterColumnTitles.DEFAULT_COLUMN3_EN,
            'column3_ar': FooterColumnTitles.DEFAULT_COLUMN3_AR,
            'modified': '',
        }

        if has_request_context:
            result.update({
                'display_column2': result.get('column2_ar') if h.lang() == 'ar' else  result.get('column2_en'),
                'display_column3': result.get('column3_ar') if h.lang() == 'ar' else  result.get('column3_en'),
            })
    return result


@tk.side_effect_free
@validate_decorator(schema.column_link_get_schema)
def footer_column_link_show(context, data_dict):
    tk.check_access('is_content_editor', context)

    id = data_dict.get('id')

    record = FooterColumnLinks.get(id = id)

    result = record.as_dict()
    if has_request_context:
        result.update({
            'display_link': result.get('link_ar') if h.lang() == 'ar' else  result.get('link_en'),
            'display_title': result.get('title_ar') if h.lang() == 'ar' else  result.get('title_en'),
        })
    
    return result


@tk.side_effect_free
@validate_decorator(schema.column_links_search_schema)
def footer_column_links_search(context, data_dict):
    tk.check_access('is_content_editor', context)

    column_number = data_dict.get('column_number')

    q = FooterColumnLinks.filter(column_number=column_number)

    results = [record.as_dict() for record in q.all()]

    if has_request_context:
        for result in results:
            result.update({
                'display_link': result.get('link_ar') if h.lang() == 'ar' else  result.get('link_en'),
                'display_title': result.get('title_ar') if h.lang() == 'ar' else  result.get('title_en'),
            })
    
    return results


@tk.side_effect_free
@validate_decorator(schema.social_media_get_schema)
def footer_social_media_item_show(context, data_dict):
    tk.check_access('is_content_editor', context)

    id = data_dict.get('id')

    record = FooterSocialMedia.get(id = id)

    result = record.as_dict()
    if has_request_context:
        image_url = result.get('image_url', '')
        result.update({
            'display_link': result.get('link_ar') if h.lang() == 'ar' else  result.get('link_en'),
            'display_title': result.get('title_ar') if h.lang() == 'ar' else  result.get('title_en'),
            'dislay_image_url': h.url_for_static(
                'uploads/footer/{}'.format(image_url),
                qualified=True
                ) if image_url and image_url[0:6] not in {'http:/', 'https:'} else image_url,
        })

    return result


@tk.side_effect_free
def footer_social_media_items_search(context, data_dict):
    tk.check_access('is_content_editor', context)

    q = FooterSocialMedia.filter()
    
    results = [record.as_dict() for record in q.all()]

    if has_request_context:
        for result in results:
            image_url = result.get('image_url', '')
            result.update({
                'display_link': result.get('link_ar') if h.lang() == 'ar' else  result.get('link_en'),
                'display_title': result.get('title_ar') if h.lang() == 'ar' else  result.get('title_en'),
                'dislay_image_url': h.url_for_static(
                    'uploads/footer/{}'.format(image_url),
                    qualified=True
                    ) if image_url and image_url[0:6] not in {'http:/', 'https:'} else image_url,
            })
    
    return results


@tk.side_effect_free
@validate_decorator(schema.banner_get_schema)
def footer_banner_item_show(context, data_dict):
    tk.check_access('is_content_editor', context)

    id = data_dict.get('id')

    record = FooterBanner.get(id = id)

    result = record.as_dict()
    if has_request_context:
        image_url = result.get('image_url', '')
        result.update({
            'display_link': result.get('link_ar') if h.lang() == 'ar' else  result.get('link_en'),
            'display_title': result.get('title_ar') if h.lang() == 'ar' else  result.get('title_en'),
            'dislay_image_url': h.url_for_static(
                'uploads/footer/{}'.format(image_url),
                qualified=True
                ) if image_url and image_url[0:6] not in {'http:/', 'https:'} else image_url,
        })
        
    return result


@tk.side_effect_free
def footer_banner_item_list(context, data_dict):
    tk.check_access('is_content_editor', context)

    q = FooterBanner.filter()

    results = [record.as_dict() for record in q.all()]

    if has_request_context:
        for result in results:
            image_url = result.get('image_url', '')
            result.update({
                'display_link': result.get('link_ar') if h.lang() == 'ar' else  result.get('link_en'),
                'display_title': result.get('title_ar') if h.lang() == 'ar' else  result.get('title_en'),
                'dislay_image_url': h.url_for_static(
                    'uploads/footer/{}'.format(image_url),
                    qualified=True
                    ) if image_url and image_url[0:6] not in {'http:/', 'https:'} else image_url,
            })
    
    return results


# CREATE

@validate_decorator(schema.column_link_create_schema)
def footer_column_link_create(context, data_dict):
    tk.check_access('footer_column_link_create', context)

    record = FooterColumnLinks(**data_dict)
    record.add()
    record.commit()

    return tk.get_action('footer_column_link_show')(context, {'id': record.id}) 
    


@validate_decorator(schema.social_media_create_schema)
def footer_social_media_item_create(context, data_dict):
    tk.check_access('footer_social_media_item_create', context)

    data_dict = single_image_upload(context, data_dict)

    record = FooterSocialMedia(**data_dict)
    record.add()
    record.commit()

    return tk.get_action('footer_social_media_item_show')(context, {'id': record.id}) 


@validate_decorator(schema.banner_create_schema)
def footer_banner_item_create(context, data_dict):
    tk.check_access('footer_banner_item_create', context)

    data_dict = single_image_upload(context, data_dict)

    record = FooterBanner(**data_dict)
    record.add()
    record.commit()

    return tk.get_action('footer_banner_item_show')(context, {'id': record.id}) 



# UPDATE

@validate_decorator(schema.column1_update_schema)
def footer_main_update(context, data_dict):
    tk.check_access('is_content_editor', context)

    data_dict1 = data_dict.copy()
    data_dict2 = data_dict.copy()

    previous_record = FooterMain.get()

    upload = uploader.get_uploader('footer', previous_record.logo_en if previous_record and previous_record.logo_en else None)
    data_dict.update(data_dict1.get('__extras', {}))
    upload.update_data_dict(data_dict1, 'logo_en', 'logo_en_upload', 'clear_logo_en_upload')
    upload.upload(uploader.get_max_image_size())

    upload = uploader.get_uploader('footer', previous_record.logo_ar if previous_record and previous_record.logo_ar else None)
    upload.update_data_dict(data_dict2, 'logo_ar', 'logo_ar_upload', 'clear_logo_ar_upload')
    upload.upload(uploader.get_max_image_size())


    data_dict.update({k:v for k,v in data_dict1.items() if 'logo_en' in k})
    data_dict.update({k:v for k,v in data_dict2.items() if 'logo_ar' in k})

    FooterMain.patch_records(**data_dict, modified= datetime.datetime.utcnow())    

    return tk.get_action('footer_main_show')(context, {})


@validate_decorator(schema.column_titles_update_schema)
def footer_column_titles_update(context, data_dict):
    tk.check_access('is_content_editor', context)

    FooterColumnTitles.patch_records(**data_dict, modified= datetime.datetime.utcnow())
    return tk.get_action('footer_column_titles_show')(context, {})


@validate_decorator(schema.column_link_update_schema)
def footer_column_link_update(context, data_dict):
    tk.check_access('is_content_editor', context)

    FooterColumnLinks.patch_record(**data_dict, modified= datetime.datetime.utcnow())
    return tk.get_action('footer_column_link_show')(context, {'id': data_dict.get('id')})


@validate_decorator(schema.social_media_update_schema)
def footer_social_media_item_update(context, data_dict):
    tk.check_access('is_content_editor', context)

    print('data_dict1', data_dict)
    record = FooterSocialMedia.get(id=data_dict.get('id'))
    old_filename = None if not record or not record.image_url else record.image_url
    data_dict = single_image_upload(context, {**data_dict, 'old_filename': old_filename})
    print('data_dict2', data_dict)

    record = FooterSocialMedia.patch_record(**data_dict, modified= datetime.datetime.utcnow())
    return tk.get_action('footer_social_media_item_show')(context, {'id': record.id}) 


@validate_decorator(schema.banner_update_schema)
def footer_banner_item_update(context, data_dict):
    tk.check_access('is_content_editor', context)

    record = FooterBanner.get(id=data_dict.get('id'))
    old_filename = None if not record or not record.image_url else record.image_url
    data_dict = single_image_upload(context, {**data_dict, 'old_filename': old_filename})

    record = FooterBanner.patch_record(**data_dict, modified= datetime.datetime.utcnow())
    return tk.get_action('footer_banner_item_show')(context, {'id': record.id}) 


# DELETE

@validate_decorator(schema.column_link_get_schema)
def footer_column_link_delete(context, data_dict):
    tk.check_access('is_content_editor', context)

    id = data_dict.get('id')

    record = FooterColumnLinks.get(id=id)
    record.delete()
    record.commit()

    return {
        'id': record.id,
        'deleted': True
    }


@validate_decorator(schema.social_media_get_schema)
def footer_social_media_item_delete(context, data_dict):
    tk.check_access('is_content_editor', context)

    id = data_dict.get('id')

    record = FooterSocialMedia.get(id=id)
    record.delete()
    record.commit()

    return {
        'id': record.id,
        'deleted': True
    }


@validate_decorator(schema.banner_get_schema)
def footer_banner_item_delete(context, data_dict):
    tk.check_access('is_content_editor', context)

    id = data_dict.get('id')

    record = FooterBanner.get(id=id)
    record.delete()
    record.commit()

    return {
        'id': record.id,
        'deleted': True
    }


def single_image_upload(context, data_dict):
    tk.check_access('is_content_editor', context)

    old_filename = data_dict.get('old_filename', None)
    old_filename = old_filename if old_filename and old_filename[0:6] not in {'http:/', 'https:'} else None
    upload = uploader.get_uploader('footer', old_filename)

    data_dict.update(data_dict.get('__extras', {}))
    upload.update_data_dict(data_dict, 'image_url', 'image_upload', 'clear_upload')
    upload.upload(uploader.get_max_image_size())

    image_url = data_dict.get('image_url')

    return {**data_dict, 'image_url': image_url}