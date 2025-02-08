import ckan.lib.helpers as h
from ckan import model
from ckanext.pages.db import HeaderLogo, HeaderMainMenu, HeaderSecondaryMenu
from sqlalchemy import case


def get_header_data():
    session = model.Session
    lang = h.lang()

    logo = session.query(HeaderLogo).filter_by(is_visible=True).first()
    logo_url = getattr(logo, f'logo_{lang}', None) if logo else ""

    main_menu_items = (
        session.query(HeaderMainMenu)
        .filter_by(is_visible=True).
        order_by(
            HeaderMainMenu.order,
            case(
                (HeaderMainMenu.menu_type == 'link', 0),
                (HeaderMainMenu.menu_type == 'menu', 1),
            ),
        )
        .all())

    secondary_menu_items = (
        session.query(HeaderSecondaryMenu)
        .filter_by(is_visible=True)
        .order_by(HeaderSecondaryMenu.order)
        .all()
    )

    def build_menu_tree(menu_items):
        menu_dict = {item.id: item for item in menu_items}
        root_items = []

        for item in menu_items:
            if item.parent_id:
                parent = menu_dict.get(item.parent_id)
                if parent and item not in parent.children:
                    parent.children.append(item)
            else:
                if item not in root_items:
                    root_items.append(item)

        return root_items

    main_menu_tree = build_menu_tree(main_menu_items)
    secondary_menu_tree = build_menu_tree(secondary_menu_items)

    return {
        'logo_url': logo_url,
        'main_menu_tree': main_menu_tree,
        'secondary_menu_tree': secondary_menu_tree,
        'lang': lang
    }

from ckan.common import _
import ckan.plugins.toolkit as tk

TARGET_VALUES_DICT = {
    '_self': _('Same Tab'),
    '_blank': _('New Tab'),
}

def get_helpers():
    return {
        'target_display': target_display,
        'footer_column1_data': footer_column1_data,
        'footer_column_titles_data': footer_column_titles_data,
        'footer_column2_items': footer_column2_items,
        'footer_column3_items': footer_column3_items,
        'footer_social_items': footer_social_items,
        'footer_banner_items': footer_banner_items,
        'get_header_data': get_header_data,
    }



def target_display(value):
    return TARGET_VALUES_DICT.get(value, '')
    
def footer_column1_data():
    return tk.get_action('footer_main_show')({'ignore_auth': True}, {})

def footer_column_titles_data():
    return tk.get_action('footer_column_titles_show')({'ignore_auth': True}, {})

def footer_column2_items():
    return tk.get_action('footer_column_links_search')({'ignore_auth': True}, {'column_number': 2})

def footer_column3_items():
    return tk.get_action('footer_column_links_search')({'ignore_auth': True}, {'column_number': 3})

def footer_social_items():
    return tk.get_action('footer_social_media_items_search')({'ignore_auth': True}, {})

def footer_banner_items():
    return tk.get_action('footer_banner_item_list')({'ignore_auth': True}, {})

