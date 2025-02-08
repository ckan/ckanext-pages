import ckan.plugins as p

import ckan.authz as authz

from ckan.plugins import toolkit as tk
from ckanext.pages.footer.model.footer import FooterBanner, FooterColumnLinks, FooterSocialMedia

_ = tk._

MAX_COLUMN_LINKS = 10
MAX_SOCIAL_MEDIA_LINKS = 6
MAX_BANNER_ITEMS = 4


def get_auth_functions():
    return {
        'footer_column_link_create': footer_column_link_create,
        'footer_social_media_item_create': footer_social_media_item_create,
        'footer_banner_item_create': footer_banner_item_create,
    }


def footer_column_link_create(context, data_dict):
    if not authz.is_authorized_boolean('is_content_editor', context):
        return {
            'success': False,
            'msg': _('User not authorized.')
        }
    
    column_number = data_dict.get('column_number', 2)
    if FooterColumnLinks.filter(column_number=column_number).count() > MAX_COLUMN_LINKS:
        return {
            'success': False,
            'msg': _('Maximum %s links can be added in a column.' % MAX_COLUMN_LINKS)
        }        
    
    return {'success': True}


def footer_social_media_item_create(context, data_dict):
    if not authz.is_authorized_boolean('is_content_editor', context):
        return {
            'success': False,
            'msg': _('User not authorized.')
        }
    
    if FooterSocialMedia.count() > MAX_SOCIAL_MEDIA_LINKS:
        return {
            'success': False,
            'msg': _('Maximum %s Social Media links can be.' % MAX_SOCIAL_MEDIA_LINKS)
        }        
    
    return {'success': True}


def footer_banner_item_create(context, data_dict):
    if not authz.is_authorized_boolean('is_content_editor', context):
        return {
            'success': False,
            'msg': _('User not authorized.')
        }
    
    if FooterBanner.count() > MAX_BANNER_ITEMS:
        return {
            'success': False,
            'msg': _('Maximum %s items can be added in Footer Banner.' % MAX_BANNER_ITEMS)
        }        
    
    return {'success': True}