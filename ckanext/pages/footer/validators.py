from ckan.plugins import toolkit as tk
from ckanext.pages.footer.model.footer import FooterBanner, FooterColumnLinks, FooterSocialMedia
Invalid = tk.Invalid
_ = tk._




def column_number_validator(value):
    if value in [2,3]:
        return value
    raise Invalid(_('Invalid Column Number.'))


def column_link_id_validator(value):
    record = FooterColumnLinks.get(id=value)
    if record:  return value
    raise Invalid(_('Invalid Id. Record not found.'))


def social_media_id_validator(value):
    record = FooterSocialMedia.get(id=value)
    if record:  return value
    raise Invalid(_('Invalid Id. Record not found.'))


def banner_id_validator(value):
    record = FooterBanner.get(id=value)
    if record:  return value
    raise Invalid(_('Invalid Id. Record not found.'))


def link_target_validator(value):
    if value in ['_self', '_blank']:
        return value
    raise Invalid(_('Invalid Target Selected.'))